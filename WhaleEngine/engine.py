from .errorlogging import setup_global_error_handler
from .logging import logLn
setup_global_error_handler()
logLn("Global error handler set up.")

from time import perf_counter
from traceback import format_exc
#from .window import Window
from .renderer2d import Renderer2D

# while developing this engine: I'll log everithing.
from .logging import set_logging_folder
set_logging_folder("logs")

class WhaleEngine:
    def __init__(self, window=None):
        logLn("Whale engine starting.")
        global current_app          
        current_app = self
        if window == None:
            raise Exception("Window API is required for WhaleEngine.")
        self.window = window
        self.renderers = []
        self.plugins = {}
        self.attrs = {}
        self.update = None
        self.last_render = perf_counter()
        logLn("Whale engine loaded.")
    def run(self):
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
        self.window.terminate()
    def close_app(self):
        self.window.terminate()

# app
current_app = None