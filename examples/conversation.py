from WhaleEngine import *
from WhaleEngine.conversationrenderer import ConversationRenderer

app = WhaleEngine(title="Conversation")
conversation = ConversationRenderer()
conversation.add_message("Hello, how are you?")
app.input = InputSystem()

shapes = LoadShapes()

def update(dt):
    if app.input.key_pressed(glfw.KEY_E):
        conversation.add_message("I'm fine, thank you!")
app.update = update

app.run()