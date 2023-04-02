import subprocess
import os

HERE = os.path.abspath(os.path.dirname(__file__))

os.environ['PYTHONPATH'] = HERE

code = os.popen('code .')
code.close()