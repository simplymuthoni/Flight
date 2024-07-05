# Flight Management API

This is a Flask-based Flight Management API that allows users to manage flights, including creating, retrieving, updating, and deleting flight records. The API is documented using Swagger.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Swagger Documentation](#swagger-documentation)
- [Database Models](#database-models)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/flight-management-api.git
    cd flight-management-api
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. Run the application:

    ```bash
    flask run
    ```

## Usage

After running the application, you can interact with the API using an API client like Postman or cURL. You can also view the Swagger documentation in your browser.

## API Endpoints

### Get All Flights

- **URL:** `/flights`
- **Method:** `GET`
- **Description:** Retrieve a list of all flights.

### Create a Flight

- **URL:** `/create`
- **Method:** `POST`
- **Description:** Create a new flight.
- **Request Body:**
    ```json
    {
        "flight_number": "string",
        "departure_airport": "string",
        "arrival_airport": "string",
        "departure_date_time": "string (ISO 8601 format: YYYY-MM-DDTHH:MM:SS)",
        "arrival_date_time": "string (ISO 8601 format: YYYY-MM-DDTHH:MM:SS)",
        "airplane_id": "integer",
        "capacity": "integer",
        "price": "number"
    }
    ```

### Update a Flight

- **URL:** `/update/<int:flight_id>`
- **Method:** `PATCH`
- **Description:** Update an existing flight.
- **Request Body:**
    ```json
    {
        "flight_number": "string",
        "departure_airport": "string",
        "arrival_airport": "string",
        "departure_date_time": "string (ISO 8601 format: YYYY-MM-DDTHH:MM:SS)",
        "arrival_date_time": "string (ISO 8601 format: YYYY-MM-DDTHH:MM:SS)",
        "airplane_id": "integer",
        "capacity": "integer",
        "price": "number"
    }
    ```

### Delete a Flight

- **URL:** `/delete/<int:flight_id>`
- **Method:** `DELETE`
- **Description:** Delete an existing flight.

## Swagger Documentation

The API is documented using Swagger. After running the application, navigate to `http://localhost:5000/apidocs` to view the Swagger documentation.

## Database Models

### Flight

- **flight_number:** `string`
- **departure_airport:** `string`
- **arrival_airport:** `string`
- **departure_date_time:** `datetime`
- **arrival_date_time:** `datetime`
- **airplane_id:** `integer`
- **capacity:** `integer`
- **price:** `float`

### Airplane

- **id:** `integer`
- **model:** `string`
- **capacity:** `integer`



