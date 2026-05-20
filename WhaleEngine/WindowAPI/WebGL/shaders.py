import os
from WhaleEngine.assets import assets_dir

_shaders_dir = os.path.join(assets_dir, "shaders", "webGL")

from .shader import shader

default_vertex_shader_path = _shaders_dir + "/normal.vsh"
normal    = shader.from_file(_shaders_dir + "/normal.fsh",    default_vertex_shader_path)
grayscale = shader.from_file(_shaders_dir + "/grayscale.fsh", default_vertex_shader_path)
invert    = shader.from_file(_shaders_dir + "/invert.fsh",    default_vertex_shader_path)
sepia     = shader.from_file(_shaders_dir + "/sepia.fsh",     default_vertex_shader_path)
vignette  = shader.from_file(_shaders_dir + "/vignette.fsh",  default_vertex_shader_path)
outline   = shader.from_file(_shaders_dir + "/outline.fsh",   default_vertex_shader_path)
brighten  = shader.from_file(_shaders_dir + "/brighten.fsh",  default_vertex_shader_path)
    