import React, { useEffect, useState, useRef } from "react";
import Globe from "react-globe.gl";

function VegetationGlobe() {
  const [points, setPoints] = useState([]);
  const [searchLat, setSearchLat] = useState("");
  const [searchLng, setSearchLng] = useState("");
  const globeRef = useRef();

  // 1️⃣ Fetch vegetation data
  useEffect(() => {
    async function fetchVegetationData() {
      try {
        const [lowRes, highRes] = await Promise.all([
          fetch("/Mhmd08___inaturalist/low_vegetation_cover_0_daily-mean.json").then(res => res.json()),
          fetch("/Mhmd08___inaturalist/high_vegetation_cover_stream-oper_daily-mean.json").then(res => res.json())
        ]);

        const latitudes = lowRes.latitude || lowRes.lat;
        const longitudes = lowRes.longitude || lowRes.lon;
        const lowData = lowRes.vegetation || lowRes[Object.keys(lowRes).find(k => !["lat","lon","latitude","longitude"].includes(k))];
        const highData = highRes.vegetation || highRes[Object.keys(highRes).find(k => !["lat","lon","latitude","longitude"].includes(k))];

        const pointsArray = [];
        for (let i = 0; i < latitudes.length; i++) {
          for (let j = 0; j < longitudes.length; j++) {
            const lowVal = lowData[i]?.[j] || 0;
            const highVal = highData[i]?.[j] || 0;
            const totalVeg = lowVal + highVal;

            pointsArray.push({
              lat: latitudes[i],
              lng: longitudes[j],
              size: 0.2,
              color: getColorFromVegetation(totalVeg)
            });
          }
        }

        setPoints(pointsArray);
        console.log("Total points:", pointsArray.length);
      } catch (err) {
        console.error("Error loading vegetation data:", err);
      }
    }

    fetchVegetationData();
  }, []);

  // 2️⃣ Color mapping
  function getColorFromVegetation(value) {
    if (value < 0.2) return "#a0522d";
    if (value < 0.5) return "#7cfc00";
    return "#006400";
  }

  // 3️⃣ Continuous rotation
  // 3️⃣ Continuous rotation (fixed)
useEffect(() => {
  const globe = globeRef.current;
  if (!globe) return;

  const controls = globe.controls();
  if (controls) {
    controls.autoRotate = true;       // enable auto rotation
    controls.autoRotateSpeed = 0.5;   // adjust rotation speed
  }
}, []);

  // 4️⃣ Handle fly-to location
  const flyToLocation = () => {
    const globe = globeRef.current;
    if (!globe) return;

    const lat = parseFloat(searchLat);
    const lng = parseFloat(searchLng);
    if (isNaN(lat) || isNaN(lng)) return;

    globe.pointOfView({ lat, lng, altitude: 2 }, 2000); // smooth 2s transition
  };

  return (
    <div style={{ width: "100vw", height: "100vh", position: "relative" }}>
      {/* Search input */}
      <div style={{ position: "absolute", top: 10, left: 10, zIndex: 10, background: "#fff", padding: 10, borderRadius: 8 }}>
        <input
          type="number"
          placeholder="Latitude"
          value={searchLat}
          onChange={(e) => setSearchLat(e.target.value)}
          style={{ marginRight: 5 }}
          className="border border-gray-700 text-black rounded-xl p-2"
        />
        <input
          type="number"
          placeholder="Longitude"
          value={searchLng}
          onChange={(e) => setSearchLng(e.target.value)}
          style={{ marginRight: 5 }}
          className="border border-gray-700 text-black rounded-xl p-2"
        />
        <button onClick={flyToLocation} className="bg-black text-white rounded p-3">Go</button>
      </div>

      {/* Globe */}
      <Globe
        ref={globeRef}
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
        pointsData={points}
        pointLat="lat"
        pointLng="lng"
        pointColor="color"
        pointAltitude={0.01}
        pointRadius="size"
        backgroundColor="#000000"
      />
    </div>
  );
}

export default VegetationGlobe;
