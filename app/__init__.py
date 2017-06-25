from flask import Flask


app = Flask(__name__)
from app import views ## put this after to avoid circular import error


def register_blueprints(app):
    from .views import BG_data
    app.register_blueprint(BG_data)

register_blueprints(app)
