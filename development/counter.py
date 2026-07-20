import os

allowed_extensions = [".py", ".txt", ".js", ".html", ".css", ".fsh", ".vsh", ".log"]
print("Allowed file extensions: " + ", ".join(allowed_extensions))

folder = "WhaleEngine"
print(f"Scanning folder: {folder}")

entire_lenght = 0
entire_characters = 0
entire_lines = 0

file_data = []

for root, dirs, files in os.walk(folder):
    for file in files:
        for i in allowed_extensions:
            if file.endswith(i):
                file_path = os.path.join(root, file)
                file_lenght = os.path.getsize(file_path)
                file_characters = 0
                file_lines = 0
                with open(file_path, "r", encoding="utf-8", errors="ignore") as file_content:
                    for line in file_content:
                        file_characters += len(line)
                        file_lines += 1
                entire_lenght += file_lenght
                entire_characters += file_characters
                entire_lines += file_lines
                file_data.append((file_path, file_characters, file_lines, file_lenght))

with open("counter.txt", "w") as f:
    f.write(f"All files and their lengths in the {folder} package code:")
    for file_path, file_characters, file_lines, file_lenght in file_data:
        pct_chars = (file_characters / entire_characters * 100) if entire_characters else 0
        pct_lines = (file_lines / entire_lines * 100) if entire_lines else 0
        pct_size = (file_lenght / entire_lenght * 100) if entire_lenght else 0
        print(f"Found file: {file_path} (Characters: {file_characters} ({pct_chars:.1f}%), Lines: {file_lines} ({pct_lines:.1f}%), Size: {file_lenght} bytes ({pct_size:.1f}%))")
        f.write(f"\n{file_path} (Characters: {file_characters} ({pct_chars:.1f}%), Lines: {file_lines} ({pct_lines:.1f}%), Size: {file_lenght} bytes ({pct_size:.1f}%))")
    f.write(f"\nTotal size: {entire_lenght} bytes")
    f.write(f"\nTotal characters: {entire_characters}")
    f.write(f"\nTotal lines: {entire_lines}")

folder = "examples"
print(f"Scanning folder: {folder}")

entire_lenght = 0
entire_characters = 0
entire_lines = 0

file_data = []

for root, dirs, files in os.walk(folder):
    for file in files:
        for i in allowed_extensions:
            if file.endswith(i):
                file_path = os.path.join(root, file)
                file_lenght = os.path.getsize(file_path)
                file_characters = 0
                file_lines = 0
                with open(file_path, "r", encoding="utf-8", errors="ignore") as file_content:
                    for line in file_content:
                        file_characters += len(line)
                        file_lines += 1
                entire_lenght += file_lenght
                entire_characters += file_characters
                entire_lines += file_lines
                file_data.append((file_path, file_characters, file_lines, file_lenght))

with open("counter.txt", "a") as f:
    f.write(f"\n\nAll files and their lengths in the {folder} folder:")
    for file_path, file_characters, file_lines, file_lenght in file_data:
        pct_chars = (file_characters / entire_characters * 100) if entire_characters else 0
        pct_lines = (file_lines / entire_lines * 100) if entire_lines else 0
        pct_size = (file_lenght / entire_lenght * 100) if entire_lenght else 0
        print(f"Found file: {file_path} (Characters: {file_characters} ({pct_chars:.1f}%), Lines: {file_lines} ({pct_lines:.1f}%), Size: {file_lenght} bytes ({pct_size:.1f}%))")
        f.write(f"\n{file_path} (Characters: {file_characters} ({pct_chars:.1f}%), Lines: {file_lines} ({pct_lines:.1f}%), Size: {file_lenght} bytes ({pct_size:.1f}%))")
    f.write(f"\nTotal size: {entire_lenght} bytes")
    f.write(f"\nTotal characters: {entire_characters}")
    f.write(f"\nTotal lines: {entire_lines}")