from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    
    UserID = fields.Int(dump_only=True)
    Name = fields.Str(required=True)
    Username = fields.Str(required=True)
    Password = fields.Str(required=True)
    Email = fields.Str(required=True)
    Phone_Number = fields.Str(required=True)
    Address = fields.Str(required=True)
    
class AirportSchema(Schema):
    
    AirportID = fields.Int(dump_only=True)
    Airport_Name = fields.Str(required=True)
    City = fields.Str(required=True)
    Country = fields.Str(required=True)
    
class AirplaneSchema(Schema):
    
    AirplaneID = fields.Int(dump_only=True)
    registration_number = fields.Str(required=True)
    total_seats= fields.Int(required=True)
    economy_seats = fields.Int(required=True)
    business_seats = fields.Int(required=True)
    first_class_seats = fields.Int(required=True)
    
class FlightSchema(Schema):
   
    FlightsID = fields.Int(dump_only=True)
    Flight_Number = fields.Str(required=True)
    Departure_Airport = fields.Str(required=True)
    Arrival_Airport = fields.Str(required=True)
    Departure_Date_Time = fields.DateTime(required=True)
    Arrival_Date_Time = fields.DateTime(required=True)
    Capacity= fields.Int(required=True)
    Price =fields.Float(required=True)

class AdminSchema(Schema):
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    password= fields.Str(required=True)
    

user_schema = UserSchema()
users_schema = UserSchema(many=True) 

airport_schema =AirportSchema()
aiports_schema = AirportSchema(many=True)

airplane_schema =AirplaneSchema()
airplanes_schema =AirplaneSchema(many=True)

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)



