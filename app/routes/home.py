from flask import Flask, Blueprint, render_template, url_for
from ..services.count import contador

home = Blueprint('home', __name__, template_folder="templates")

@home.route("/")
def index():
    conteos = contador()
    print(conteos)
    return render_template('index.html', conteos=conteos)