import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function ObservationsList() {
  const [observations, setObservations] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/observations')
      .then(res => setObservations(res.data.observations))
      .catch(err => console.error(err));
  }, []);

  if (observations.length === 0) return <p>No observations yet.</p>;

  return (
    <div style={{ maxWidth: '700px', margin: '0 auto' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '15px' }}>Submitted Observations</h2>
      {observations.map(obs => (
        <div
          key={obs.id}
          style={{
            border: '1px solid #ddd',
            borderRadius: '8px',
            padding: '12px',
            marginBottom: '12px',
            display: 'flex',
            alignItems: 'center',
            gap: '15px',
            backgroundColor: '#fff',
            boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
          }}
        >
          <div style={{ flex: 1 }}>
            <p><strong>Name:</strong> {obs.user_name}</p>
            <p><strong>Location:</strong> {obs.lat}, {obs.lon}</p>
            <p><strong>Date:</strong> {obs.date_observed}</p>
            <p><strong>Plant:</strong> {obs.plant_type}</p>
            <p><strong>Intensity:</strong> {obs.intensity}</p>
          </div>
          {obs.photo_path && (
            <img
              src={`http://127.0.0.1:5000/${obs.photo_path}`}
              alt="Observation"
              style={{ width: '100px', height: '100px', objectFit: 'cover', borderRadius: '5px' }}
            />
          )}
        </div>
      ))}
    </div>
  );
}
