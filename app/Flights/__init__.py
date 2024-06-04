from flask import Blueprint

flight_management = Blueprint('flight_management', __name__)

from. import routes
from. import models
from. import schemas

def init_app(app):
    app.register_blueprint(flight_management)