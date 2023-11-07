from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# def checkSession(html):
#     return render_template(f"{html}.html")

from . import controllers
from . import web