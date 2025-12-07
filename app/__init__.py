from flask import Flask
from .routes.search import search
from .routes.library import library

def create_app():
    app = Flask(__name__)

    app.register_blueprint(search)
    app.register_blueprint(library)
    return app