from .logging import logLn
from OpenGL.GL import *

class Renderer2D:
    def __init__(self):
        from .engine import current_app
        current_app.renderers.append(self)
        self.entities = []
        logLn("Renderer 2d loaded.")
    def start(self):
        pass
    def update(self,dt):
        pass
    def add(self, entity):
        self.entities.append(entity)
    def update_entitys(self,dt):
        for i in self.entities:
            if i.do_update:
                i.update(dt)
    def render(self):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        for e in self.entities:
            glBindTexture(GL_TEXTURE_2D, e.texture.id)
            glColor4f(e.color.r, e.color.g, e.color.b, e.color.a)

            glPushMatrix()
            glTranslatef(e.x, e.y, 0)
            glRotatef(e.rotation, 0, 0, 1)
            glScalef(e.scale_x, e.scale_y, 1)
            w = e.w / 2
            h = e.h / 2
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex2f(-w, -h)
            glTexCoord2f(1, 0); glVertex2f( w, -h)
            glTexCoord2f(1, 1); glVertex2f( w,  h)
            glTexCoord2f(0, 1); glVertex2f(-w,  h)
            glEnd()
            glPopMatrix()
        glColor4f(1,1,1,1)
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)