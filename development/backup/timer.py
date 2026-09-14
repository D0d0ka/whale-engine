from WhaleEngine.logging import logLn

logLn("This is deprecated, use TimerSystem instead.", "warning")

class timer:
    def __init__(self, time):
        self.time = time
        self.current_time = 0
    def update(self, dt):
        self.current_time += dt
        if self.current_time > self.time:
            self.current_time = 0
            return True
        return False
    def reset(self):
        self.current_time = 0