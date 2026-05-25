import os

allowed_extensions = [".py", ".png", ".mp3", ".txt", ".js", ".html", ".css", ".fsh", ".vsh", "coming"]

print("Allowed file extensions: " + ", ".join(allowed_extensions))

folder = "WhaleEngine"
print(f"Scanning folder: {folder}")

with open("agent.txt", "w") as f:
    f.write("All files in the WhaleEngine package code:")
    for root, dirs, files in os.walk(folder):
        for file in files:
            for i in allowed_extensions:
                if file.endswith(i):
                    print(f"Found file: {os.path.join(root, file)}")
                    f.write("\n"+os.path.join(root, file))

folder = "requirements"
print(f"Scanning folder: {folder}")

with open("agent.txt", "a") as f:
    f.write(f"\n\nAll files in the {folder} folder:")
    for root, dirs, files in os.walk(folder):
        for file in files:
            for i in allowed_extensions:
                if file.endswith(i):
                    print(f"Found file: {os.path.join(root, file)}", "agent")
                    f.write("\n"+os.path.join(root, file))

folder = "examples"
print(f"Scanning folder: {folder}")

with open("agent.txt", "a") as f:
    f.write(f"\n\nAll files in the {folder} folder:")
    for root, dirs, files in os.walk(folder):
        for file in files:
            for i in allowed_extensions:
                if file.endswith(i):
                    print(f"Found file: {os.path.join(root, file)}")
                    f.write("\n"+os.path.join(root, file))

print("Agent provider finished scanning.")