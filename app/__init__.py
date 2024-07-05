""" The create_app function wraps the creation of a new Flask object, and
    returns it after it's loaded up with configuration settingsusing app.config
"""
import os
import atexit
import logging

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required
from flask_mail import Mail
from dotenv import load_dotenv
from app import config
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flasgger import Swagger
# from flask_script import Manager

load_dotenv()

jwt = JWTManager()
mail = Mail()
db = SQLAlchemy()  

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


<<<<<<< HEAD
def create_app(config_name='development'):
=======
def create_app(config_name):
>>>>>>> upstream/main
    """Function wraps the creation of a new Flask object, and returns it after it's
        loaded up with configuration settings
    """
    app = Flask(__name__)
    app_config={
        'development':config.DevelopmentConfig,
        'testing': config.TestingConfig,
        'production' :config.ProductionConfig, 
    }
   
    if config_name not in app_config:
        raise KeyError(f"Configuration '{config_name}' is not a valid configuration name.")
    
    app.config.from_object(app_config[config_name])
    
    if __name__ == "__main__":
        config_name = os.getenv('FLASK_CONFIG', 'development')
    CORS(app)    
     
    db.app = app
    db.init_app(app)
    # manager = Manager(app)
    migrate = Migrate(app, db)
    mail.init_app(app)
    ma = Marshmallow(app)
    swagger = Swagger(app)
    jwt = JWTManager(app)
    
    from app.auth.routes import auth 
    app.register_blueprint(auth)
<<<<<<< HEAD

    from app.admin.routes import admin_blueprint
    from app.Flights.routes.flights import flights_blueprint
    from app.Flights.routes.airplane import airplane_blueprint
    from app.Flights.routes.airport import airport_blueprint

    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(flights_blueprint, url_prefix='/api/flights')
    app.register_blueprint(airplane_blueprint, url_prefix='/api/airplane')
    app.register_blueprint(airport_blueprint, url_prefix='/api/airport')
    
=======
    
    from app.Flights.routes.flights import flights_blueprint
    from app.Flights.routes.airplane import airplane_blueprint
    from app.Flights.routes.airport import airport_blueprint
    
    app.register_blueprint(flights_blueprint, url_prefix='/api/flights')
    app.register_blueprint(airplane_blueprint, url_prefix='/api/airplane')
    app.register_blueprint(airport_blueprint, url_prefix='/api/airport')

>>>>>>> upstream/main
    from app.helpers.send_email import background_scheduler

    background_scheduler()

    @app.route('/')
    def index():
        return jsonify({"message":
           ("Welcome to SkyHigh Flights API,"
            "This is a Flask API that provides User Authentication,"
            "Flight Search, Flight Booking and Email Notifications") }),200
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return jsonify({"errors": messages})
        else:
            return jsonify({"errors":messages})

    return app