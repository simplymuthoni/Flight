from werkzeug.security import generate_password_hash
from app import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, email, name, password, is_admin=False, confirmed=False):
        self.email = email
        self.name = name
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
        self.confirmed = confirmed
        
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'is_admin': self.is_admin,
            'confirmed': self.confirmed
        }
