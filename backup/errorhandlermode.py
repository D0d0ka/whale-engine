import sys
import traceback
from .logging import logLn

errors = []

def setup_global_error_handler(mode="safe"):
    """Setup global exception handler to log all uncaught exceptions"""
    def global_exception_handler(exc_type, exc_value, exc_traceback):
        logLn("Uncaught exception:", "error logger")
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_str = "".join(tb_lines)
        if mode == "safe":
            if not tb_str in errors:
                errors.append(tb_str)
                logLn(tb_str, "python")
                logLn(f"Currently {len(errors)} unique uncaught exceptions logged.", "error logger")
                #logLn("Exiting due to uncaught exception.")
            
        elif mode == "verbose":
            logLn(tb_str, "python")
            logLn("Exiting due to uncaught exception.", "error logger")
            sys.exit(1)
    sys.excepthook = global_exception_handler