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

const VegetationData = () => {
  const [place, setPlace] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch(`http://127.0.0.1:8000/lai?place=${place}`);
      const json = await res.json();
      if (json.error) {
        alert(json.error);
        setData(null);
      } else {
        setData(json);
      }
    } catch (err) {
      console.error(err);
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
            borderColor: "#16a34a", // Tailwind green-600
            backgroundColor: "rgba(22,163,74,0.2)",
            fill: true,
            tension: 0.3, // smoother line
            pointRadius: 2,
          },
        ],
      }
    : null;

  return (
    <div className="p-6 bg-gray-50 min-h-screen flex flex-col items-center">
      <div className="w-full max-w-4xl bg-white shadow-xl rounded-2xl p-6">
        <h1 className="text-2xl font-extrabold mb-3 text-center text-green-700">
          Bloom Data Viewer
        </h1>
        <div className="h-1 w-24 bg-green-600 mx-auto rounded-full mb-6"></div>

        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          <input
            type="text"
            value={place}
            onChange={(e) => setPlace(e.target.value)}
            placeholder="Enter location (e.g., Delhi)"
            className="border border-gray-300 p-3 rounded-xl flex-1 focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-green-500 shadow-sm text-green-900"
          />
          <button
            onClick={fetchData}
            className="bg-green-600 text-white py-3 px-6 rounded-xl hover:bg-green-700 transition-all shadow-md"
          >
            {loading ? "Loading..." : "Get Data"}
          </button>
        </div>

        {data && (
          <div className="bg-green-50 p-5 rounded-xl shadow-inner">
            <div className="flex flex-wrap gap-4 mb-5">
              <span className="bg-green-100 text-green-800 px-4 py-2 rounded-full font-semibold">
                {data.place.toUpperCase()}
              </span>
              <span className="bg-green-100 text-green-800 px-4 py-2 rounded-full font-semibold">
                Latitude: {data.latitude}
              </span>
              <span className="bg-green-100 text-green-800 px-4 py-2 rounded-full font-semibold">
                Longitude: {data.longitude}
              </span>
            </div>

            <div className="w-full overflow-x-auto">
              <Line data={chartData} options={{ responsive: true, maintainAspectRatio: false, height: 300 }} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VegetationData;
