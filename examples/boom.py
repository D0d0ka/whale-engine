from WhaleEngine import *
from WhaleEngine.helpers.fpscounter import *

set_logging_file("boom.log")

window_size_multiplier = 1.5

assets_folder = "boomassets/"

def load_texture(name):
    return Texture(assets_folder+"textures/"+name)

directions = {"up": (0, -1),"down": (0, 1),"left": (-1, 0),"right": (1, 0)}

app = WhaleEngine(title="Boom",width=round(window_size_multiplier*800),height=round(window_size_multiplier*600))
main_renderer = Renderer2D()
app.input = InputSystem()

openpath = load_texture("open.png")
closedpath = load_texture("closed.png")

class mainentity(Entity2D):
    def __init__(self, *, texture, color=Color.white, position=(0,0), scale=(1,1), rotation=0,update=True):
        super().__init__(texture=texture, color=color, position=position, scale=(scale[0]*window_size_multiplier,scale[1]*window_size_multiplier), rotation=rotation, update=update, renderer=main_renderer)

class path(mainentity):
    def __init__(self,open=True,color=Color.white,distance=1):
        if open:
            texture = openpath
        else:
            texture = closedpath
        super().__init__(texture=texture, color=color, scale=(1/distance/0.95,1/distance/0.95), update=False)

class entity(mainentity):
    def __init__(self, *, texture, position=(0,0), scale=(1,1), rotation=0,update=True):
        super().__init__(texture=texture, color=Color.white, position=position, scale=(scale[0]*window_size_multiplier,scale[1]*window_size_multiplier), rotation=rotation, update=update)

maps = [
    {
        "name":"test map",
        "map":[
            [1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],
        "spawn position":(4,4),
        "spawn way":"up"
    },
    {
        "name": "labyrinth valley",
        "map": [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # 0
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],  # 1
            [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1],  # 2
            [1,0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,1],  # 3
            [1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],  # 4
            [1,0,1,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1],  # 5
            [1,0,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1],  # 6
            [1,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],  # 7
            [1,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1],  # 8
            [1,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],  # 9
            [1,0,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1],  # 10
            [1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],  # 11
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]   # 12
        ],
        "spawn position": (20, 6),
        "spawn way": "up"
    },
    {
        "name":"closed get map",
        "map":[
            [0],
            [0],
            [0]
        ],
        "spawn position":(0,3),
        "spawn way":"up"
    },
]

class Map:
    def __init__(self, map_data):
        self.name = map_data["name"]
        self.map = map_data["map"]
        self.entities = {}
    def get_tile(self, position):
        x, y = position
        if y < 0 or y >= len(self.map):
            return None
        if x < 0 or x >= len(self.map[y]):
            return None
        return self.map[y][x]
    def get_view(self, position, view_direction, view_distance=100):
        dx, dy = directions[view_direction]
        x, y = position
        path = []
        for distance in range(1, view_distance + 1):
            pos = (x + dx * distance, y + dy * distance)
            tile = self.get_tile(pos)
            if tile is None:
                break
            entity = self.entities.get(pos)
            path.insert(0,{"distance": distance, "tile": tile, "entity": entity})
            
        return path

class Player:
    def __init__(self,position=(0,0), view_direction="up"):
        self.x, self.y = position
        self.view_direction = view_direction
        render_view(position,self.view_direction)
    def update(self,dt):
        if app.input.key_pressed(glfw.KEY_W):
            self.x += directions[self.view_direction][0]
            self.y += directions[self.view_direction][1]
            if current_map.get_tile((self.x,self.y)) == 1:
                self.x -= directions[self.view_direction][0]
                self.y -= directions[self.view_direction][1]
            else:
                render_view((self.x,self.y), self.view_direction)
        if app.input.key_pressed(glfw.KEY_S):
            self.x -= directions[self.view_direction][0]
            self.y -= directions[self.view_direction][1]
            if current_map.get_tile((self.x,self.y)) == 1:
                self.x += directions[self.view_direction][0]
                self.y += directions[self.view_direction][1]
            else:
                render_view((self.x,self.y), self.view_direction)
        if app.input.key_pressed(glfw.KEY_A):
            way = {"up": "left", "left": "down", "down": "right", "right": "up"}[self.view_direction]
            self.x += directions[way][0]
            self.y += directions[way][1]
            if current_map.get_tile((self.x,self.y)) == 1:
                self.x -= directions[way][0]
                self.y -= directions[way][1]
            else:
                render_view((self.x,self.y), self.view_direction)
        if app.input.key_pressed(glfw.KEY_D):
            way = {"up": "right", "right": "down", "down": "left", "left": "up"}[self.view_direction]
            self.x += directions[way][0]
            self.y += directions[way][1]
            if current_map.get_tile((self.x,self.y)) == 1:
                self.x -= directions[way][0]
                self.y -= directions[way][1]
            else:
                render_view((self.x,self.y), self.view_direction)
        if app.input.key_pressed(glfw.KEY_LEFT):
            self.view_direction = {"up": "left", "left": "down", "down": "right", "right": "up"}[self.view_direction]
            render_view((self.x,self.y), self.view_direction)
        if app.input.key_pressed(glfw.KEY_RIGHT):
            self.view_direction = {"up": "right", "right": "down", "down": "left", "left": "up"}[self.view_direction]
            render_view((self.x,self.y), self.view_direction)
        if app.input.key_pressed(glfw.KEY_ESCAPE):
            app.close_app()

current_map_num = 1

current_map_data = maps[current_map_num]
current_map_name = maps[current_map_num]["name"]
current_map = Map(current_map_data)
current_map_spawn_position = current_map_data["spawn position"] 
current_map_spawn_way = current_map_data["spawn way"]

view_entitys = []

def render_view(position, view_direction, view_distance=100):
    for i in view_entitys:
        destroy(i)
    view_entitys.clear()
    view = current_map.get_view(position, view_direction, view_distance)
    for i in view:
        if i["tile"] == 0:
            view_entitys.append(path(open=True, distance=i["distance"]))
        elif i["tile"] == 1:
            view_entitys.append(path(open=False, distance=i["distance"]))
        else:
            continue

player = Player(position=current_map_spawn_position, view_direction=current_map_spawn_way)

def update(dt):
    player.update(dt)
    FPS_counter(dt)
    app.window.set_title(f"Boom - {current_map_name} - FPS: {round(get_FPS())}")
    app.window.set_width(round(window_size_multiplier*800))
    app.window.set_height(round(window_size_multiplier*600))
app.update = update

app.run()