from flask import Flask, Blueprint
from flask_script import Manager
from werkzeug.security import generate_password_hash
from app.schemas import AdminSchema
from app import db
from app.admin.models import Admin
import os

app = Flask(__name__)

admin =  Blueprint('admin', __name__, url_prefix='/api')

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

manager = Manager(app)

@manager.command
def create_admin():
    """Creates the admin user."""
    try:
        db.session.add(Admin(
            email=os.getenv('ADMIN_EMAIL'),
            name=os.getenv('ADMIN_NAME'),
            password=generate_password_hash(os.getenv('ADMIN_PASSWORD')),
            is_admin=True,
            confirmed=True)
        )
        db.session.commit()
        print('Admin user created successfully.')
    except Exception as e:
        print('Failed to create admin user: ' + str(e))

if __name__ == '__main__':
    manager.run()
