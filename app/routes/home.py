from flask import Flask, Blueprint, render_template, url_for
from ..services.count import contador
from app.utils.auth import login_required

home = Blueprint('home', __name__, template_folder="templates")

@home.route("/")
@login_required
def index():
    conteos = contador()
    return render_template('index.html', conteos=conteos)