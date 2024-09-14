// src/App.js
import React, { useState } from 'react';
import { reserveSeats, cancelBooking, showBooking } from './api'; // Import API functions

function App() {
  // State variables for form inputs
  const [originCity, setOriginCity] = useState('');
  const [destinationCity, setDestinationCity] = useState('');
  const [reqSeats, setReqSeats] = useState('');
  const [bookedUnder, setBookedUnder] = useState('');
  const [bookingId, setBookingId] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  // Handler for reserving seats
  const handleReserveSeats = async () => {
    try {
      const result = await reserveSeats(originCity, destinationCity, reqSeats, bookedUnder);
      setMessage(`Reservation successful: ${JSON.stringify(result)}`);
    } catch (error) {
      setMessage('Failed to reserve seats');
    }
  };

  // Handler for cancelling booking
  const handleCancelBooking = async () => {
    try {
      const result = await cancelBooking(bookingId, password);
      setMessage(result.message || 'Cancellation successful');
    } catch (error) {
      setMessage('Failed to cancel booking');
    }
  };

  // Handler for showing booking
  const handleShowBooking = async () => {
    try {
      const result = await showBooking(bookingId, password);
      setMessage(`Booking details: ${JSON.stringify(result)}`);
    } catch (error) {
      setMessage('Failed to show booking');
    }
  };

  return (
    <div className="App">
      <h1>Flight Reservation System</h1>

      {/* Reserve Seats Form */}
      <div>
        <h2>Reserve Seats</h2>
        <input
          type="text"
          placeholder="Origin City"
          value={originCity}
          onChange={(e) => setOriginCity(e.target.value)}
        />
        <input
          type="text"
          placeholder="Destination City"
          value={destinationCity}
          onChange={(e) => setDestinationCity(e.target.value)}
        />
        <input
          type="number"
          placeholder="Number of Seats"
          value={reqSeats}
          onChange={(e) => setReqSeats(e.target.value)}
        />
        <input
          type="text"
          placeholder="Booked Under"
          value={bookedUnder}
          onChange={(e) => setBookedUnder(e.target.value)}
        />
        <button type="button" onClick={handleReserveSeats}>Reserve Seats</button>
      </div>

      {/* Cancel Booking Form */}
      <div>
        <h2>Cancel Booking</h2>
        <input
          type="text"
          placeholder="Booking ID"
          value={bookingId}
          onChange={(e) => setBookingId(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="button" onClick={handleCancelBooking}>Cancel Booking</button>
      </div>

      {/* Show Booking Form */}
      <div>
        <h2>Show Booking</h2>
        <input
          type="text"
          placeholder="Booking ID"
          value={bookingId}
          onChange={(e) => setBookingId(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="button" onClick={handleShowBooking}>Show Booking</button>
      </div>

      {/* Message Display */}
      <p>{message}</p>
    </div>
  );
}

export default App;
