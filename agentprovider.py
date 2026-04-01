import os

kaust = "WhaleEngine"
with open("agent.txt", "w") as f:
    f.write("All python files in the WhaleEngine package code:\n")
    for root, dirs, files in os.walk(kaust):
        for file in files:
            if file.endswith(".py"):
                f.write(os.path.join(root, file) + "\n")