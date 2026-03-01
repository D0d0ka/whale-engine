from WhaleEngine import *

app = WhaleEngine(title="Conversation")
conversation = ConversationRenderer()
conversation.add_message("Hello, how are you?")

shapes = LoadShapes()

def update(dt):
    if app.input.key_pressed(glfw.KEY_E):
        conversation.add_message("I'm fine, thank you!")
app.update = update

app.run()