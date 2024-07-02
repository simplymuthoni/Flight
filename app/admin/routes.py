from flask import Flask, Blueprint, request, jsonify
from app.schemas import AdminSchema
from app import db
from app.admin.models import Admin

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/register', methods=['POST'])
def register_admin():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    if not all([email, name, password]):
        return jsonify({"error": "Missing required fields"}),400

    # Check if admin with this email already exists
    if Admin.query.filter_by(email=email)is not None:
        return jsonify({"error": "Email already registered"}), 400
    
    if Admin.query.filter_by(name=name) is not None:
        return jsonify({"error":"Name already registered"})

    admin = Admin(
        email=email, 
        name=name, 
        password=password
        )
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()

    return jsonify({"message": "Admin registered successfully", "admin": admin.to_dict()}), 201

@admin_blueprint.route('/login', methods=['POST'])
def login_admin():
    """Logins the specified admin user"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400
    
    admin = Admin.query.filter_by(email=email).first()

    if admin is None or not admin.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 400
    
    return jsonify({"message": "Login successful", "admin": admin.to_dict()}), 200

