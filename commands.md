# make venv
python -m venv .venv

# activate venv
windows:
.venv\Scripts\activate

linux/macos:
source .venv/bin/activate

# you need to install theese
python -m pip install -r requirements/mainrequirements.txt

# if you wan't to use openGL then you need to install this:
python -m pip install -r requirements/openGLrequirements.txt

# if you wan't to use Vulcan then you need to install this:
python -m pip install -r requirements/vulcanrequirements.txt

# to save requirements (development)
pip freeze > requirements.txt