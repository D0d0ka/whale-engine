from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI
from WhaleEngine.prefabs.charactercontroller2d import CharacterController2D

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
renderer = Renderer2D()
textures = LoadTextures()
app.input = InputSystem()
ParentingSystem()
BetterCollisionSystem2D()

character = CharacterController2D(texture=textures.dodo, collider_w=50, collider_h=170, feetray_lenght=100, position=(0, 0))

QuadCollider2D(50, 170, position=(300, 0), visualize=True, visualition_color=Color.red)
QuadCollider2D(1000, 50, position=(0, -122), visualize=True, visualition_color=Color.green, layers=[0, "ground"])
QuadCollider2D(400, 50, position=(0, 150), visualize=True, visualition_color=Color.green, layers=[0, "ground"])

def update(dt):
    pass
app.update = update

app.run()