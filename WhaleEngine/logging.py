from datetime import datetime
from uuid import uuid4
from os import makedirs, path as os_path

logging_file = None
logging_mode = "console" # can be: "console", "file", "folder"

def set_logging_file(path):
    global logging_file, logging_mode
    logging_file = path
    logging_mode = "file"
    string = f"<Logger> Log file set to {path} and created."
    with open(logging_file, "w") as f:
        f.write(string)
    print(string)

def set_logging_folder(path):
    global logging_mode, logging_file
    logging_mode = "folder"
    logging_file = f"{path}/{datetime.now().strftime('%H-%M-%S_%d-%m-%Y')}&&{str(uuid4())[:10]}.log"
    string = f"<Logger> Log file set to {logging_file} and created."
    if not os_path.exists(path):
        makedirs(path, exist_ok=True)
        string = f'<Logger> Logging folder "{path}" missing. Created new folder.\n{string}'
    with open(logging_file, "w") as f:
        f.write(string)    
    print(string)

def logLn(message, by="WhaleEngine"):
    string = f"<{by}> {message}"
    print(string)
    if not logging_file:
        return
    with open(logging_file, "a") as f:
        f.write(f"\n{string}")