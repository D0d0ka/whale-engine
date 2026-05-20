import os
from WhaleEngine.logging import *

#set_logging_file("agent.log")

#def logLn(message, role="agent"): # I accidentaly broke WhaleEngine's code and was too lazy to replace all logLNs with print, so I made this function to log messages to the console and to a file at the same time. It is not the most efficient way to do it, but it works.
#    print(f"<{role}> {message}")

allowed_extensions = [".py", ".png", ".mp3", ".txt"]

logLn("Agent started. Scanning WhaleEngine package for python files.", "agent")
logLn("Allowed file extensions: " + ", ".join(allowed_extensions), "agent")

folder = "WhaleEngine"
logLn(f"Scanning folder: {folder}", "agent")

with open("agent.txt", "w") as f:
    f.write("All files in the WhaleEngine package code:")
    for root, dirs, files in os.walk(folder):
        for file in files:
            for i in allowed_extensions:
                if file.endswith(i):
                    logLn(f"Found file: {os.path.join(root, file)}", "agent")
                    f.write("\n"+os.path.join(root, file))

folder = "requirements"
logLn(f"Scanning folder: {folder}", "agent")

with open("agent.txt", "a") as f:
    f.write("\n\nAll files in the requirements folder:")
    for root, dirs, files in os.walk(folder):
        for file in files:
            for i in allowed_extensions:
                if file.endswith(i):
                    logLn(f"Found file: {os.path.join(root, file)}", "agent")
                    f.write("\n"+os.path.join(root, file))

folder = "examples"
logLn(f"Scanning folder: {folder}", "agent")

with open("agent.txt", "a") as f:
    f.write("\n\nAll files in the examples folder:")
    for root, dirs, files in os.walk(folder):
        for file in files:
            for i in allowed_extensions:
                if file.endswith(i):
                    logLn(f"Found file: {os.path.join(root, file)}", "agent")
                    f.write("\n"+os.path.join(root, file))

logLn("Agent finished scanning.", "agent")