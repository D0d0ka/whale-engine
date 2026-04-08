import os
from WhaleEngine.logging import *

set_logging_file("agent.log")

allowed_extensions = [".py", ".png", ".mp3"]

logLn("Agent started. Scanning WhaleEngine package for python files.", "agent")
logLn("Allowed file extensions: " + ", ".join(allowed_extensions), "agent")

folder = "WhaleEngine"
logLn(f"Scanning folder: {folder}", "agent")

with open("agent.txt", "w") as f:
    f.write("All python files in the WhaleEngine package code:\n")
    for root, dirs, files in os.walk(folder):
        for file in files:
            for i in allowed_extensions:
                if file.endswith(i):
                    logLn(f"Found file: {os.path.join(root, file)}", "agent")
                    f.write(os.path.join(root, file) + "\n")

logLn("Agent finished scanning.", "agent")