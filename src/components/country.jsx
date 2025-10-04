import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
} from "recharts";

const RADIUS = 5; // ±5 degrees around country centroid

export default function CountryTrendChart() {
  const [data, setData] = useState([]);
  const [country, setCountry] = useState("India");
  const [yearRange, setYearRange] = useState({ start: 1981, end: 2010 });
  const [filteredData, setFilteredData] = useState([]);
  const [centroids, setCentroids] = useState({});
  const [loading, setLoading] = useState(true);

  // --- Load CSV + Centroid JSON ---
  useEffect(() => {
    const loadData = async () => {
      try {
        console.log("Loading CSV and centroids...");
        const csvResp = await fetch("/data/bloomwatch_land.csv");
        const csvText = await csvResp.text();
        const rows = csvText.trim().split("\n").slice(1); // skip header
        const parsed = rows.map((r) => {
          const [year, lat, lon, frost_days, id, tg, tn, tnn] = r.split(",");
          return {
            year: +year,
            lat: +lat,
            lon: +lon,
            frost_days: +frost_days,
            id: +id,
            tg: +tg,
            tn: +tn,
            tnn: +tnn,
          };
        });
        console.log("Parsed rows (first 5):", parsed.slice(0, 5));
        setData(parsed);

        const centroidsResp = await fetch("/data/country_centroids.json");
        const centroidsJson = await centroidsResp.json();
        console.log("Loaded centroids:", Object.keys(centroidsJson));
        setCentroids(centroidsJson);
      } catch (err) {
        console.error("Error loading data:", err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  // --- Filter Data by Country + Year Range ---
  useEffect(() => {
    if (!data.length || !centroids[country]) return;

    const { lat: latC, lon: lonC } = centroids[country].lat
      ? centroids[country]
      : { lat: centroids[country][0], lon: centroids[country][1] };

    const filtered = data.filter(
      (d) =>
        d.lat >= latC - RADIUS &&
        d.lat <= latC + RADIUS &&
        d.lon >= lonC - RADIUS &&
        d.lon <= lonC + RADIUS &&
        d.year >= yearRange.start &&
        d.year <= yearRange.end
    );

    console.log(
      `Filtered ${filtered.length} records for ${country} (${yearRange.start}-${yearRange.end})`
    );

    setFilteredData(filtered);
  }, [data, country, yearRange, centroids]);

  if (loading) return <p>⏳ Loading data...</p>;

  return (
    <div style={{ padding: "20px", fontFamily: "Inter, sans-serif" }}>
      <h2 style={{ textAlign: "center", marginBottom: "20px" }}>
        🌸 Bloom/Frost Trends for {country}
      </h2>

      {/* --- Country & Year Selection --- */}
      <div
        style={{
          display: "flex",
          gap: "10px",
          justifyContent: "center",
          alignItems: "center",
          marginBottom: "20px",
        }}
      >
        <select
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          style={{
            color:"black",
            padding: "8px 12px",
            border: "1px solid #ccc",
            borderRadius: "6px",
          }}
        >
          {Object.keys(centroids).map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>

        <input
          type="number"
          value={yearRange.start}
          onChange={(e) =>
            setYearRange({ ...yearRange, start: +e.target.value })
          }
          placeholder="Start Year"
          style={{
            color:"black",
            padding: "8px",
            width: "100px",
            border: "1px solid #ccc",
            borderRadius: "6px",
          }}
        />

        <input
          type="number"
          value={yearRange.end}
          onChange={(e) =>
            setYearRange({ ...yearRange, end: +e.target.value })
          }
          placeholder="End Year"
          style={{
            color:"black",
            padding: "8px",
            width: "100px",
            border: "1px solid #ccc",
            borderRadius: "6px",
          }}
        />
      </div>

      {/* --- Chart --- */}
      {filteredData.length > 0 ? (
        <LineChart
          width={900}
          height={400}
          data={filteredData}
          style={{ margin: "auto" }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="year" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="frost_days" stroke="#FF6B35" />
          <Line type="monotone" dataKey="tg" stroke="#1f77b4" />
          <Line type="monotone" dataKey="tnn" stroke="#2ca02c" />
        </LineChart>
      ) : (
        <p style={{ textAlign: "center", color: "#999" }}>
          No data found for this selection.
        </p>
      )}
    </div>
  );
}
