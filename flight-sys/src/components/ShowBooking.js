import React, { useState } from 'react';
import axios from 'axios';

function ShowBooking() {
  const [bookingId, setBookingId] = useState('');
  const [bookingDetails, setBookingDetails] = useState(null);
  const [result, setResult] = useState('');

  const handleShow = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/booking/${bookingId}`);
      if (response.data.success) {
        setBookingDetails(response.data.booking);
        setResult('');
      } else {
        setResult('Booking not found.');
        setBookingDetails(null);
      }
    } catch (error) {
      setResult('Error fetching booking.');
    }
  };

  return (
    <div>
      <h2>Show Booking</h2>
      <label>
        Booking ID:
        <input type="number" value={bookingId} onChange={(e) => setBookingId(e.target.value)} />
      </label>
      <br />
      <button onClick={handleShow}>Show</button>
      {result && <p>{result}</p>}
      {bookingDetails && (
        <div>
          <h3>Booking Details</h3>
          <p>Name: {bookingDetails.booked_under}</p>
          <p>Number of Seats: {bookingDetails.num_seats}</p>
          <p>Distance: {bookingDetails.distance} miles</p>
          <p>Cost: ${bookingDetails.cost}</p>
        </div>
      )}
    </div>
  );
}

export default ShowBooking;
