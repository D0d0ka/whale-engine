Clone the project and create a virtual environment:

```bash
git clone https://github.com/D0d0ka/whale-engine.git
cd whale-engine
python -m venv .venv
```

Activate it:

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install the base dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r WhaleEngine/requirements/mainrequirements.txt
```

Then install the graphics backend you want to use:

OpenGL (recommended):
```bash
python -m pip install -r WhaleEngine/requirements/openGLrequirements.txt
```

Vulkan (most unstable):
```bash
python -m pip install -r WhaleEngine/requirements/vulcanrequirements.txt
```

WebGL:
```bash
python -m pip install -r WhaleEngine/requirements/webGLrequirements.txt
```
