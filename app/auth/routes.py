<<<<<<< HEAD
from flask import Flask, request, jsonify, Blueprint
from flasgger import Swagger
=======
from flask import request, jsonify, Blueprint, Flask
>>>>>>> upstream/main
from app.auth.models import User
from app.schemas import UserSchema
from app import db

app = Flask(__name__)
<<<<<<< HEAD
swagger = Swagger(app)
=======
>>>>>>> upstream/main

auth = Blueprint('auth', __name__, url_prefix='/api')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Route to register a user
<<<<<<< HEAD
@app.route('/register', methods=['POST'])
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
=======

@app.route('/register', methods=['POST'])
def add_user():
>>>>>>> upstream/main
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    username = data.get('username')
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')
    phone_number = data.get('phone_number')
    address = data.get('address')
<<<<<<< HEAD

    if not all([username, name, password, email, phone_number, address]):
        return jsonify({"error": "Missing required fields"}), 400

=======
    type = data.get('type')
    

    if not all([username, name, password, email, phone_number, address, type]):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the user already exists
>>>>>>> upstream/main
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "Username already taken"}), 400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email already registered"}), 400

    user = User(
        username=username,
        name=name,
        email=email,
        phone_number=phone_number,
        address=address,
<<<<<<< HEAD
        password=password
=======
        type=type
>>>>>>> upstream/main
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
<<<<<<< HEAD
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

=======
    data = request.get_json()
    
>>>>>>> upstream/main
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

<<<<<<< HEAD
    user = User.query.filter_by(email=email).first()

    # if not user or not user.check_password(password):
    #     return jsonify({"error": "Invalid email or password"}), 400
=======
    user = User.query.filter(User.email == email).first()

    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 400
>>>>>>> upstream/main

    return jsonify({"message": "Login successful", "user": user.to_dict()}), 200

@app.route('/users', methods=['GET'])
def get_users():
<<<<<<< HEAD
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
=======
    # users = User.query.all()
    # # result = users_schema.dump(users)
    # return jsonify(users.to_dict()), 200
>>>>>>> upstream/main
    users = User.query.all()
    users_dict_list = [user.to_dict() for user in users]
    return jsonify(users_dict_list), 200

@app.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
<<<<<<< HEAD
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
=======
>>>>>>> upstream/main
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
<<<<<<< HEAD
=======
    type = data.get('type')
>>>>>>> upstream/main

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

<<<<<<< HEAD
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

@app.route('/delete/<int:user_id>', methods=['DELETE'])
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
=======
    if type:
        user.type = type

    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(user_id):
>>>>>>> upstream/main
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

auth.add_url_rule('/register', view_func=add_user, methods=['POST'])
auth.add_url_rule('/login', view_func=login, methods=['POST'])
auth.add_url_rule('/users', view_func=get_users, methods=['GET'])
auth.add_url_rule('/update', view_func=update_user, methods=['PATCH'])
auth.add_url_rule('/delete', view_func=delete_user, methods=['delete'])

if __name__ == '__main__':
    app.run(debug=True)
<<<<<<< HEAD
=======

>>>>>>> upstream/main
