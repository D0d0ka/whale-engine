from .errorlogging import setup_global_error_handler, controlledrun
from .logging import logLn
setup_global_error_handler()
logLn("Global error handler set up.", "error logger")

from .renderer2d import Renderer2D

# while developing this engine: I'll log everything.
from .logging import set_logging_folder
set_logging_folder("logs")

from time import perf_counter
from pathlib import Path
from sys import version
import platform

# TODO: add threading support to the engine, and make sure the error logging works across threads as well.
#import threading

logLn(f"Python version: {version}", "version")
logLn(f"WhaleEngine version: 0.0.1 alpha", "version")

class WhaleEngine:
    def __init__(self, window=None, **kwargs):
        logLn("Whale engine starting.")
        self.os = platform.system()
        logLn(self.os, "os")
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
        path = Path(__file__).resolve().parent
        parts = path.parts
        if parts.count("WhaleEngine") > 1:
            idx = parts.index("WhaleEngine")
            path = Path(*parts[:idx + 1])
        self.path = str(path)
        logLn(f"{self.path}","project")
        #self.last_values = {"window_width": window.width, "window_height": window.height, "window_title": window.title, "window_color": window.color}
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
        if self.on_app_close:
            self.on_app_close()
        self.running = False
        if self.on_app_close:
            self.on_app_close()
        self.window.terminate()

# app
current_app = None