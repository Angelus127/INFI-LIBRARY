from flask import Flask, Blueprint, render_template, url_for

home = Blueprint('home', __name__, template_folder="templates")

@home.route("/")
def index():
    return render_template('index.html')