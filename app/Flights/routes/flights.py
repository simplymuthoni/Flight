from flask import Blueprint, request, jsonify, Flask
from app.Flights.models import Flight, Airplane
from app import db
from app.schemas import FlightSchema
from datetime import datetime

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)

flights_blueprint = Blueprint('flights', __name__)

@flights_blueprint.route('/flights', methods=['GET'])
def get_flights():
    flights = Flight.query.all()
    flights_dict_list = [Flight.to_dict() for Flight in flights]
    return jsonify(flights_dict_list), 200

@flights_blueprint.route('/create', methods=['POST'])
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
    
    departure_date_time=datetime.strptime(departure_date, '%Y-%m-%dT%H:%M:%S')
    arrival_date_time=datetime.strptime(arrival_date, '%Y-%m-%dT%H:%M:%S')

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
    
@flights_blueprint.route('/update/<int:flight_id>', methods=['PATCH'])
def update_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({'message': 'Flight not found'}), 404

    data = request.get_json()
    flight.Departure_Date_time = data.get('Departure_Date_time', flight.Departure_Date_time)
    flight.Departure_Airport = data.get('Departure_Airport', flight.Departure_Airport)
    flight.Arrival_Date_time = data.get('Arrival_Date_time', flight.Arrival_Date_time)
    flight.Arrival_Airport = data.get('Arrival_Airport', flight.Arrival_Airport)
    flight.Flight_Number = data.get('Flight_Number', flight.Flight_Number)
    flight.Capacity = data.get('Capacity', flight.Capacity)
    flight.Price = data.get('Price', flight.Price)
    flight.AirPlaneID = data.get('AirPlaneID', flight.AirPlaneID)

    db.session.commit()

    return jsonify({'message': 'Flight updated successfully', 'flight': flight.serialize()}), 200
    
@flights_blueprint.route('/delete/<int:flight_id>', methods=['DELETE'])
def delete_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({'message': 'Flight not found'}), 404

    db.session.delete(flight)
    db.session.commit()

    return jsonify({'message': 'Flight deleted successfully'}), 200
    
flights_blueprint.add_url_rule('/flights', view_func=get_flights, methods=['GET'])
flights_blueprint.add_url_rule('/create', view_func=create_flight,methods=['POST'])
flights_blueprint.add_url_rule('/update', view_func=update_flight, methods=['PATCH'])
flights_blueprint.add_url_rule('/delete', view_func=delete_flight, methods=['DELETE'])
