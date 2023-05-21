# Under development
# This file has to be launched to start the application
import sys
import os
repo_path = os.path.abspath(__file__).split('src')[0]
src_path = os.path.join(repo_path, 'src')

# Add python modules to system path's variable to avoid '.' imports
sys.path.append(src_path)
sys.path.append(os.path.join(src_path, 'app'))
sys.path.append(os.path.join(src_path, 'youtube'))

if not os.path.isdir(os.path.join(repo_path, 'logs')):
    os.mkdir(os.path.join(repo_path, 'logs'))

from app.app_main import run

run()
