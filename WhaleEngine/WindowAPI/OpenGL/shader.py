import os

_shaders_dir = os.path.join(os.path.dirname(__file__), "assets", "shaders")

def _load_default_vertex():
    path = os.path.join(_shaders_dir, "normal.vsh")
    with open(path) as f:
        return f.read()

class Shader:
    def __init__(self, fragment_code, vertex_code=None):
        self.fragment_code = fragment_code
        self._vertex_code = vertex_code
        self._program = None
        self._uniform_locations = {}

    @property
    def vertex_code(self):
        if self._vertex_code is None:
            return _load_default_vertex()
        return self._vertex_code

    def _compile(self):
        if self._program is not None:
            return self._program
        from OpenGL.GL import (
            glCreateShader, glShaderSource, glCompileShader,
            glGetShaderiv, glGetShaderInfoLog,
            glCreateProgram, glAttachShader, glLinkProgram,
            glGetProgramiv, glGetProgramInfoLog,
            glDeleteShader,
            GL_VERTEX_SHADER, GL_FRAGMENT_SHADER,
            GL_COMPILE_STATUS, GL_LINK_STATUS,
        )
        from WhaleEngine.logging import logLn

        vert = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vert, self.vertex_code)
        glCompileShader(vert)
        if not glGetShaderiv(vert, GL_COMPILE_STATUS):
            raise RuntimeError("Vertex shader compile error: " + glGetShaderInfoLog(vert).decode())

        frag = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(frag, self.fragment_code)
        glCompileShader(frag)
        if not glGetShaderiv(frag, GL_COMPILE_STATUS):
            raise RuntimeError("Fragment shader compile error: " + glGetShaderInfoLog(frag).decode())

        prog = glCreateProgram()
        glAttachShader(prog, vert)
        glAttachShader(prog, frag)
        glLinkProgram(prog)
        if not glGetProgramiv(prog, GL_LINK_STATUS):
            raise RuntimeError("Shader link error: " + glGetProgramInfoLog(prog).decode())
        glDeleteShader(vert)
        glDeleteShader(frag)
        self._program = prog
        return prog

    def use(self):
        from OpenGL.GL import glUseProgram
        prog = self._compile()
        glUseProgram(prog)
        return prog

    @property
    def program(self):
        return self._compile()

    def _get_uniform_location(self, name):
        from OpenGL.GL import glGetUniformLocation

        if name not in self._uniform_locations:
            self._uniform_locations[name] = glGetUniformLocation(self.program, name)
        return self._uniform_locations[name]

    def set_mat4(self, name, value):
        from OpenGL.GL import glUniformMatrix4fv, GL_FALSE

        location = self._get_uniform_location(name)
        if location != -1:
            glUniformMatrix4fv(location, 1, GL_FALSE, value)

    def set_vec4(self, name, value):
        from OpenGL.GL import glUniform4f

        location = self._get_uniform_location(name)
        if location != -1:
            glUniform4f(location, value[0], value[1], value[2], value[3])

    def set_int(self, name, value):
        from OpenGL.GL import glUniform1i

        location = self._get_uniform_location(name)
        if location != -1:
            glUniform1i(location, value)

    def set_float(self, name, value):
        from OpenGL.GL import glUniform1f

        location = self._get_uniform_location(name)
        if location != -1:
            glUniform1f(location, value)

    @classmethod
    def from_file(cls, path, vertex_path=None):
        with open(path) as f:
            frag_code = f.read()
        vert_code = None
        if vertex_path:
            with open(vertex_path) as f:
                vert_code = f.read()
        return cls(frag_code, vert_code)

shader = Shader