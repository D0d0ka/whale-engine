import os
from WhaleEngine.assets import assets_dir

_shaders_dir = os.path.join(assets_dir, "shaders", "webGL")

def _read_shader_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

class shader:
    @classmethod
    def from_file(cls, fragment_path, vertex_path=None):
        frag_code = _read_shader_file(fragment_path)
        if vertex_path is None:
            vertex_path = os.path.join(_shaders_dir, "normal.vsh")
        vert_code = _read_shader_file(vertex_path)
        return {"fragment": frag_code, "vertex": vert_code}
