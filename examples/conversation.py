from WhaleEngine import *

app = WhaleEngine(title="Conversation")
conversation = ConversationRenderer(app)
conversation.add_message("Hello, how are you?")

shapes = LoadShapes()

def update(dt):
    pass
app.update = update

app.run()