import sys
import traceback
from .logging import logLn

def setup_global_error_handler():
    """Setup global exception handler to log all uncaught exceptions"""
    def global_exception_handler(exc_type, exc_value, exc_traceback):
        logLn("Uncaught exception:")
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_str = "".join(tb_lines)
        print("<python> " + tb_str)
        logLn(tb_str, "python", only_write=True)
    sys.excepthook = global_exception_handler