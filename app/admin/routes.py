from flask import Blueprint, request, jsonify, session
from app.schemas import AdminSchema
from app import db
from app.admin.models import Admin
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from flasgger import swag_from
from flask_session import Session

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/register', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Admin registered successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    },
                    'admin': {
                        'type': 'object'
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input, Missing required fields'
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {
                        'type': 'string'
                    },
                    'name': {
                        'type': 'string'
                    },
                    'password': {
                        'type': 'string'
                    }
                }
            }
        }
    ]
})
def register_admin():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    logging.debug(f"Received data - Email: {email}, Name: {name}, Password: {password}")

    if not all([email, name, password]):
        return jsonify({"error": "Missing required fields"}), 400

    if Admin.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email exists"}), 400

    if Admin.query.filter_by(name=name).first() is not None:
        return jsonify({"error": "Name already registered"}), 400

    if password is None:
        logging.error("Password is None before hashing")
        return jsonify({"error": "Password cannot be None"}), 400

    hashed_password = generate_password_hash(password)
    logging.debug(f"Hashed Password: {hashed_password}")

    admin = Admin(
        email=email,
        name=name,
        password=hashed_password)

    db.session.add(admin)
    db.session.commit()
    return jsonify({"message": "Admin registered successfully", "admin": admin.to_dict()}), 201

@admin_blueprint.route('/login', methods=['POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    },
                    'admin': {
                        'type': 'object'
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input'
        },
        401: {
            'description': 'Unauthorized'
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {
                        'type': 'string'
                    },
                    'password': {
                        'type': 'string'
                    }
                }
            }
        }
    ]
})
def login_admin():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    admin = Admin.query.filter_by(email=email).first()

    if admin is None or not check_password_hash(admin.password, password):
        return jsonify({"error": "Invalid email or password"}), 400

    session['admin_id'] = admin.id
    session['admin_email'] = admin.email
    return jsonify({"message": "Login successful", "admin": admin.to_dict()}), 200

@admin_blueprint.route('/logout', methods=['POST'])
def logout_admin():
    session.pop('admin_id', None)
    session.pop('admin_email', None)
    return jsonify({"message": "Logged out successfully"}), 200

@admin_blueprint.route('/session', methods=['GET'])
def get_session():
    if 'admin_id' in session:
        return jsonify({"admin_id": session['admin_id'], "admin_email": session['admin_email']}), 200
    return jsonify({"error": "No active session"}), 401
