// src/api.js
import axios from 'axios';

// const API_BASE_URL = 'http://localhost:5000'; // Replace with your backend URL


const API_BASE_URL = 'https://stunning-engine-v7gr6469xwp2pw5x-5000.app.github.dev'

export const reserveSeats = async (originCity, destinationCity, reqSeats, bookedUnder) => {
  try {


    
    
    const response = await axios.post(`${API_BASE_URL}/reserve`, {
      maxRedirect : 0,
      withCredentials : true,
      originCity,
      destinationCity,
      reqSeats,
      bookedUnder
    });
    console.log(response);
    return response.data;
  } catch (error) {
    console.error('Error reserving seats:', error);
    throw error;
  }
};

export const cancelBooking = async (bookingId, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/cancel`, {
      bookingId,
      password
    });
    return response.data;
  } catch (error) {
    console.error('Error cancelling booking:', error);
    throw error;
  }
};

export const showBooking = async (bookingId, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/show`, {
      bookingId,
      password
    });
    return response.data;
  } catch (error) {
    console.error('Error showing booking:', error);
    throw error;
  }
};
