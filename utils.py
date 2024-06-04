import os
from datetime import datetime, timedelta
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from Flights.models import Flight, Booking
from app import db
from app import models
import jwt

def validate_flight_data(data):
    
    required_fields = ['flight_number', 'departure_city', 'arrival_city', 'departure_time', 'arrival_time', 'price', 'seats']
    for field in required_fields:
        if field not in data:
            return False, "Missing required field: {field}"
    try:
        datetime.datetime.strptime(data['departure_time'], '%Y-%m-%d %H:%M:%S')
        datetime.datetime.strptime(data['arrival_time'], '%Y-%m-%d %H:%M:%S')
        float(data['price'])
        int(data['seats'])
    except ValueError:
        return False, "Invalid data format"
    return True, ""

def validate_booking_data(data):
    """
    Validate booking data
    """
    required_fields = ['flight_id', 'num_seats', 'total_price', 'customer_name', 'customer_email', 'booking_time']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    try:
        int(data['flight_id'])
        int(data['num_seats'])
    except ValueError:
        return False, "Invalid data format"
    return True, ""

def get_flight(flight_id):
    """
    Get a flight by ID
    """
    flight = Flight.query.get(flight_id)
    if flight is None:
        return jsonify({"error": "Flight not found"}), 404
    return flight

def get_bookings(flight_id):
    """
    Get bookings for a flight
    """
    bookings = Booking.query.filter_by(flight_id=flight_id).all()
    return bookings

def create_booking(data):
    """
    Create a new booking
    """
    flight_id = data['flight_id']
    num_seats = data['num_seats']
    customer_name = data['customer_name']
    customer_email = data['customer_email']
    flight = get_flight(flight_id)
    if flight is None:
        return jsonify({"error": "Flight not found"}), 404
    if num_seats > flight.seats:
        return jsonify({"error": "Not enough seats available"}), 400
    booking = Booking(flight_id=flight_id, num_seats=num_seats, customer_name=customer_name, customer_email=customer_email)
    db.session.add(booking)
    db.session.commit()
    return jsonify({"message": "Booking created successfully"}), 201

def cancel_booking(booking_id):
    """
    Cancel a booking
    """
    booking = Booking.query.get(booking_id)
    if booking is None:
        return jsonify({"error": "Booking not found"}), 404
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking cancelled successfully"}), 200

def generate_password(password):
    return generate_password_hash(password, method=current_app.config['PASSWORD_HASH_METHOD'])

def check_password(password, hashed_password):
    return check_password_hash(hashed_password, password)

def generate_token():
    import secrets
    return secrets.token_hex(16)

def handle_exceptions(default_response_msg):
    def exception_handler_decorator(func):
        def decorated_function(*args, **kwargs):
            try:
                # Call the original function
                return func(*args, **kwargs)
            except Exception as error:
                # Handle the exception and provide the default response
                print(f"Exception occurred: {error}")
                return default_response_msg
        return decorated_function
    return exception_handler_decorator

def log_arguments_and_return_value(original_function):
    def wrapper(*args, **kwargs):
        print(f"Calling {original_function.__name__} with args: {args}, kwargs: {kwargs}")

        # Call the original function
        result = original_function(*args, **kwargs)

        # Log the return value
        print(f"{original_function.__name__} returned: {result}")

        # Return the result
        return result
    return wrapper

def convert_return_value_to_type(target_type):
    def decorator(func):
        def type_converter_decorator(*args, **kwargs):
            # Call the original function
            result = func(*args, **kwargs)

            # Convert the return value to the target type
            return target_type(result)
        return type_converter_decorator
    return decorator

def enforce_type_checking(function):
    def type_checked_wrapper(*args, **kwargs):
        # Get the function parameters
        function_parameters = function.__annotations__

        # Check the types of the positional arguments
        for i, arg in enumerate(args):
            parameter_type = function_parameters[i].annotation
            if not isinstance(arg, parameter_type):
                raise TypeError(f"Argument {i} must be of type {parameter_type.__name__}")

        # Iterate over the keyword arguments
        for keyword_name, arg_value in kwargs.items():
            parameter_type = function_parameters[keyword_name].annotation
            if not isinstance(arg_value, parameter_type):
                raise TypeError(f"Argument '{keyword_name}' must be of type '{parameter_type.__name__}'")

        # Call the original function
        return function (*args, **kwargs)

    return type_checked_wrapper
def get_formatted_date(date: datetime) -> str:
    """
    Format a datetime object as a string.
    """
    return date.strftime('%Y-%m-%d')

def get_flight_duration(departure_time: datetime, arrival_time: datetime) -> str:
    
    def search_flights(query_parameters):
    # implement search logic here
    # return a list of flight objects that match the search criteria#
    pass

def filter_flights(query_parameters, flights):
    # implement filter logic here
    # return a list of flight objects that match the filter criteria
    pass

def get_flight_details(flight_id):
    # implement logic to retrieve flight details
    # return a flight object with details
    pass

def get_airport_code(airport_name):
    # implement logic to retrieve airport code
    # return the airport code
    pass

def get_airline_code(airline_name):
    # implement logic to retrieve airline code
    # return the airline code
    pass

def encode_token(user):
    """
    Encode user payload as a JWT
    :param user:
    :return:
    """
    payload = {"name": user}
    encoded_data = jwt.encode(payload=payload, key= os.environ.get('JWT_TOKEN '), algorithm="HS256")
    return encoded_data

def decode_token(token):

    """
    Decode a JWT token
    :param token:
    :return:
    """
    try:

        payload = jwt.decode(token=token, key='we_outside', algorithms=["HS256"])

        return payload

    except jwt.ExpiredSignatureError as error:

        print(f'Unable to decode the token, error: {error}')

        return None

    except jwt.InvalidTokenError as error:

        print(f'Unable to decode the token, error: {error}')

        return None
if __name__ == "__main__":

    encoded_token = encode_token(user="")

    print(f"Encoded token: {encoded_token}")


    decoded_token = decode_token(token=encoded_token)

    print(f"Decoded token: {decoded_token}")   