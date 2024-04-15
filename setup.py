import os
#os.system("pip uninstall gym-retro gym -y")
#os.system("pip install gym-retro gym==0.21.0")
import time
from pathlib import Path
import importlib
import shutil
path = Path(importlib.import_module("retro").__file__).parent/"data\\stable"
shutil.copytree("ROM/Asteroids",path/"Asteroids")
shutil.copytree("ROM/Gravitar",path/"Gravitar")
