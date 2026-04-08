from WhaleEngine.logging import logLn

min_fps = float("inf")
max_fps = avg_fps = fps_timer = frame_count = 0
FPS = 60

def FPS_counter(dt, fps_timer_lenght=1,print_fps=False):
    global min_fps, max_fps, avg_fps, fps_timer, frame_count, FPS
    if dt <= 0:
        return
    if dt > 0.25:
        return
    fps = 1.0 / dt
    min_fps = min(min_fps, fps)
    max_fps = max(max_fps, fps)
    if avg_fps == 0:
        avg_fps = fps
    else:
        avg_fps = avg_fps * 0.9 + fps * 0.1
    fps_timer += dt
    frame_count += 1
    if fps_timer >= fps_timer_lenght:
        if print_fps:
            logLn(f"FPS: {fps}")
        FPS = fps
        fps_timer = 0.0
        frame_count = 0

def get_FPS():
    return FPS

def summarize_FPS(print_summary=False):
    global min_fps, max_fps, avg_fps, fps_timer, frame_count
    summary = f"Min FPS: {min_fps},\nAvg FPS: {avg_fps},\nMax FPS: {max_fps}"
    if print_summary:
        logLn(summary)
    return summary