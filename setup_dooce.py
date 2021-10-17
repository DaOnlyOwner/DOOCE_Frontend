import os
from shutil import copyfile
from pathlib import Path

Path("build").mkdir(parents=True,exist_ok=True)
cmake_call = os.popen("cd build && cmake . ../extern/DOOCE")
out = cmake_call.read()
cmake_call.close()
print("CMAKE OUTPUT:")
print(out)
print("")

build_call = os.popen("cd build && cmake --build . --config Release")
build_call.close()
Path("lib").mkdir(parents=True,exist_ok=True)
copyfile("build/Release/dooce.cp39-win_amd64.pyd","lib/dooce.cp39-win_amd64.pyd")
copyfile("build/Release/dooce.exp","lib/dooce.exp")
copyfile("build/Release/dooce.lib","lib/dooce.lib")
with open("lib/__init__.py",'a'):
    pass
