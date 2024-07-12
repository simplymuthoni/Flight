from flask import Blueprint, request, jsonify
from app.Flights.models import Flight, Airplane, Airport
from app import db
from app.schemas import FlightSchema
from datetime import datetime
from flasgger import Swagger, swag_from

flights_schema = FlightSchema(many=True)

flights_blueprint = Blueprint('flights', __name__)

@flights_blueprint.route('/flights', methods=['GET'])
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

@flights_blueprint.route('/filter', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'A list of flights',
            'examples': {
                'application/json': [
                    {
                        'flight_id': 1,
                        'flight_number': 123,
                        'departure_airport': 'JFK',
                        'departure_airport_name': 'John F. Kennedy International Airport',
                        'departure_city': 'New York',
                        'departure_country': 'USA',
                        'arrival_airport': 'LAX',
                        'arrival_airport_name': 'Los Angeles International Airport',
                        'arrival_city': 'Los Angeles',
                        'arrival_country': 'USA',
                        'departure_date_time': '2024-07-09T12:00:00',
                        'arrival_date_time': '2024-07-09T15:00:00',
                        'capacity': 200,
                        'price': 300.0,
                        'airplane_id': 5
                    }
                ]
            }
        },
        400: {
            'description': 'Error occurred',
            'examples': {
                'application/json': {
                    'error': 'Error message'
                }
            }
        }},
    'parameters': [
        {
            'name': 'departure_city',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'City of departure'
        },
        {
            'name': 'arrival_city',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'City of arrival'
        }
    ]})
def filter_flights():
    try:
        # Fetch query parameters
        departure_city = request.args.get('departure_city')
        arrival_city = request.args.get('arrival_city')

        # Aliases for the Airport table
        departure_alias = db.aliased(Airport)
        arrival_alias = db.aliased(Airport)

        # Build the query
        query = db.session.query(
            Flight.FlightID,
            Flight.Flight_Number,
            Flight.Departure_Airport,
            departure_alias.airport_name.label('departure_airport_name'),
            departure_alias.city.label('departure_city'),
            departure_alias.country.label('departure_country'),
            Flight.Arrival_Airport,
            arrival_alias.airport_name.label('arrival_airport_name'),
            arrival_alias.city.label('arrival_city'),
            arrival_alias.country.label('arrival_country'),
            Flight.Departure_Date_time,
            Flight.Arrival_Date_time,
            Flight.Capacity,
            Flight.Price,
            Flight.AirPlaneID
        ).join(
            departure_alias, departure_alias.airport_name == Flight.Departure_Airport
        ).join(
            arrival_alias, arrival_alias.airport_name == Flight.Arrival_Airport
        )

        # Apply filters if provided
        if departure_city:
            query = query.filter(departure_alias.city == departure_city)
        if arrival_city:
            query = query.filter(arrival_alias.city == arrival_city)

        # Execute the query and get the results
        flights = query.all()
        
         # Prepare the response
        flights_data = [{
            'flight_id': flight.FlightID,
            'flight_number': flight.Flight_Number,
            'departure_airport': flight.Departure_Airport,
            'departure_airport_name': flight.departure_airport_name,
            'departure_city': flight.departure_city,
            'departure_country': flight.departure_country,
            'arrival_airport': flight.Arrival_Airport,
            'arrival_airport_name': flight.arrival_airport_name,
            'arrival_city': flight.arrival_city,
            'arrival_country': flight.arrival_country,
            'departure_date_time': flight.Departure_Date_time.isoformat(),  # Format datetime as ISO string
            'arrival_date_time': flight.Arrival_Date_time.isoformat(),      # Format datetime as ISO string
            'capacity': flight.Capacity,
            'price': float(flight.Price),  # Convert price to float for JSON serialization
            'airplane_id': flight.AirPlaneID
        }for flight in flights]
        return jsonify(flights_data), 200
  
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# Register Blueprints
flights_blueprint.add_url_rule('/filter', view_func=filter_flights, methods=['GET'])
flights_blueprint.add_url_rule('/flights', view_func=get_flights, methods=['GET'])
