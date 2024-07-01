from flask import Flask, Blueprint, request, jsonify
from app.schemas import AdminSchema
from app import db
from app.admin.models import Admin

app = Flask(__name__)
admin_bp = Blueprint('admin', __name__)

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

@app.route('/register', methods=['POST'])
def create_admin():
    """Creates the admin user."""
    try:
        db.session.add(Admin(
            email= "collotoo254@gmail.com",
            name= "collins too",
            password="Kipkemoitoo254#2024",
            )
        )
        db.session.commit()
        print('Admin user created successfully.')
    except Exception as e:
        print('Failed to create admin user: ' + str(e))

@app.route('/login', methods=['POST'])
def login_admin():

    """Logins the Specified admin user"""

    data = request.get_json()
    if not data:
        return jsonify({"error":"Invalid input"}), 400
    
    email =data.get('email')
    password =data.get('password')

    if not email or not password:
        return jsonify({"error":"Missing required fields"}),400
    
    admin = admin.query.filter(admin.email ==email)

    if admin is None or not admin.check_password(password):
        return jsonify({"error": "Invalid email or password"}),400
    
    return jsonify({"message": "Login successful", "admin": admin.to_dict()}),200


if __name__ == '__main__':
    app.run()
