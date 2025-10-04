import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function TrendChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="year" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="frost_days" stroke="#1f77b4" />
        <Line type="monotone" dataKey="tg" stroke="#ff7f0e" />
        <Line type="monotone" dataKey="tnn" stroke="#2ca02c" />
      </LineChart>
    </ResponsiveContainer>
  );
}
