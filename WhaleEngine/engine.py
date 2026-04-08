from time import perf_counter
from traceback import format_exc
from .logging import logLn
from .window import Window
from .renderer2d import Renderer2D

class WhaleEngine:
    def __init__(self, width=800, height=600, title="Whale Engine"):
        logLn("Whale engine starting.")
        global current_app
        current_app = self
        self.width = width
        self.height = height
        self.window = Window(width, height, title)
        self.renderers = []
        self.plugins = {}
        self.attrs = {}
        self.update = None
        self.last_render = perf_counter()
        logLn("Whale engine started.")
    def run(self):
        try:
            logLn("Whale engine starting.")
            if len(self.renderers) == 0:
                self.renderers.append(Renderer2D())
            for i in self.renderers:
                i.start()
            logLn("Whale engine started")
            while not self.window.should_close():
                this_update = perf_counter()
                dt = this_update-self.last_render
                self.window.poll()
                self.window.clear()
                for i in self.plugins:
                    self.plugins[i].update(dt)
                if self.update != None:
                    self.update(dt)
                for i in self.renderers:
                    i.update(dt)
                    i.update_entitys(dt)
                    i.render()
                self.window.swap()
                self.last_render = this_update
        except Exception:
            logLn("Whale engine crashed with error:")
            logLn(format_exc(), "python")
        self.window.terminate()
    def close_app(self):
        self.window.terminate()

# app
current_app = None