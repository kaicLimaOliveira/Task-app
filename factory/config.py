import sys
import os
import secrets
import json
from pathlib import Path

var_env = json.load(open(str(Path(__file__).parent.parent) + os.sep + 'config.json'))

if sys.platform == "linux" or sys.platform == "linux2":
    debug = True
    env = 'dev'
else:
    debug = False
    env = 'dev'

secret_key = str(secrets.token_hex(16))
