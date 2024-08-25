import React, { useState } from 'react';
import axios from 'axios';

function ReserveSeats() {
  const [originCity, setOriginCity] = useState('');
  const [destinationCity, setDestinationCity] = useState('');
  const [numSeats, setNumSeats] = useState('');
  const [result, setResult] = useState('');

  const handleReserve = async () => {
    try {
      const response = await axios.post('http://localhost:5000/reserve', {
        originCity,
        destinationCity,
        numSeats: parseInt(numSeats),
      });
      if (response.data.success) {
        setResult('Seats reserved successfully!');
      } else {
        setResult('Reservation failed.');
      }
    } catch (error) {
      setResult('Error reserving seats.');
    }
  };

  return (
    <div>
      <h2>Reserve Seats</h2>
      <label>
        Origin City:
        <input type="text" value={originCity} onChange={(e) => setOriginCity(e.target.value)} />
      </label>
      <br />
      <label>
        Destination City:
        <input type="text" value={destinationCity} onChange={(e) => setDestinationCity(e.target.value)} />
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
