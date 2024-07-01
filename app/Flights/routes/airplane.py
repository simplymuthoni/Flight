from flask import Blueprint, request, jsonify, Flask
from app.Flights.models import Airplane
from app import db
from app.schemas import AirplaneSchema

airplane_schema =AirplaneSchema()
airplanes_schema =AirplaneSchema(many=True)

airplane_blueprint = Blueprint('airplane', __name__)

#Airplane Routes
@airplane_blueprint.route('/create', methods=['POST']) 
def create_airplane():
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
    print("THE AIRPLANE INSTANCE IS ",airplane)
    message = "Success"
    
    return message
    
    # result = airplane_schema.dump(airplane)
    # return jsonify(result), 201
    
@airplane_blueprint.route('/airplanes', methods=['GET'])
def get_airplanes():
    airplanes = Airplane.query.all()
    airplanes_dict_list =[Airplane.to_dict() for Airplane in airplanes]
    return jsonify(airplanes_dict_list),200
    
@airplane_blueprint.route('/update/<int:id>', methods=['PATCH'])
def update_airplane(airplane_id):
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

    return jsonify({'message': 'Airplane updated successfully', 'airplane': airplane.serialize()}), 200

@airplane_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete_airplane(airplane_id):
    airplane = Airplane.query.get(airplane_id)
    if not airplane:
        return jsonify({'message': 'Airplane not found'}), 404

    db.session.delete(airplane)
    db.session.commit()

    return jsonify({'message': 'Airplane deleted successfully'}), 200

airplane_blueprint.add_url_rule('/airplanes', view_func=get_airplanes, methods=['GET'])   
airplane_blueprint.add_url_rule('/create', view_func=create_airplane, methods=['POST'])
airplane_blueprint.add_url_rule('/update', view_func=update_airplane, methods=['PATCH'])
airplane_blueprint.add_url_rule('/delete', view_func=delete_airplane, methods=['DELETE'])