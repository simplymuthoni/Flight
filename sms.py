from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

account_sid = os.environ.get('account_sid')
auth_token = os.environ.get('auth_token')
twilio_phone_number = os.environ.get('twilio_phone_number')

# Dummy data for demonstration purposes
users = [
    {"id": 1, "name": "John Doe", "phone": "+1234567890"},
    {"id": 2, "name": "Jane Smith", "phone": "+1987654321"},
    # Add more users as needed
]

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Endpoint to send SMS notifications
@app.route('/send_sms', methods=['POST'])
def send_sms_notification():
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')

    if not user_id or not message:
        return jsonify({"error": "Missing user_id or message"}), 400

    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Send SMS using Twilio
    try:
        client.messages.create(
            to=user['phone'],
            from_=twilio_phone_number,
            body=message
        )
        return jsonify({"message": "SMS notification sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
