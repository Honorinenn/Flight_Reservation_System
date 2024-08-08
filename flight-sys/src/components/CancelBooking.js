import React, { useState } from 'react';
import axios from 'axios';

function CancelBooking() {
  const [bookingId, setBookingId] = useState('');
  const [password, setPassword] = useState('');
  const [result, setResult] = useState('');

  const handleCancel = async () => {
    try {
      const response = await axios.post('http://localhost:5000/cancel', {
        booking_id: parseInt(bookingId),
        password: password,
      });
      if (response.data.success) {
        setResult('Booking cancelled successfully!');
      } else {
        setResult('Cancellation failed.');
      }
    } catch (error) {
      setResult('Error cancelling booking.');
    }
  };

  return (
    <div>
      <h2>Cancel Booking</h2>
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
      <button onClick={handleCancel}>Cancel</button>
      <p>{result}</p>
    </div>
  );
}

export default CancelBooking;
