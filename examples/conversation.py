from WhaleEngine import *
from WhaleEngine.conversationrenderer import ConversationRenderer
from WhaleEngine.WindowAPI.OpenGL import windowAPI

window = windowAPI(800, 600, "Conversation Example")
app = WhaleEngine(window=window)
conversation = ConversationRenderer()
conversation.add_message("Hello, how are you?")
app.input = InputSystem()

def update(dt):
    if app.input.key_pressed(Keys.E):
        conversation.add_message("I'm fine, thank you!")
app.update = update

app.run()