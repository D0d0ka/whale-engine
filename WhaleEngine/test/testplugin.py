from WhaleEngine.plugin import Plugin
from WhaleEngine.logging import logLn

class TestPlugin(Plugin):
    def __init__(self):
        super().__init__(requirements=["CircleCollisionSystem2D"], incompatibilities=["BetterCollisionSystem2D"])
        self.time_to_next_log = 0
    def update(self, dt):
        self.time_to_next_log -= dt
        if self.time_to_next_log <= 0:
            logLn("TestPlugin is updating.")
            self.time_to_next_log = 1