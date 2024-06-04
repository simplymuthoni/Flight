from datetime import datetime
from app import db, login
from base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User(BaseModel):
    
    """This class defines the users table"""
    __tablename__ = 'users'
    
    UserID = db.Column(db.String, primary_key=True, default=lambda:str(uuid.uuid4()))
    Username = db.Column(db.String(64), index=True, unique=True)
    Name = db.Column(db.String)
    password_hash = db.Column(db.String(128))
    Email = db.Column(db.String(120), index=True, unique=True)
    Phone_Number =db.Column(db.String)
    Address = db.Column(db.String)
    Type = db.Column(db.Text)
    
    def __init__(self, email, username, password):
        
        """Initialize the user with
        the user details"""
        self.email = email
        self.username = username
        self.password = generate_password_hash(password).decode()
        

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

