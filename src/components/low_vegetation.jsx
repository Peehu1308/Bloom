import React, { useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const LowVegetationData = () => {
  const [place, setPlace] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    if (!place || !startDate || !endDate) {
      alert("Please enter location, start date, and end date");
      return;
    }

    setLoading(true);
    setData(null);

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/lai_lv?place=${place}&start_date=${startDate}&end_date=${endDate}`
      );
      const json = await res.json();
      if (json.error) {
        alert(json.error);
        setData(null);
      } else {
        setData(json);
      }
    } catch (err) {
      console.error(err);
      alert("Failed to fetch data from backend");
    } finally {
      setLoading(false);
    }
  };

  const chartData = data
    ? {
        labels: data.times,
        datasets: [
          {
            label: "Leaf Area Index (LAI)",
            data: data.lai_values,
            borderColor: "#22c55e", // bright green line
            backgroundColor: "rgba(34, 197, 94, 0.2)", // semi-transparent fill
            fill: true,
            tension: 0.4,
            pointRadius: 3,
            pointHoverRadius: 6,
            borderWidth: 3,
          },
        ],
      }
    : null;

  return (
    <div className="p-8 bg-black min-h-screen flex flex-col items-center">
      <div className="w-full max-w-5xl bg-gray-900 shadow-2xl rounded-3xl p-8 border-t-4 border-green-700">
        <h1 className="text-3xl font-extrabold mb-6 text-center text-green-400 drop-shadow-md">
          Low Vegetation LAI Viewer
        </h1>

        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <input
            type="text"
            value={place}
            onChange={(e) => setPlace(e.target.value)}
            placeholder="Enter location (e.g., Delhi)"
            className="text-green-400 bg-gray-800 border border-green-600 p-4 rounded-2xl flex-1 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 shadow-sm hover:shadow-md transition-all"
          />
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="border p-4 rounded-2xl text-green-400 bg-gray-800 focus:ring-2 focus:ring-green-500 focus:border-green-500 shadow-sm hover:shadow-md transition-all"
          />
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="border p-4 rounded-2xl text-green-400 bg-gray-800 focus:ring-2 focus:ring-green-500 focus:border-green-500 shadow-sm hover:shadow-md transition-all"
          />
          <button
            onClick={fetchData}
            className={`py-4 px-8 rounded-2xl text-black font-semibold shadow-lg transition-all hover:shadow-2xl ${
              loading ? "bg-green-600 cursor-not-allowed" : "bg-green-400 hover:bg-green-500"
            }`}
            disabled={loading}
          >
            {loading ? "Loading..." : "Get Data"}
          </button>
        </div>

        {data && (
          <div className="bg-gray-800 p-6 rounded-3xl shadow-inner border-l-4 border-green-700">
            <div className="flex flex-wrap gap-4 mb-6">
              <span className="bg-green-700 text-black px-5 py-2 rounded-full font-semibold shadow-sm">
                {data.place.toUpperCase()}
              </span>
              <span className="bg-green-700 text-black px-5 py-2 rounded-full font-semibold shadow-sm">
                Latitude: {data.latitude}
              </span>
              <span className="bg-green-700 text-black px-5 py-2 rounded-full font-semibold shadow-sm">
                Longitude: {data.longitude}
              </span>
            </div>

            <div className="w-full overflow-x-auto" style={{ height: 450 }}>
              <Line
                data={chartData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: { position: "top", labels: { color: "#22c55e", font: { weight: "bold" } } },
                    tooltip: { mode: "index", intersect: false, backgroundColor: "#064e3b", titleColor: "#fff", bodyColor: "#fff" },
                  },
                  scales: {
                    x: { ticks: { color: "#22c55e" }, grid: { color: "#064e3b" } },
                    y: { ticks: { color: "#22c55e" }, grid: { color: "#064e3b" } },
                  },
                }}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default LowVegetationData;
