import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "mariadb+mariadbconnector://mugo:Demo123@127.0.0.1:3306/tembea"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'flask_session:'

    # JWT Config
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour in seconds
    JWT_REFRESH_TOKEN_EXPIRES=2592000  # 30 days in seconds
    
    #email confog
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Payment Gateway Config
    PESAPAL_CONSUMER_KEY = os.environ.get('PESAPAL_CONSUMER_KEY')
    PESAPAL_CONSUMER_SECRET = os.environ.get('PESAPAL_CONSUMER_SECRET')

    # Logging Config
    LOG_LEVEL = 'DEBUG'
    LOG_FILE = 'flight.log'
    
    #Twilio Credentials
    account_sid = os.environ.get('account_sid')
    auth_token = os.environ.get('auth_token')
    twilio_phone_number = os.environ.get('twilio_phone_number')

class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    USE_RELOADER = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}