import React, { useEffect } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet.heat";

function HeatmapLayer({ points }) {
  const map = useMap();
  useEffect(() => {
    if (!points || points.length === 0) return;

    const heatPoints = points.map((p) => [p.lat, p.lon, p.frost_days / 100]); // normalize value
    const layer = L.heatLayer(heatPoints, { radius: 25, blur: 15 }).addTo(map);

    return () => map.removeLayer(layer);
  }, [map, points]);

  return null;
}

export default function HeatmapView({ data }) {
  return (
    <MapContainer center={[0, 0]} zoom={2} style={{ height: "600px" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <HeatmapLayer points={data} />
    </MapContainer>
  );
}
