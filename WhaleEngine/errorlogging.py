import sys
import traceback
from .logging import logLn

def setup_global_error_handler():
    """Setup global exception handler to log all uncaught exceptions"""
    def global_exception_handler(exc_type, exc_value, exc_traceback):
        logLn("Uncaught exception:", "error logger")
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_str = "".join(tb_lines)
        logLn(tb_str, "python")
        logLn("Exiting due to uncaught exception.")
        sys.exit(1)
    sys.excepthook = global_exception_handler