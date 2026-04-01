logging_file = None

def set_logging_file(path):
    global logging_file
    logging_file = path

def logLn(message, by="WhaleEngine"):
    print(f"<{by}> {message}")
    if not logging_file:
        return
    with open(logging_file, "a") as f:
        f.write(f"[{by}] {message}\n")