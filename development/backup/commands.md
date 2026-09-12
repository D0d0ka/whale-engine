# install it
git clone https://github.com/D0d0ka/whale-engine.git

# make venv
windows:

python -m venv .venv

linux/macos

python3 -m venv .venv

# activate venv
windows:

.venv\Scripts\activate

linux/macos:

source .venv/bin/activate

# upgrade pip

windows:

python.exe -m pip install --upgrade pip

linux/macos:

pip install --upgrade pip

# you need to install theese
python -m pip install -r WhaleEngine/requirements/mainrequirements.txt

# if you wan't to use openGL then you need to install this:
python -m pip install -r WhaleEngine/requirements/openGLrequirements.txt

# if you wan't to use Vulcan then you need to install this:
python -m pip install -r WhaleEngine/requirements/vulcanrequirements.txt

# if you wan't to use WebGL then you need to install this (Currently there are none): 
python -m pip install -r WhaleEngine/requirements/webGLrequirements.txt

# to save requirements (development)
pip freeze > requirements.txt