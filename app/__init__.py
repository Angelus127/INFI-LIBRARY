from flask import Flask, session
from .routes.search import search
from .routes.controller.media import media
from .routes.library import library
import os

def create_app():
    app = Flask(__name__)

    app.secret_key = os.urandom(24)

    app.register_blueprint(search)
    app.register_blueprint(library)
    app.register_blueprint(media)
    return app