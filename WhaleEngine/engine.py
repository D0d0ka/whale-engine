from .errorlogging import setup_global_error_handler, controlledrun
from .logging import logLn
setup_global_error_handler()
logLn("Global error handler set up.", "error logger")

from time import perf_counter
from traceback import format_exc
#from .window import Window
from .renderer2d import Renderer2D

# while developing this engine: I'll log everything.
from .logging import set_logging_folder
set_logging_folder("logs")

# TODO: add threading support to the engine, and make sure the error logging works across threads as well.
#import threading

class WhaleEngine:
    def __init__(self, window=None, **kwargs):
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
        self.clamping = False
        self.clamping_threshold = 0.1
        self.on_app_close = None
        self.running = False
        self.exit = self.close = self.close_app
        for key, value in kwargs.items():
            if key == "safemode":
                from .errorlogging import set_mode
                set_mode(value)
            else:
                setattr(self, key, value)
        logLn("Whale engine loaded.")
    def run(self):
        logLn("Whale engine starting.")
        if len(self.renderers) == 0:
            self.renderers.append(Renderer2D())
        for i in self.renderers:
            i.start()
        logLn("Whale engine started")
        self.running = True
        while not self.window.should_close():
            this_update = perf_counter()
            dt = this_update-self.last_render
            if self.clamping and dt > self.clamping_threshold:
                logLn(f"Clamping dt from {dt} to {self.clamping_threshold} seconds.", "warning")
                dt = self.clamping_threshold
            self.window.poll()
            self.window.clear()
            for i in self.plugins:
                controlledrun(self.plugins[i].update, dt)
            if self.update != None:
                controlledrun(self.update, dt)
            for i in self.renderers:
                controlledrun(i.update, dt)
                controlledrun(i.update_entitys, dt)
                controlledrun(i.render)
            self.window.swap()
            self.last_render = this_update
        if self.on_app_close:
            self.on_app_close()
        self.window.terminate()
        self.running = False
    def close_app(self):
        self.running = False
        if self.on_app_close:
            self.on_app_close()
        self.window.terminate()

# app
current_app = None