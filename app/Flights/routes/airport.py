from flask import Flask, jsonify, request, Blueprint
from app.Flights.models import Airport
from app import db
from app.schemas import AirportSchema
<<<<<<< HEAD
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

airport_blueprint = Blueprint('airport', __name__)

airport_schema = AirportSchema()
airports_schema = AirportSchema(many=True)

@airport_blueprint.route('/create', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Airport',
                'required': ['airport_name', 'city', 'country'],
                'properties': {
                    'airport_name': {'type': 'string'},
                    'city': {'type': 'string'},
                    'country': {'type': 'string'},
                },
            },
        },
    ],
    'responses': {
        '201': {'description': 'Airport created successfully'},
        '400': {'description': 'Missing required fields'},
    },
})
def create_airport():
    data = request.get_json()
    airport_name = data.get('airport_name')
    city = data.get('city')
    country = data.get('country')

    if not all([airport_name, city, country]):
        return jsonify({"error": "Missing required fields"}), 400

    airport = Airport(airport_name=airport_name, city=city, country=country)
    db.session.add(airport)
    db.session.commit()
    return jsonify({"message": "Airport created successfully"}), 201

@airport_blueprint.route('/airports', methods=['GET'])
@swag_from({
    'responses': {
        '200': {
            'description': 'A list of airports',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/Airport'
                },
            },
        },
    },
})
=======

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
>>>>>>> upstream/main
def get_airports():
    airports = Airport.query.all()
    airports_dict_list = [airport.to_dict() for airport in airports]
    return jsonify(airports_dict_list), 200

@airport_blueprint.route('/delete/<int:airport_id>', methods=['DELETE'])
<<<<<<< HEAD
@swag_from({
    'parameters': [
        {
            'name': 'airport_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The airport ID'
        },
    ],
    'responses': {
        '200': {'description': 'Airport deleted successfully'},
        '404': {'description': 'Airport not found'},
        '500': {'description': 'Internal server error'}
    },
})
=======
>>>>>>> upstream/main
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
<<<<<<< HEAD

# Register Blueprints
=======
 
 
>>>>>>> upstream/main
airport_blueprint.add_url_rule('/airports', view_func=get_airports, methods=['GET'])
airport_blueprint.add_url_rule('/create', view_func=create_airport, methods=['POST'])
# airport_blueprint.add_url_rule('/update', view_func=update_airport, methods=['PATCH'])
airport_blueprint.add_url_rule('/delete', view_func=delete_airport, methods=['DELETE'])
<<<<<<< HEAD
if __name__ == '__main__':
    app.run(debug=True)
=======

>>>>>>> upstream/main
