###        ###
## Settings ##
###        ###

import platform
import os
import subprocess

OS_NAME = platform.system()

MC_VERSION = "1.21.11"

if OS_NAME == "Windows":
    MC_DIR = os.path.abspath(r"C:\Program Files\Athilia\minecraft")
else:
    MC_DIR = os.path.expanduser("~/.athilia/minecraft")
print(OS_NAME)
print(MC_DIR)
