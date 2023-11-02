from flask import Flask, redirect, render_template, request, session
from . import app

@app.route("/")
def index():
    return render_template("base.html")