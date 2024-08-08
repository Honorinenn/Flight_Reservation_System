import React, { useState } from 'react';
import axios from 'axios';

function ReserveSeats() {
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [numSeats, setNumSeats] = useState('');
  const [result, setResult] = useState('');

  const handleReserve = async () => {
    try {
      const response = await axios.post('http://localhost:5000/reserve', {
        originCity: origin,
        destinationCity: destination,
        numSeats: parseInt(numSeats),
      });
      setResult(`Booking Successful! ID: ${response.data.booking_id}, Password: ${response.data.password}`);
    } catch (error) {
      setResult('Error reserving seats.');
    }
  };

  return (
    <div>
      <h2>Reserve Seats</h2>
      <label>
        Origin City:
        <input type="text" value={origin} onChange={(e) => setOrigin(e.target.value)} />
      </label>
      <br />
      <label>
        Destination City:
        <input type="text" value={destination} onChange={(e) => setDestination(e.target.value)} />
      </label>
      <br />
      <label>
        Number of Seats:
        <input type="number" value={numSeats} onChange={(e) => setNumSeats(e.target.value)} />
      </label>
      <br />
      <button onClick={handleReserve}>Reserve</button>
      <p>{result}</p>
    </div>
  );
}

export default ReserveSeats;
