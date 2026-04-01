from .plugin import Plugin
import numpy as np
import importlib
import os
import threading

def _require_audio_module(module_name, package_name):
    try:
        return importlib.import_module(module_name)
    except ImportError as error:
        raise RuntimeError(f"{package_name} is required for the sound system. Install dependencies from requirements.txt.") from error

def _resample_audio(data, src_rate, dst_rate):
    if src_rate == dst_rate:
        return data
    if len(data) == 0:
        return data
    src_positions = np.arange(len(data), dtype=np.float32)
    dst_len = max(1, int(len(data) * float(dst_rate) / float(src_rate)))
    dst_positions = np.linspace(0, len(data) - 1, dst_len, dtype=np.float32)
    channels = []
    for channel_idx in range(data.shape[1]):
        channels.append(np.interp(dst_positions, src_positions, data[:, channel_idx]))
    return np.stack(channels, axis=1).astype(np.float32)

def _match_channel_count(data, channels):
    if data.shape[1] == channels:
        return data
    if channels == 1:
        return data.mean(axis=1, keepdims=True).astype(np.float32)
    if data.shape[1] == 1:
        return np.repeat(data, channels, axis=1).astype(np.float32)
    return data[:, :channels].astype(np.float32)

class SoundSystem(Plugin):
    def __init__(self):
        super().__init__()
        self.sounds = {}
        self.sd = _require_audio_module("sounddevice", "sounddevice")
        self.sf = _require_audio_module("soundfile", "soundfile")
        self.sample_rate = 44100
        self.channels = 2
        self.block_size = 1024
        self._stream = None
        self._active_playbacks = []
        self._lock = threading.Lock()

    def _ensure_stream(self):
        if self._stream is not None:
            return
        try:
            self._stream = self.sd.OutputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
                blocksize=self.block_size,
                callback=self._audio_callback,
            )
            self._stream.start()
        except Exception as error:
            raise RuntimeError(f"Failed to start audio output stream: {error}")

    def _audio_callback(self, outdata, frames, time_info, status):
        del time_info
        if status:
            pass
        outdata.fill(0)
        finished = []
        with self._lock:
            for playback in self._active_playbacks:
                sound = playback["sound"]
                position = playback["position"]
                write_index = 0
                while write_index < frames:
                    if position >= sound.frame_count:
                        if playback["loops"] == -1:
                            position = 0
                        elif playback["loops"] > 0:
                            playback["loops"] -= 1
                            position = 0
                        else:
                            finished.append(playback)
                            sound.is_playing = False
                            break
                    remaining_source = sound.frame_count - position
                    remaining_target = frames - write_index
                    take = min(remaining_source, remaining_target)
                    if take <= 0:
                        break
                    outdata[write_index:write_index + take] += sound.frames[position:position + take] * playback["volume"]
                    position += take
                    write_index += take
                playback["position"] = position
            if finished:
                self._active_playbacks = [item for item in self._active_playbacks if item not in finished]
        np.clip(outdata, -1.0, 1.0, out=outdata)

    def _play_sound(self, sound, loops=0):
        loops = int(loops)
        with self._lock:
            self._active_playbacks.append({
                "sound": sound,
                "position": 0,
                "loops": loops,
                "volume": sound.volume,
            })
            sound.is_playing = True
        self._ensure_stream()

    def _stop_sound(self, sound):
        with self._lock:
            self._active_playbacks = [item for item in self._active_playbacks if item["sound"] is not sound]
            sound.is_playing = False

    def _update_sound_volume(self, sound):
        with self._lock:
            for playback in self._active_playbacks:
                if playback["sound"] is sound:
                    playback["volume"] = sound.volume

    def load_sound(self, name, path):
        self.sounds[name] = Sound(name, path, self)
        return self.sounds[name]
    def play_sound(self, name, loops=0):
        if name in self.sounds:
            self.sounds[name].play(loops=loops)
        else:
            raise ValueError(f"Sound not found: {name}")
    def stop_sound(self, name):
        if name in self.sounds:
            self.sounds[name].stop()
        else:
            raise ValueError(f"Sound not found: {name}")
    def stop_all_sounds(self):
        with self._lock:
            for sound in self.sounds.values():
                sound.is_playing = False
            self._active_playbacks = []
    def set_volume(self, name, volume):
        if name in self.sounds:
            self.sounds[name].set_volume(volume)
        else:
            raise ValueError(f"Sound not found: {name}")
    def update(self, dt):
        for sound in self.sounds.values():
            sound.refresh_state()

class Sound:
    def __init__(self, name, path):
        from .engine import current_app
        if not os.path.isfile(path):
            raise ValueError(f"Sound file not found: {path}")
        self.name = name
        if hasattr(current_app, "SoundSystem") and current_app.SoundSystem is not None:
            current_app.SoundSystem.sounds[name] = self
            self.sound_system = current_app.SoundSystem
        else:
            raise RuntimeError("SoundSystem plugin is not available in the current application.")
        self.path = path
        try:
            frames, sample_rate = self.sound_system.sf.read(path, dtype="float32", always_2d=True)
        except Exception as error:
            raise ValueError(f"Failed to load sound file: {path}. {error}") from error
        frames = _resample_audio(frames, sample_rate, self.sound_system.sample_rate)
        frames = _match_channel_count(frames, self.sound_system.channels)
        self.frames = np.ascontiguousarray(frames, dtype=np.float32)
        self.frame_count = len(self.frames)
        self.volume = 1.0
        self.is_playing = False
    def play(self, loops=0):
        self.sound_system._play_sound(self, loops=loops)
    def stop(self):
        self.sound_system._stop_sound(self)
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, float(volume)))
        self.sound_system._update_sound_volume(self)
    def get_volume(self):
        return self.volume
    def refresh_state(self):
        pass