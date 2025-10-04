import React, { useState } from "react";
import axios from "axios";

const FlowerPredictor = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setPrediction(null);
    setError("");
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select an image first.");
      return;
    }
    setLoading(true);
    setError("");
    setPrediction(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/predict",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setPrediction(res.data);
    } catch (err) {
      console.error(err);
      setError("Error fetching prediction. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "500px", margin: "50px auto", textAlign: "center" }}>
      <h2>Flower Classifier</h2>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {preview && <img src={preview} alt="preview" style={{ maxWidth: "100%", margin: "20px 0" }} />}
      <br />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Predicting..." : "Predict"}
      </button>

      {prediction && (
        <div style={{ marginTop: "20px" }}>
          <h3>Prediction:</h3>
          <p>
            <strong>Class:</strong> {prediction.class}
          </p>
          <p>
            <strong>Confidence:</strong> {(prediction.confidence * 100).toFixed(2)}%
          </p>
        </div>
      )}

      {error && <p style={{ color: "red", marginTop: "20px" }}>{error}</p>}
    </div>
  );
};

export default FlowerPredictor;
