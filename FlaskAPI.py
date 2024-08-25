from flask import Flask, jsonify, request

@app.route('/reserve', methods=['POST'])
def reserve_seats():
    data = request.json
    origin_city = data.get('origin_city')
    destination_city = data.get('destination_city')
    num_seats = data.get('num_seats')
    
    # Simulate reservation logic (replace with actual logic)
    if origin_city and destination_city and num_seats > 0:
        # Dummy reservation ID and success response
        return jsonify({
            'success': True,
            'booking_id': 1,  # This should be generated dynamically
            'password': 'abcd1234'
        }), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid input data.'}), 400

@app.route('/cancel', methods=['POST'])
def cancel_booking():
    data = request.json
    booking_id = data.get('booking_id')
    password = data.get('password')
    
    # Simulate cancellation logic (replace with actual logic)
    if booking_id and password:
        # Dummy success response
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid booking ID or password.'}), 400

@app.route('/booking/<int:booking_id>', methods=['GET'])
def show_booking(booking_id):
    # Simulate fetching booking details (replace with actual logic)
    booking = {
        'booking_id': booking_id,
        'name': 'John Doe',
        'num_seats': 2,
        'flights': ['Flight 123', 'Flight 456'],
        'cost': 150
    }
    
    return jsonify({'success': True, 'booking': booking}), 200
