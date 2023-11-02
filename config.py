"""Config"""

import os

class Config(object):
    SECRET_KEY= os.urandom(69).hex()