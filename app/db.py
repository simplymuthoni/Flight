import os
import mariadb
from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from mariadb import Error
from app.Flights import models
from app import config
import app

app.Config["SQLALCHEMY_DATABASE_URI"] = "mariadb+mariadbconnector://mugo:Demo123@127.0.0.1:3306/tembea"

db = SQLAlchemy(app)


def create_connection():
    
    conn = None
    try:
        conn = mariadb.connect(db)
    except Error as e:
        print(e)
    return conn

def create_tables():

    conn = create_connection()
    if conn is not None:
        
        conn.execute('''CREATE TABLE IF NOT EXISTS Users(
                            UserID CHAR(36) PRIMARY KEY,
                            Username VARCHAR(255) NOT NULL,
                            Name VARCHAR(255) NOT NULL,
                            Password VARCHAR(255) NOT NULL,
                            Email VARCHAR(255) NOT NULL,
                            Phone_Number VARCHAR(10) NOT NULL,
                            Address VARCHAR(255) NOT NULL);''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS Airport(
                            AirportID CHAR(36) PRIMARY KEY,
                            Airport_Code VARCHAR(255) NOT NULL,
                            Airport_Name VARCHAR(255) NOT NULL,
                            City VARCHAR(255) NOT NULL,
                            Country VARCHAR(255) NOT NULL);''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS Airplanes(
                            AirplaneID CHAR(36) PRIMARY KEY,
                            reg_number VARCHAR(255) NOT NULL,
                            total_seats INTEGER NOT NULL,
                            economy_seats INTEGER NOT NULL,
                            business_seats INTEGER NOT NULL,
                            first_class_seats INTEGER NOT NULL);''')
        
        
        conn.execute('''CREATE TABLE IF NOT EXISTS flight (
                            FlightID CHAR(36) PRIMARY KEY,
                            Flight_Number VARCHAR(255) NOT NULL,
                            Departure_Airport VARCHAR(255) NOT NULL,
                            Arrival_Airport VARCHAR(255) NOT NULL,
                            Departure_Date_Time DATETIME NOT NULL,
                            Arrival_Date_Time DATETIME NOT NULL,
                            price FLOAT NOT NULL,
                            Capacity INTEGER NOT NULL,
                            AirplaneID CHAR(36),
                            FOREIGN KEY(AirplaneID)REFERENCES Flights(AirplaneID));''')
        
        
        
        conn.commit()
        conn.close()

def init_db():
    
    create_tables()

# Flight management functions
def add_flight(origin, destination, departure_date, price):
    
    conn = create_connection()
    if conn is not None:
        conn.execute('''INSERT INTO flights (origin, destination, departure_date, price)
                       VALUES (?, ?, ?, ?);''', (origin, destination, departure_date, price))
        conn.commit()
        conn.close()

def get_flights():
    
    conn = create_connection()
    if conn is not None:
        flights = conn.execute('''SELECT * FROM flights;''').fetchall()
        conn.close()
        return flights

def update_flight(flight_id, origin, destination, departure_date, price):
    
    conn = create_connection()
    if conn is not None:
        conn.execute('''UPDATE flights SET origin=?, destination=?, departure_date=?, price=? WHERE id=?;''',
                       (origin, destination, departure_date, price, flight_id))
        conn.commit()
        conn.close()

def delete_flight(flight_id):
    
    conn = create_connection()
    if conn is not None:
        conn.execute('''DELETE FROM flights WHERE id=?;''', (flight_id,))
        conn.commit()
        conn.close()


       