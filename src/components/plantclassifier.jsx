import React, { useState } from "react";

const PlantClassifier = () => {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
  };

  const handleUpload = async () => {
    if (!image) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", image);

    try {
      const res = await fetch("http://localhost:5000/predict", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Failed to classify. Check server logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Plant Classifier (CNN)</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {preview && <img src={preview} alt="preview" className="w-64 my-4" />}
      <button
        onClick={handleUpload}
        className="px-4 py-2 bg-green-600 text-white rounded"
        disabled={loading}
      >
        {loading ? "Classifying..." : "Classify"}
      </button>

      {result && (
        <div className="mt-4">
          <h2 className="text-lg font-semibold">Prediction:</h2>
          <p>
            {result.prediction} ({(result.confidence * 100).toFixed(2)}%)
          </p>
        </div>
      )}
    </div>
  );
};

export default PlantClassifier;
