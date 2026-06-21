from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # from WhaleEngine.WindowAPI.Vulkan import windowAPI # from WhaleEngine.WindowAPI.WebGL import windowAPI

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
renderer = Renderer2D()
app.input = InputSystem()
ParentingSystem()
TimerSystem()
BetterCollisionSystem2D(update_interval=0)
shapes = LoadShapes() #use built in shapes
textures = LoadTextures() #use built textures

collider = QuadCollider2D(100, 1000, position=(-160, 0), visualize=True)

player = Entity2D(texture=textures.dodo,scale=(0.5, 0.5), position=(0, 0))
player.collider = QuadCollider2D(100, 100, position=(0, 0), visualize=False)
ParentIn(player, player.collider)

last_safe_x = player.x

def update(dt):
    global last_safe_x
    if app.input.key(Keys.ESCAPE):
        app.exit()
    if player.collider.colliding:
        player.x = last_safe_x
    last_safe_x = player.x
    if app.input.key(Keys.A):
        player.x -= 100 * dt
        player.scale_x = 0.5
    if app.input.key(Keys.D):
        player.x += 100 * dt
        player.scale_x = -0.5
app.update = update

app.run()