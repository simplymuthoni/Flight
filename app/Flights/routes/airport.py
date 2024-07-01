from flask import Flask, jsonify, request, Blueprint
from app.Flights.models import Airport
from app import db
from app.schemas import AirportSchema

airport_blueprint = Blueprint('airport', __name__)

airport_schema =AirportSchema()
aiports_schema = AirportSchema(many=True)

@airport_blueprint.route('/create', methods=['POST'])
def create_airport():
    data = request.get_json()
        
    airport_name = data.get('airport_name')
    city = data.get('city')
    country = data.get('country')
    
    if not all ([airport_name, city, country]):
        return jsonify({"error": "Missing required fields"}), 400

    airport = Airport(
        airport_name=airport_name, 
        city=city, 
        country=country)
    
    db.session.add(Airport)
    db.session.commit()
    return jsonify({"message": "Airport created successfully"}), 201
   
    
# @airport_blueprint.route('/update/<int:airport_id>', methods=['PATCH'])
# def update_airport(airport_id):
#     airport = Airport.query.get(airport_id)
#     if not airport:
#         return jsonify({'message': 'Airport not found'}), 404

#     data = request.get_json()
    
#     airport_name = data.get('airport_name')
#     city = data.get('city')
#     country = data.get('country')

#     db.session.commit()

#     return jsonify({'message': 'Airport updated successfully', 'airport': airport.serialize()}), 200

@airport_blueprint.route('/airports', methods=['GET'])
def get_airports():
    airports = Airport.query.all()
    airports_dict_list = [airport.to_dict() for airport in airports]
    return jsonify(airports_dict_list), 200

@airport_blueprint.route('/delete/<int:airport_id>', methods=['DELETE'])
def delete_airport(airport_id):
    airport = Airport.query.get(airport_id)
    if not airport:
        return jsonify({"error": "Airport not found"}), 404
    try:
        db.session.delete(airport)
        db.session.commit()
        return jsonify({"message": "Airport deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
 
 
airport_blueprint.add_url_rule('/airports', view_func=get_airports, methods=['GET'])
airport_blueprint.add_url_rule('/create', view_func=create_airport, methods=['POST'])
# airport_blueprint.add_url_rule('/update', view_func=update_airport, methods=['PATCH'])
airport_blueprint.add_url_rule('/delete', view_func=delete_airport, methods=['DELETE'])