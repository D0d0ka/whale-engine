from .shader import shader
from WhaleEngine.assets import assets_dir

import os

_shaders_dir = os.path.join(assets_dir, "shaders", "openGL")

defeault_vertex_shader_path = _shaders_dir + "/normal.vsh"

normal = shader.from_file(_shaders_dir + "/normal.fsh",    defeault_vertex_shader_path)
grayscale = shader.from_file(_shaders_dir + "/grayscale.fsh", defeault_vertex_shader_path)
invert = shader.from_file(_shaders_dir + "/invert.fsh",    defeault_vertex_shader_path)
sepia = shader.from_file(_shaders_dir + "/sepia.fsh",     defeault_vertex_shader_path)
vignette = shader.from_file(_shaders_dir + "/vignette.fsh",  defeault_vertex_shader_path)
outline = shader.from_file(_shaders_dir + "/outline.fsh",   defeault_vertex_shader_path)
brighten = shader.from_file(_shaders_dir + "/brighten.fsh",  defeault_vertex_shader_path)