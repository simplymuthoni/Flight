<<<<<<< HEAD
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(128), nullable=False)  
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200), nullable=False)
=======
from datetime import datetime
from app import db
from app.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker
import scrypt

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(36), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
>>>>>>> upstream/main

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
<<<<<<< HEAD
    def __init__(self, username, name, password, email, phone_number=None, address=None):
        self.username = username
        self.name = name
        # self.set_password(password)
        self.password =  password
        self.email = email
        self.phone_number = phone_number
        self.address = address
        
=======
>>>>>>> upstream/main
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
<<<<<<< HEAD
            "password": self.password
        }
=======
            "type": self.type
        }

   
>>>>>>> upstream/main
