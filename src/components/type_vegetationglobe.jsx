import React, { useEffect, useState, useRef } from "react";
import Globe from "react-globe.gl";

function VegetationHeatmapGlobe() {
  const globeRef = useRef();
  const [lowPoints, setLowPoints] = useState([]);
  const [highPoints, setHighPoints] = useState([]);

  // Load both datasets
  useEffect(() => {
    async function fetchData() {
      try {
        const [low, high] = await Promise.all([
          fetch("/Mhmd08___inaturalist/low_vegetation_points.json").then(res => res.json()),
          fetch("/Mhmd08___inaturalist/high_vegetation_points.json").then(res => res.json())
        ]);

        setLowPoints(low);
        setHighPoints(high);
      } catch (err) {
        console.error("Error loading vegetation data:", err);
      }
    }
    fetchData();
  }, []);

  // Color mapping with visible alpha
  const getColor = (d) => {
    const alpha = Math.max(d.value, 0.3); // minimum opacity
    return d.type === "low" ? `rgba(144,238,144,${alpha})` : `rgba(0,100,0,${alpha})`;
  };

  // Altitude: scaled for visibility
  const getAltitude = (d) => Math.max(d.value * 5, 0.5);

  // Radius: scaled for visibility
  const getRadius = (d) => Math.max(d.size * 5, 0.5);

  // Continuous rotation
  useEffect(() => {
    const globe = globeRef.current;
    if (!globe) return;
    const controls = globe.controls();
    if (controls) {
      controls.autoRotate = true;
      controls.autoRotateSpeed = 0.5;
    }
  }, []);

  return (
    <div style={{ width: "100vw", height: "100vh", position: "relative" }}>
      {/* Legend */}
      <div style={{
        position: "absolute",
        bottom: 20,
        right: 20,
        background: "#fff",
        padding: 10,
        borderRadius: 8,
        zIndex: 10
      }}>
        <div style={{ display: "flex", alignItems: "center", marginBottom: 5 }}>
          <div style={{ width: 20, height: 20, backgroundColor: "rgba(144,238,144,1)", marginRight: 5 }}></div>
          <span>Low Vegetation</span>
        </div>
        <div style={{ display: "flex", alignItems: "center" }}>
          <div style={{ width: 20, height: 20, backgroundColor: "rgba(0,100,0,1)", marginRight: 5 }}></div>
          <span>High Vegetation</span>
        </div>
      </div>

      {/* Globe */}
      <Globe
        ref={globeRef}
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
        pointsData={[
          ...lowPoints.map(p => ({ ...p, type: "low" })),
          ...highPoints.map(p => ({ ...p, type: "high" }))
        ]}
        pointLat="lat"
        pointLng="lng"
        pointColor={getColor}
        pointAltitude={getAltitude}
        pointRadius={getRadius}
        backgroundColor="#000000"
      />
    </div>
  );
}

export default VegetationHeatmapGlobe;
