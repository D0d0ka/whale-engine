from .plugin import Plugin
from .helpers import none

class TimerPlugin(Plugin):
    def __init__(self, engine):
        super().__init__(engine)
        self.timers = []
        self.delays = []
    def update(self, delta_time):
        removing_timers = []
        for i in self.timers:
            i.time -= delta_time
            if i.time <= 0:
                i.over = True
                removing_timers.append(i)
        for i in removing_timers:
            self.timers.remove(i)
        removing_delays = []
        for i in self.delays:
            i['delay'] -= delta_time
            if i['delay'] <= 0:
                i['callback']()
                removing_delays.append(i)
        for i in removing_delays:
            self.delays.remove(i)

class Timer:
    def __init__(self, lenght):
        self.time = lenght
        self.over = False
        from .engine import current_app
        current_app.TimerPlugin.timers.append(self)

def delay(lenght=1, func=none):
    from .engine import current_app
    current_app.TimerPlugin.delays.append({'delay': lenght, 'callback': func})