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

users_blueprint = Blueprint('users', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_blueprint.route('/users', methods=['GET'])
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

@users_blueprint.route('/delete/<int:user_id>', methods=['DELETE'])
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

if __name__ == '__main__':
    app.run(debug=True)
