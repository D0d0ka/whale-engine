import json
import os
import threading
import time

class json_database:
    def __init__(self, file,*,backup_content={}, indent=4):
        #from WhaleEngine.engine import current_app
        #current_app.need_stop.append(self)
        if not file.endswith(".json"):
            raise ValueError("File must be a .json file")
        self.file = file
        self.job_count = 0
        self.jobs = []
        self.stopping = False
        self.indent = indent
        if not os.path.exists(file):
            with open(file,"w") as f:
                json.dump(backup_content,f,indent=indent)
        def thread():
            while not self.stopping or self.job_count > 0:
                if self.job_count > 0:
                    job = self.jobs.pop(0)
                    with open(self.file, "w") as f:
                            return json.dump(job,f,indent=self.indent)
                    self.job_count -= 1
                else:
                    time.sleep(0.1)
        self.thread = threading.Thread(target=thread)
        self.thread.start()
    def read(self):
        if self.job_count > 0:
            return self.jobs[-1]
        with open(self.file,"r") as f:
            return json.load(f)
    def write(self, content):
        self.jobs.append(content)
        self.job_count += 1
    def stop(self):
        self.stopping = True
        self.thread.join()