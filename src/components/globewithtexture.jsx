import React from 'react';
import Globe from 'react-globe.gl';

export default function TypeVegetationGlobe() {
  return (
    <div style={{ height: '100vh' }}>
      <Globe
        globeImageUrl="/vegetation_map.png"  // the texture image we created
        backgroundColor="#000000"
      />
    </div>
  );
}
