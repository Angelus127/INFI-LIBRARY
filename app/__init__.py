from flask import Flask, session
from .routes.search import search_bp
from .controller.media import media
from .routes.library import library
from .routes.home import home
import os

def create_app():
    app = Flask(__name__)

    app.secret_key = os.urandom(24)

    app.register_blueprint(search_bp)
    app.register_blueprint(library)
    app.register_blueprint(media)
    app.register_blueprint(home)
    return app