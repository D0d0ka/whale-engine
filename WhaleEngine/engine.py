from time import perf_counter
from traceback import format_exc
from .logging import logLn
#from .window import Window
from .renderer2d import Renderer2D
from .errorlogging import setup_global_error_handler
import sys

# while developing this engine: I'll log everithing.
from .logging import set_logging_folder
set_logging_folder("logs")

class WhaleEngine:
    def __init__(self, window=None):
        try:
            logLn("Whale engine starting.")
            global current_app
            setup_global_error_handler()
            logLn("Global error handler set up.")            
            current_app = self
            if window == None:
                raise Exception("Window is required for WhaleEngine.")
            self.window = window#Window(400,400,"Whale Engine")
            self.renderers = []
            self.plugins = {}
            self.attrs = {}
            self.update = None
            self.last_render = perf_counter()
            logLn("Whale engine loaded.")
        except Exception:
            logLn("Whale engine failed to load with error:")
            print("<python> ",end="")
            logLn(format_exc(), "python", only_write=True)
            logLn("Whale engine failed to load, exiting.")
            sys.exit(1)
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
            print("<python> ", end="")
            logLn(format_exc(), "python", only_write=True)
        self.window.terminate()
    def close_app(self):
        self.window.terminate()

# app
current_app = None