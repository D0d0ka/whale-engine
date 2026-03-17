import json
import os

class json_save:
    def __init__(self, file,*,backup_content={}):
        if not file.endswith(".json"):
            raise ValueError("File must be a .json file")
        self.file = file
        if not os.path.exists(file):
            with open(file,"w") as f:
                json.dump(backup_content,f,indent=4)
    def read(self):
        with open(self.file,"r") as f:
            return json.load(f)
    def write(self, content):
        with open(self.file,"w") as f:
            return json.dump(content,f,indent=4)