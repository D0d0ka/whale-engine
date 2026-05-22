from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # from WhaleEngine.WindowAPI.Vulkan import windowAPI # from WhaleEngine.WindowAPI.WebGL import windowAPI

window = windowAPI(title="Whale engine app") # create a window using the OpenGL API, you can also use Vulkan or WebGL by changing the import above and uncommenting the line below
app = WhaleEngine(window=window) # create app with the window we just made
renderer = Renderer2D() # create a 2D renderer
#app.input = InputSystem() # loads input system so you can use app.input instead of app.InputSystem
#shapes = LoadShapes() # use built in shapes
#textures = LoadTextures() # use built textures

#entity = Entity2D(texture=textures.whale) # create an entity with the whale texture

def update(dt):
    #if app.input.key(Keys.SPACE): # check if space is being pressed
    #    entity.rotation += 90 * dt # rotate entity 90 degrees per second
    #    entity.x += 100 * dt # move entity 100 pixels to the right per second
    pass
app.update = update # set the app's update function to the one we just made

app.run() # run the app