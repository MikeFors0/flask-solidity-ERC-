from flask import Flask
from config import Config
from pymongo import MongoCLinet

app = Flask(__name__)
app.config.from_object(Config)

from . import controllers