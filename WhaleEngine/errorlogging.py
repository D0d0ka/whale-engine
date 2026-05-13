import sys
import traceback
from .logging import logLn

def set_mode(mode):
    global safe_mode
    if mode == "safe" or mode == True:
        safe_mode = True
    elif mode == "verbose" or mode == False:
        safe_mode = False
    else:
        raise ValueError("Invalid mode. Use 'safe' or 'verbose'.")
safe_mode = True

errors = []
def register_error(error):
    if not str(error) in errors:
        errors.append(str(error))
        return True
    return False

def controlledrun(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if safe_mode:
            error_info = traceback.format_exc()
            if register_error(error_info):
                logLn(error_info, "python")
                logLn(f"Currently {len(errors)} unique exceptions logged.", "error logger")
        else:
            raise e

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