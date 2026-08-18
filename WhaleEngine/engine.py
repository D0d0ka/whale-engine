from .logging import set_logging_folder
set_logging_folder("logs")

from .errorlogging import setup_global_error_handler, controlledrun
from .logging import logLn
setup_global_error_handler()
logLn("Global error handler set up.", "error logger")

from .renderer2d import Renderer2D

from time import perf_counter, strftime, localtime
from pathlib import Path
from sys import version
import platform

# TODO: add threading support to the engine, and make sure the error logging works across threads as well.
#import threading

logLn(f"Python version: {version}", "version")
version_file = Path(__file__).resolve().parent / "version"
try:
    version_text = version_file.read_text(encoding="utf-8").strip()
except FileNotFoundError:
    version_text = "unknown"
logLn(f"WhaleEngine version: {version_text}", "version")

class WhaleEngine:
    def __init__(self, window=None, **kwargs):
        loading_time = perf_counter()
        logLn("Whale engine loading.")
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
        self.start_time = None
        # Get workspace root: go up from WhaleEngine/engine.py -> WhaleEngine -> workspace
        path = Path(__file__).resolve().parent
        if path.name == "WhaleEngine":
            path = path.parent
        self.path = str(path)
        logLn(f"{self.path}","project")
        #self.last_values = {"window_width": window.width, "window_height": window.height, "window_title": window.title, "window_color": window.color}
        for key, value in kwargs.items():
            if key == "safemode":
                from .errorlogging import set_mode
                set_mode(value)
            else:
                setattr(self, key, value)
        logLn(f"Whale engine loaded in {round(perf_counter() - loading_time)} seconds.")
    def run(self):
        staring_time = perf_counter()
        logLn("Whale engine starting.")
        if len(self.renderers) == 0:
            self.renderers.append(Renderer2D())
        for i in self.renderers:
            i.start()
        self.start_time_str, self.start_time = strftime("%Y-%m-%d %H:%M:%S", localtime()), perf_counter()
        logLn(f"Whale engine started at {self.start_time_str}, took {round(perf_counter() - staring_time)} seconds.")
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
        self.close_app()
    def close_app(self):
        self.running = False
        if self.on_app_close:
            controlledrun(self.on_app_close)
        stoptime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        if self.start_time is not None:
            logLn(f"Whale engine stopped at {stoptime}. Total runtime: {round(perf_counter() - self.start_time, 2)} seconds.")
        else:
            logLn(f"Whale engine stopped at {stoptime} (did not fully start).")
        self.window.terminate()

# app
current_app = None