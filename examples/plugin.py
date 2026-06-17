from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI

#simple plugin that prints "Dodo!" every [delay] seconds, using the TimerPlugin to keep track of time
class DodoPlugin(Plugin):
    def __init__(self, delay=5):
        super().__init__(requirements=["TimerPlugin"], incompatibilities=[])
        self.timer = Timer(delay)
    def update(self, dt):
        if self.timer.over:
            print("Dodo!")
            self.timer.reset()

window = windowAPI("Dodo Plugin example",800, 600)
app = WhaleEngine(window=window)
TimerPlugin()
DodoPlugin(1)
app.run()