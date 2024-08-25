import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ReserveSeats from './components/ReserveSeats';
import CancelBooking from './components/CancelBooking';
import ShowBooking from './components/ShowBooking';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/some-endpoint');
        setData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <h1>Flight Reservation System</h1>
      <ReserveSeats />
      <CancelBooking />
      <ShowBooking />
      {/* Display fetched data */}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}

export default App;
