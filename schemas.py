from marshmallow import Schema, fields, validate

class FlightSchema(Schema):
    """
    A schema for validating flight data.
    """
    FlightsID = fields.Int(dump_only=True)
    Flight_Number = fields.Int(required =True)
    Departure_Airport = fields.Str(required =True)
    Arrival_Aiport = fields.Str(required=True)
    Departure_Date_Time = fields.DateTime(required=True)
    Arrival_Date_Time = fields.DateTime(required=True)
    Capacity = fields.Int(required=True)
    price = fields.Float(required=True)

class BookingSchema(Schema):
    """
    A schema for validating booking data.
    """
    BookingID = fields.Int(dump_only=True)
    UserID = fields.Int(required=True)
    FlightID = fields.Int(required=True)
    Booking_Date_time = fields.DateTime(required=True)
    Seat_Number = fields.Str(required=True)
    status = fields.Str(required=True)

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)