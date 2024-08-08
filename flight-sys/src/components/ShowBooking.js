import React, { useState } from 'react';
import axios from 'axios';

function ShowBooking() {
  const [bookingId, setBookingId] = useState('');
  const [password, setPassword] = useState('');
  const [bookingDetails, setBookingDetails] = useState('');

  const handleShow = async () => {
    try {
      const response = await axios.post('http://localhost:5000/show', {
        booking_id: parseInt(bookingId),
        password: password,
      });
      if (response.data.success) {
        setBookingDetails(JSON.stringify(response.data.booking, null, 2));
      } else {
        setBookingDetails('Booking not found or incorrect details.');
      }
    } catch (error) {
      setBookingDetails('Error fetching booking.');
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
      <label>
        Password:
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </label>
      <br />
      <button onClick={handleShow}>Show Booking</button>
      <pre>{bookingDetails}</pre>
    </div>
  );
}

export default ShowBooking;
