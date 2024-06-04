import datetime
import uuid
from app import db
from base_model import BaseModel


class Airport(BaseModel):
    """This class defines the airports table"""

    __tablename__ = 'Airpot'
   

    AirportID = db.Column(db.String, primary_key=True, default=lambda:str(uuid.uuid4()))
    AirportCode = db.Column(db.String, nullable=False)
    AirportName = db.Column(db.String, nullable=False)
    city = db.Column(db.String(256), nullable=False)
    country = db.Column(db.String(256), nullable=False)
    Latitude = db.Column(db.String, nullable=False)
    Longitude = db.Column(db.String, nullable=False)
    flights = db.relationship('Flight', backref='airport', lazy=True)

    def __init__(self, AirportName, country, city):
        """Initialize the airport with the airport details"""
        self.AirportName = AirportName
        self.country = country
        self.city = city

    def serialize(self):
        """Return a dictionary"""
        return {
            'airport_id': self.id,
            'airport_name': self.AirportName,
            'country': self.country,
            'city': self.city
        }

    @staticmethod
    def get_all():
        return Airport.query.all()

    def __repr__(self):
        return 'airports: {}'.format(self.name)


class Airplane(BaseModel):
    """This class defines the airplanes table"""

    __tablename__ = 'airplanes'

    id = db.Column(db.Integer, primary_key=True)
    reg_number = db.Column(db.String, nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    economy_seats = db.Column(db.Integer, nullable=False)
    business_seats = db.Column(db.Integer, nullable=False)
    flights = db.relationship('Flight', backref='airplane', lazy=True)

    def __init__(self, reg_number, economy_seats, business_seats,
                 first_class_seats):
        """Initialize the airplane details"""
        self.reg_number = reg_number
        self.total_seats = economy_seats + business_seats
        self.economy_seats = economy_seats
        self.business_seats = business_seats
        self.first_class_seats = first_class_seats

    def serialize(self):
        """Return a dictionary"""
        return {
            'airplane_id': self.id,
            'reg_number': self.reg_number,
            'business_seats': self.business_seats,
            'economy_seats': self.economy_seats,
            'total_seats': self.total_seats
        }

    @staticmethod
    def get_all():
        return Airplane.query.all()

    def __repr__(self):
        return 'Airplane: {}'.format(self.reg_number)


class Flight(BaseModel):
    """This class defines the flight schedules table"""

    __tablename__ = 'Flights'

    FlightsID = db.Column(db.Integer, primary_key=True)
    Flight_Number = db.Column(db.Integer)
    Departure_Airport = db.Column(db.String, nullable=False)
    Arrival_Airport = db.Column(db.String, nullable=False)
    Departure_Date_time =db.Column(db.DateTime)
    Arrival_Date_time = db.Column(db.DateTime)
    Capacity=db.Colum(db.Integer)
    Price =db.Column(db.Currency)
    bookings = db.relationship('Booking', backref='flight', lazy=True)

    def __init__(self, Departure_Date_Time, Departure_Airport, Arrival_Date_Time,
                 Arrival_Airport, FlightsID):
        """Initialize the flight details"""
        
        
        self.Departure_Date_time = Departure_Date_Time
        self.Departure_Airport = Departure_Airport
        self.Arrival_Date_time= Arrival_Date_Time
        self.Arrival_Airport = Arrival_Airport
        self.FlightsID = FlightsID

    def get_arrival_airport(self):
        return Airport.query.filter_by(id=self.Arrival_Airport).first()

    def serialize(self):
        """Return a dictionary"""
        self.arrival_airport = self.get_arrival_airport()
        return {
            'FlightID': self.FlightsID,
            'Departure_Date_Time': self.Departure_Date_time,
            'Departure_Airport': self.Departure_Airport,
            'Arrival_Date_Time': self.Arrival_Date_time,
            'Arrival_Airport': self.Arrival_Airport,
        }

    @staticmethod
    def get_all():
        return Flight.query.all()

    def __repr__(self):
        return 'Flight: {}'.format(self.id)
