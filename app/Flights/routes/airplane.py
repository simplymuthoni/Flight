from flask import Blueprint, request, jsonify, Flask
from app.Flights.models import Airplane
from app import db
from app.schemas import AirplaneSchema
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

airplane_schema =AirplaneSchema()
airplanes_schema =AirplaneSchema(many=True)

airplane_blueprint = Blueprint('airplane', __name__)

@airplane_blueprint.route('/create', methods=['POST'])
def create_airplane():
    """
    Create a new airplane
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Airplane
          required:
            - registration_number
            - total_seats
            - economy_seats
            - business_seats
            - first_class_seats
          properties:
            registration_number:
              type: string
            total_seats:
              type: integer
            economy_seats:
              type: integer
            business_seats:
              type: integer
            first_class_seats:
              type: integer
    responses:
      201:
        description: Airplane created successfully
      400:
        description: Invalid input or missing required fields
    """
    data = request.get_json()
    registration_number = data.get('registration_number')
    total_seats = data.get('total_seats')
    economy_seats = data.get('economy_seats')
    business_seats = data.get('business_seats')
    first_class_seats = data.get('first_class_seats')
    if not registration_number or not total_seats or not economy_seats or not business_seats or not first_class_seats:
        return jsonify({"error": "missing required fields"}), 400
    airplane = Airplane(
        registration_number=registration_number,
        total_seats=total_seats,
        economy_seats=economy_seats,
        business_seats=business_seats,
        first_class_seats=first_class_seats
    )
    db.session.add(airplane)
    db.session.commit()
    return jsonify({"message": "Airplane created successfully"}), 201

@airplane_blueprint.route('/airplanes', methods=['GET'])
def get_airplanes():
    """
    Get all airplanes
    ---
    responses:
      200:
        description: A list of airplanes
        schema:
          type: array
          items:
            $ref: '#/definitions/Airplane'
    """
    airplanes = Airplane.query.all()
    airplanes_dict_list = [airplane.to_dict() for airplane in airplanes]
    return jsonify(airplanes_dict_list), 200

@airplane_blueprint.route('/update/<int:id>', methods=['PATCH'])
def update_airplane(airplane_id):
    """
    Update airplane
    ---
    parameters:
      - name: airplane_id
        in: path
        type: integer
        required: true
        description: The airplane ID
      - name: body
        in: body
        required: true
        schema:
          id: Airplane
          properties:
            registration_number:
              type: string
            total_seats:
              type: integer
            economy_seats:
              type: integer
            business_seats:
              type: integer
            first_class_seats:
              type: integer
    responses:
      200:
        description: Airplane updated successfully
      400:
        description: Invalid input or missing required fields
      404:
        description: Airplane not found
    """
    airplane = Airplane.query.get(airplane_id)
    if not airplane:
        return jsonify({'message': 'Airplane not found'}), 404
    data = request.get_json()
    airplane.registration_number = data.get('registration_number', airplane.registration_number)
    airplane.total_seats = data.get('total_seats', airplane.total_seats)
    airplane.economy_seats = data.get('economy_seats', airplane.economy_seats)
    airplane.business_seats = data.get('business_seats', airplane.business_seats)
    airplane.first_class_seats = data.get('first_class_seats', airplane.first_class_seats)
    db.session.commit()
    return jsonify({'message': 'Airplane updated successfully', 'airplane': airplane.to_dict()}), 200

@airplane_blueprint.route('/airplane/<int:airplane_id>/seats', methods=['GET'])
def get_seat_arrangement(airplane_id):
    """
    Get seat arrangement for an airplane
    ---
    parameters:
      - name: airplane_id
        in: path
        type: integer
        required: true
        description: The airplane ID
    responses:
      200:
        description: A list of seats
        schema:
          type: array
          items:
            properties:
              seat_number:
                type: integer
              seat_class:
                type: string
              available:
                type: boolean
      404:
        description: Airplane not found
    """
    airplane = Airplane.query.get(airplane_id)
    if not airplane:
        return jsonify({'message': 'Airplane not found'}), 404
    seats = airplane.generate_seat_arrangement()
    return jsonify(seats), 200

@airplane_blueprint.route('/delete/<int:airplane_id>', methods=['DELETE'])
def delete_airplane(airplane_id):
    """
    Delete an airplane
    ---
    parameters:
      - name: airplane_id
        in: path
        type: integer
        required: true
        description: The airplane ID
    responses:
      200:
        description: Airplane deleted successfully
      404:
        description: Airplane not found
      500:
        description: Internal server error
    """
    airplane = Airplane.query.get(airplane_id)
    if not airplane:
        return jsonify({'message': 'Airplane not found'}), 404
    try:
        db.session.delete(airplane)
        db.session.commit()
        return jsonify({'message': 'Airplane deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Register Blueprints
airplane_blueprint.add_url_rule('/airplanes', view_func=get_airplanes, methods=['GET'])   
airplane_blueprint.add_url_rule('/create', view_func=create_airplane, methods=['POST'])
airplane_blueprint.add_url_rule('/update', view_func=update_airplane, methods=['PATCH'])
airplane_blueprint.add_url_rule('/delete/<int:airplane_id>', view_func=delete_airplane, methods=['DELETE'])
airplane_blueprint.add_url_rule('/airplane/<int:airplane_id>/seats', view_func=get_seat_arrangement, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
