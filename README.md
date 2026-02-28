# whale-engine
A game engine

In development!

A basic app looks like this:

from WhaleEngine import *

app = WhaleEngine(title="Whale engine app")
render = Renderer2D(app)
shapes = LoadShapes()

def update(dt):
    pass
app.update = update

app.run()

There are other various things that you can see from examples.
WhaleEngine.py and your projekt must be in same file.

Documentation:
- easy way to write and read json.
First you have to import it:
from json_save import json_save.

Then you need to select a file:

file = json_save("path to your file")

If it doesn't exist then it creates this file. You can give what to write into it like this or just leave it. then it writes into it {}.

content = {
    "sth":23
    4:{
        "sdg":[]
    }
}

file = json_save("path to your file", backup_content=content)

It can be list or dict.

To read it just do:

content = file.read()

It returns it's content. It reads it again.
To write into file just do:

new_content = {"message":"I love WhaleEngine!"}

file.write(new_content)