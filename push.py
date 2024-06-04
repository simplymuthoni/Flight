from flask import Flask, request, jsonify

app = Flask(__name__)


Users = [
    {"id": 1, "name": "John Doe", "token": "abc123xyz"},
    {"id": 2, "name": "Jane Smith", "token": "def456uvw"},
   
]

# Endpoint to send push notifications
@app.route('/send_push', methods=['POST'])
def send_push_notification():
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')

    if not user_id or not message:
        return jsonify({"error": "Missing user_id or message"}), 400

    user = next((user for user in Users if user['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    print(f"Sending push notification to {user['name']}: {message}")

    return jsonify({"message": "Push notification sent successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
