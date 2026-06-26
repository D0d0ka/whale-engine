from .entitys2d import Entity2D
from .require import requirePlugin
from .timer import Timer

class animatedEntity2D(Entity2D):
    def __init__(self, texture, x=0, y=0, renderer=None, animation_speed=1):
        super().__init__(texture, x=x, y=y, renderer=renderer)
        requirePlugin("TimerPlugin")
        self.animation_speed = animation_speed
        self.animation_timer = Timer(1 / self.animation_speed)
        self.current_frame = 0
        self.frames = []
        self.loop = True
        self.playing = True
    def update(self, dt):
        if self.playing:
            self.animation_timer.update(dt)
            if self.animation_timer.over:
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    if self.loop:
                        self.current_frame = 0
                    else:
                        self.current_frame = len(self.frames) - 1
                        self.playing = False
                self.texture = self.frames[self.current_frame]
                self.animation_timer.reset()