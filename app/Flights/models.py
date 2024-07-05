from app import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Airport(db.Model):
    """This class defines the airports table"""
    
    __tablename__ = 'Airport'
    
    AirportID = db.Column(db.Integer, primary_key=True)
    airport_name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(256), nullable=False)
    country = db.Column(db.String(256), nullable=False)
    
    def __init__(self, airport_name, country, city):
        """Initialize the airport with the airport details"""
        self.airport_name = airport_name
        self.country = country
        self.city = city

    def to_dict(self):
        """Return a dictionary"""
        return {
            'airport_id': self.AirportID,
            'airport_name': self.airport_name,
            'country': self.country,
            'city': self.city
        }
    def __repr__(self):
        return f"Airport(airport_id={self.AirportID}, airport_name='{self.airport_name}', country='{self.country}', city='{self.city}')"


class Airplane(db.Model):
    """This class defines the airplanes table"""
    __tablename__ = 'Airplane'
    
    AirplaneID = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String, nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    economy_seats = db.Column(db.Integer, nullable=False)
    business_seats = db.Column(db.Integer, nullable=False)
    first_class_seats = db.Column(db.Integer, nullable=False)

    def __init__(self, registration_number,total_seats, economy_seats, business_seats,first_class_seats):
        """Initialize the airplane details"""
        self.registration_number = registration_number
        self.total_seats = total_seats
        self.economy_seats = economy_seats
        self.business_seats = business_seats
        self.first_class_seats = first_class_seats
<<<<<<< HEAD
    
    def generate_seat_arrangement(self):
        seats = []
        seat_classes = [
            ('First Class', self.first_class_seats),
            ('Business', self.business_seats),
            ('Economy', self.economy_seats)
        ]
        seat_number = 1
        for seat_class, num_seats in seat_classes:
            for _ in range(num_seats):
                seat = {
                    'seat_number': seat_number,
                    'seat_class': seat_class,
                    'available': True
                }
                seats.append(seat)
                seat_number += 1
        return seats
=======
>>>>>>> upstream/main

    def to_dict(self):
        """Return a dictionary"""
        return {
            'airplane_id': self.AirplaneID,
            'registration_number': self.registration_number,
            'business_seats': self.business_seats,
            'economy_seats': self.economy_seats,
            'first_class_seats': self.first_class_seats,
            'total_seats': self.total_seats
        }

    @staticmethod
    def get_all():
        return Airplane.query.all()

    def __repr__(self):
        return 'Airplane: {}'.format(self.registration_number)


class Flight(db.Model):
    """This class defines the flight schedules table"""
    __tablename__ = 'Flight'
    
    FlightID = db.Column(db.Integer, primary_key=True)
    Flight_Number = db.Column(db.Integer)
    Departure_Airport = db.Column(db.String, nullable=False)
    Arrival_Airport = db.Column(db.String, nullable=False)
    Departure_Date_time =db.Column(db.DateTime)
    Arrival_Date_time = db.Column(db.DateTime)
    Capacity= db.Column(db.Integer)
    Price =db.Column(db.Float)
    AirPlaneID = db.Column(db.Integer, db.ForeignKey('Airplane.AirplaneID'), nullable=False)

    def __init__(self, Departure_Date_Time, Departure_Airport, Arrival_Date_Time,Arrival_Airport, Flight_Number, Capacity, Price, AirplaneID):
        """Initialize the flight details"""
        
        self.Departure_Date_time = Departure_Date_Time
        self.Departure_Airport = Departure_Airport
        self.Arrival_Date_time= Arrival_Date_Time
        self.Arrival_Airport = Arrival_Airport
        self.Flight_Number = Flight_Number
        self.Capacity= Capacity
        self.Price = Price
        self.AirPlaneID = AirplaneID

    def to_dict(self):
        """Return a dictionary"""
        return {
            'FlightID': self.FlightID,
            'Departure_Date_Time': self.Departure_Date_time,
            'Departure_Airport': self.Departure_Airport,
            'Arrival_Date_Time': self.Arrival_Date_time,
            'Arrival_Airport': self.Arrival_Airport,
            'Flight_Number': self.Flight_Number,
            'Capacity': self.Capacity,
            'Price': self.Price,
            'AirplaneID': self.AirPlaneID
        }
        


    @staticmethod
    def get_all():
        return Flight.query.all()

    def __repr__(self):
        return 'Flight: {}'.format(self.FlightsID)
