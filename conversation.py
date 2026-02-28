from WhaleEngine import *

app = WhaleEngine(title="Conversation")
conversation = ConversationRenderer(app)

shapes = LoadShapes()

def update(dt):
    pass
app.update = update

app.run()