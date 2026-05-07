from .shader import shader
import os

_shaders_dir = os.path.join(os.path.dirname(__file__), "assets", "shaders")

defeault_vertex_shader_path = _shaders_dir + "/normal.vsh"

normal = shader.from_file(_shaders_dir + "/normal.fsh",    defeault_vertex_shader_path)
grayscale = shader.from_file(_shaders_dir + "/grayscale.fsh", defeault_vertex_shader_path)
invert = shader.from_file(_shaders_dir + "/invert.fsh",    defeault_vertex_shader_path)
sepia = shader.from_file(_shaders_dir + "/sepia.fsh",     defeault_vertex_shader_path)
vignette = shader.from_file(_shaders_dir + "/vignette.fsh",  defeault_vertex_shader_path)
outline = shader.from_file(_shaders_dir + "/outline.fsh",   defeault_vertex_shader_path)
brighten = shader.from_file(_shaders_dir + "/brighten.fsh",  defeault_vertex_shader_path)