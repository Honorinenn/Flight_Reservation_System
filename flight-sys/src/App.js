import React, { useState } from 'react';
import axios from 'axios';
import ReserveSeats from './ReserveSeats';
import CancelBooking from './CancelBooking';
import ShowBooking from './ShowBooking';

function App() {
  const [view, setView] = useState('reserve'); // 'reserve', 'cancel', 'show'

  const handleViewChange = (newView) => {
    setView(newView);
  };

  return (
    <div className="App">
      <h1>Flight Booking System</h1>
      <nav>
        <button onClick={() => handleViewChange('reserve')}>Reserve Seats</button>
        <button onClick={() => handleViewChange('cancel')}>Cancel Booking</button>
        <button onClick={() => handleViewChange('show')}>Show Booking</button>
      </nav>
      {view === 'reserve' && <ReserveSeats />}
      {view === 'cancel' && <CancelBooking />}
      {view === 'show' && <ShowBooking />}
    </div>
  );
}

export default App;
