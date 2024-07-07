from flask import Flask, request, jsonify, Blueprint, session
from flasgger import Swagger
from app.auth.models import User
from app.schemas import UserSchema
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session

app = Flask(__name__)
swagger = Swagger(app)

# Initialize Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'supersecretkey'
Session(app)

auth = Blueprint('auth', __name__, url_prefix='/api/auth')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@auth.route('/register', methods=['POST'])
def add_user():
    """
    Register a new user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: User
          required:
            - username
            - name
            - password
            - email
            - phone_number
            - address
          properties:
            username:
              type: string
            name:
              type: string
            password:
              type: string
            email:
              type: string
            phone_number:
              type: string
            address:
              type: string
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid input or missing required fields
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    username = data.get('username')
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')
    phone_number = data.get('phone_number')
    address = data.get('address')

    if not all([username, name, password, email, phone_number, address]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "Username already taken"}), 400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)
    user = User(
        username=username,
        name=name,
        email=email,
        phone_number=phone_number,
        address=address,
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Login
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      400:
        description: Invalid input or missing required fields
      401:
        description: Unauthorized
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(email=email).first()

    if user is None or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 400

    session['user_id'] = user.id
    session['user_email'] = user.email

    return jsonify({"message": "Login successful", "user": user.to_dict()}), 200

@auth.route('/logout', methods=['POST'])
def logout():
    """
    User logout
    ---
    responses:
      200:
        description: Logout successful
    """
    session.pop('user_id', None)
    session.pop('user_email', None)
    return jsonify({"message": "Logout successful"}), 200

@auth.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            $ref: '#/definitions/User'
    """
    users = User.query.all()
    users_dict_list = [user.to_dict() for user in users]
    return jsonify(users_dict_list), 200

@auth.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update user
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The user ID
      - name: body
        in: body
        required: true
        schema:
          id: User
          properties:
            username:
              type: string
            name:
              type: string
            password:
              type: string
            email:
              type: string
            phone_number:
              type: string
            address:
              type: string
    responses:
      200:
        description: User updated successfully
      400:
        description: Invalid input or missing required fields
      404:
        description: User not found
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    username = data.get('username')
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')
    phone_number = data.get('phone_number')
    address = data.get('address')

    if username:
        if User.query.filter_by(username=username).first() and User.query.filter_by(username=username).first().id != user_id:
            return jsonify({"error": "Username already taken"}), 400
        user.username = username

    if email:
        if User.query.filter_by(email=email).first() and User.query.filter_by(email=email).first().id != user_id:
            return jsonify({"error": "Email already registered"}), 400
        user.email = email

    if name:
        user.name = name

    if password:
        user.set_password(password)

    if phone_number:
        user.phone_number = phone_number

    if address:
        user.address = address

    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

@auth.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete user
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The user ID
    responses:
      200:
        description: User deleted successfully
      404:
        description: User not found
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

# Register Blueprint
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)
