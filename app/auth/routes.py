from flask import request, jsonify, Blueprint, Flask
from app.auth.models import User
from app.schemas import UserSchema
from app import db

app = Flask(__name__)

auth = Blueprint('auth', __name__, url_prefix='/api')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Route to register a user

@app.route('/register', methods=['POST'])
def add_user():
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

    # Check if the user already exists
    if User.query.filter_by(username=username) is not None:
        return jsonify({"error": "Username already taken"}), 400
    if User.query.filter_by(email=email) is not None:
        return jsonify({"error": "Email already registered"}), 400

    user = User(
        username=username,
        name=name,
        email=email,
        phone_number=phone_number,
        address=address,
        password= password
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(email=email).first()

    # if not user or not user.check_password(password):
    #     return jsonify({"error": "Invalid email or password"}), 400

    return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
@app.route('/users', methods=['GET'])
def get_users():
    # users = User.query.all()
    # # result = users_schema.dump(users)
    # return jsonify(users.to_dict()), 200
    users = User.query.all()
    users_dict_list = [user.to_dict() for user in users]
    return jsonify(users_dict_list), 200

@app.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
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
        if User.query.filter_by(username=username) and User.query.filter_by(username=username).id != user_id:
            return jsonify({"error": "Username already taken"}), 400
        user.username = username

    if email:
        if User.query.filter_by(email=email) and User.query.filter_by(email=email).id != user_id:
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

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(user_id):
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