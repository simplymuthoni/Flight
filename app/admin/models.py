from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = 'admin'
    
    adminid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        # self.set_password(password) 
        self.password = password   

    def to_dict(self):
        return {
            "adminid": self.adminid,
            "email": self.email,
            "name": self.name,
            # "password": self.password_hash
            "password": self.password
        }