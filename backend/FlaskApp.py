from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
from FLIGHT import FlightSystem  # Import the FlightSystem class

app = Flask(__name__)
CORS(app, resources={
    r"/api/*" : {"origins" : "*"}
})  # Enable CORS for all routes

# Initialize the FlightSystem
fs = FlightSystem()
fs.install()

@app.route('/test', methods=['GET'])
def test():
    return jsonify("test")

@app.route('/reserve', methods=['POST'])
def reserve():
    print("testing reservr")
    data = request.json
    result = fs.reserveSeats(
        data.get('originCity'),
        data.get('destinationCity'),
        data.get('reqseats'),
        data.get('booked_under')
    )
    return jsonify(result)

@app.route('/cancel', methods=['POST'])
def cancel():
    data = request.json
    result = fs.cancellation(
        data.get('booking_id'),
        data.get('password')
    )
    return jsonify({"message": result})

@app.route('/show', methods=['POST'])
def show():
    data = request.json
    result = fs.showBooking(
        data.get('booking_id'),
        data.get('password')
    )
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
