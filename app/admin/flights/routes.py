from flask import Blueprint, request, jsonify
from app.Flights.models import Flight, Airplane
from app import db
from app.schemas import FlightSchema
from datetime import datetime
from flasgger import Swagger, swag_from

flights_schema = FlightSchema(many=True)

wing_blueprint = Blueprint('wings', __name__)

@wing_blueprint.route('/create', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Flight',
                'required': ['flight_number', 'departure_airport', 'arrival_airport', 'departure_date_time', 'arrival_date_time', 'airplane_id', 'capacity', 'price'],
                'properties': {
                    'flight_number': {'type': 'string'},
                    'departure_airport': {'type': 'string'},
                    'arrival_airport': {'type': 'string'},
                    'departure_date_time': {'type': 'string', 'format': 'date-time'},
                    'arrival_date_time': {'type': 'string', 'format': 'date-time'},
                    'airplane_id': {'type': 'integer'},
                    'capacity': {'type': 'integer'},
                    'price': {'type': 'number'},
                },
            },
        },
    ],
    'responses': {
        '201': {'description': 'Flight created successfully'},
        '400': {'description': 'Missing required fields or incorrect format'},
        '404': {'description': 'Airplane not found'}
    },
})
def create_flight():
    data = request.get_json()

    flight_number = data.get('flight_number')
    departure_airport = data.get('departure_airport')
    arrival_airport = data.get('arrival_airport')
    departure_date = data.get('departure_date_time')
    arrival_date = data.get('arrival_date_time')
    airplane_id = data.get('airplane_id')
    capacity = data.get('capacity')
    price = data.get('price')
    
    try:
        departure_date_time = datetime.strptime(departure_date, '%Y-%m-%dT%H:%M:%S')
        arrival_date_time = datetime.strptime(arrival_date, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return jsonify({"error": "Incorrect datetime format. Use ISO 8601 format: YYYY-MM-DDTHH:MM:SS"}), 400

    # Check if all required fields are provided
    if not all([flight_number, departure_airport, arrival_airport, departure_date_time, arrival_date_time, airplane_id, capacity, price]):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if departure and arrival airports are different
    if departure_airport == arrival_airport:
        return jsonify({"error": "Departure and arrival airports must be different"}), 400

    # Check if the airplane exists
    airplane = Airplane.query.get(airplane_id)
    if not airplane:
        return jsonify({"error": "Airplane not found"}), 404

    # Create the flight object
    flight = Flight(
        Flight_Number=flight_number,
        Departure_Airport=departure_airport,
        Arrival_Airport=arrival_airport,
        Departure_Date_Time=departure_date_time,
        Arrival_Date_Time=arrival_date_time,
        AirplaneID=airplane_id,
        Capacity=capacity,
        Price=price
    )

    try:
        db.session.add(flight)
        db.session.commit()
        return jsonify({"message": "Flight created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@wing_blueprint.route('/update/<int:flight_id>', methods=['PATCH'])
@swag_from({
    'parameters': [
        {
            'name': 'flight_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the flight to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Flight',
                'properties': {
                    'flight_number': {'type': 'string'},
                    'departure_airport': {'type': 'string'},
                    'arrival_airport': {'type': 'string'},
                    'departure_date_time': {'type': 'string', 'format': 'date-time'},
                    'arrival_date_time': {'type': 'string', 'format': 'date-time'},
                    'airplane_id': {'type': 'integer'},
                    'capacity': {'type': 'integer'},
                    'price': {'type': 'number'},
                },
            },
        },
    ],
    'responses': {
        '200': {'description': 'Flight updated successfully'},
        '400': {'description': 'Invalid request'},
        '404': {'description': 'Flight not found'}
    },
})
def update_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({'message': 'Flight not found'}), 404

    data = request.get_json()
    try:
        departure_date_time = datetime.strptime(data.get('departure_date_time'), '%Y-%m-%dT%H:%M:%S') if data.get('departure_date_time') else flight.departure_date_time
        arrival_date_time = datetime.strptime(data.get('arrival_date_time'), '%Y-%m-%dT%H:%M:%S') if data.get('arrival_date_time') else flight.arrival_date_time
    except ValueError:
        return jsonify({"error": "Incorrect datetime format. Use ISO 8601 format: YYYY-MM-DDTHH:MM:SS"}), 400

    flight.flight_number = data.get('flight_number', flight.flight_number)
    flight.departure_airport = data.get('departure_airport', flight.departure_airport)
    flight.arrival_airport = data.get('arrival_airport', flight.arrival_airport)
    flight.departure_date_time = departure_date_time
    flight.arrival_date_time = arrival_date_time
    flight.airplane_id = data.get('airplane_id', flight.airplane_id)
    flight.capacity = data.get('capacity', flight.capacity)
    flight.price = data.get('price', flight.price)

    db.session.commit()

    return jsonify({'message': 'Flight updated successfully', 'flight': flight.to_dict()}), 200

@wing_blueprint.route('/delete/<int:flight_id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'flight_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the flight to delete'
        },
    ],
    'responses': {
        '200': {'description': 'Flight deleted successfully'},
        '404': {'description': 'Flight not found'}
    },
})
def delete_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({'message': 'Flight not found'}), 404

    db.session.delete(flight)
    db.session.commit()

    return jsonify({'message': 'Flight deleted successfully'}), 200

@wing_blueprint.route('/flights', methods=['GET'])
@swag_from({
    'responses': {
        '200': {
            'description': 'List of flights',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/Flight'
                },
            },
        },
    },
})
def get_flights():
    flights = Flight.query.all()
    flights_dict_list = [flight.to_dict() for flight in flights]
    return jsonify(flights_dict_list), 200

wing_blueprint.add_url_rule('/create', view_func=create_flight, methods=['POST'])
wing_blueprint.add_url_rule('/update/<int:flight_id>', view_func=update_flight, methods=['PATCH'])
wing_blueprint.add_url_rule('/delete/<int:flight_id>', view_func=delete_flight, methods=['DELETE'])
wing_blueprint.add_url_rule('/flights', view_func=get_flights, methods=['GET'])
