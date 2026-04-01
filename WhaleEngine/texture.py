from PIL import Image
from OpenGL.GL import *

class Texture:
    def __init__(self, path):
        self.path = path
        img = Image.open(path).convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM)
        self.w, self.h = img.size
        data = img.tobytes()

        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(
            GL_TEXTURE_2D, 0,
            GL_RGBA, self.w, self.h, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, data
        )