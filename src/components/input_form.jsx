import React, { useState } from 'react';
import axios from 'axios';

export default function CitizenObservationForm() {
  const [formData, setFormData] = useState({
    user_name: '',
    lat: '',
    lon: '',
    date_observed: '',
    plant_type: '',
    intensity: '',
    photo: null,
  });

  const handleChange = (e) => {
    if (e.target.name === 'photo') {
      setFormData({ ...formData, photo: e.target.files[0] });
    } else {
      setFormData({ ...formData, [e.target.name]: e.target.value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();
    Object.entries(formData).forEach(([key, value]) => data.append(key, value));

    try {
      await axios.post('http://127.0.0.1:5000/observations', data);
      alert('Observation submitted!');
      setFormData({
        user_name: '',
        lat: '',
        lon: '',
        date_observed: '',
        plant_type: '',
        intensity: '',
        photo: null,
      });
    } catch (err) {
      console.error(err);
      alert('Failed to submit observation');
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        display: 'flex',
        flexDirection: 'column',
        width: '350px',
        gap: '12px',
        padding: '20px',
        border: '1px solid #ccc',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
        marginBottom: '20px',
        backgroundColor: '#fafafa',
      }}
    >
      <h2 style={{ textAlign: 'center', marginBottom: '10px' }}>Submit Observation</h2>
      <input name="user_name" placeholder="Your Name" value={formData.user_name} onChange={handleChange} required />
      <input name="lat" placeholder="Latitude" value={formData.lat} onChange={handleChange} required />
      <input name="lon" placeholder="Longitude" value={formData.lon} onChange={handleChange} required />
      <input type="date" name="date_observed" value={formData.date_observed} onChange={handleChange} required />
      <input name="plant_type" placeholder="Plant Type" value={formData.plant_type} onChange={handleChange} required />
      <input name="intensity" placeholder="Intensity" value={formData.intensity} onChange={handleChange} />
      <input type="file" name="photo" onChange={handleChange} />
      <button
        type="submit"
        style={{
          padding: '10px',
          border: 'none',
          backgroundColor: '#28a745',
          color: 'white',
          fontWeight: 'bold',
          borderRadius: '5px',
          cursor: 'pointer',
        }}
      >
        Submit
      </button>
    </form>
  );
}
