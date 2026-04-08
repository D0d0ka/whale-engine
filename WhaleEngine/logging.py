logging_file = None

def set_logging_file(path):
    global logging_file
    logging_file = path
    string = f"<Logger> Log file set to {path} and created."
    with open(logging_file, "w") as f:
        f.write(string)
    print(string)

def logLn(message, by="WhaleEngine"):
    print(f"<{by}> {message}")
    if not logging_file:
        return
    with open(logging_file, "a") as f:
        f.write(f"\n<{by}> {message}")