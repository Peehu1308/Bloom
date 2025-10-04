from flask import Flask, request, jsonify, send_from_directory
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
import sqlite3
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
import requests

# -----------------------------
# Paths
# -----------------------------
PHOTO_FOLDER = os.path.abspath("../db/photos")
DB_PATH = os.path.abspath("../db/citizen_observations.db")
os.makedirs(PHOTO_FOLDER, exist_ok=True)

# -----------------------------
# Flask app
# -----------------------------
app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

# -----------------------------
# SQLite Table
# -----------------------------
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS CitizenObservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    location_lat REAL,
    location_lon REAL,
    date_observed TEXT,
    plant_type TEXT,
    intensity TEXT,
    photo_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()

# -----------------------------
# Flower Model
# -----------------------------
MODEL_PATH = "flower_classifier.h5"
model = load_model(MODEL_PATH)

class_names = ['dandelion', 'daisy', 'tulip', 'sunflower', 'rose']
IMG_SIZE = 224

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# -----------------------------
# Prediction Endpoint
# -----------------------------
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    img_array = preprocess_image(file.read())
    prediction = model.predict(img_array)
    class_index = int(np.argmax(prediction, axis=1)[0])
    class_name = class_names[class_index]
    confidence = float(np.max(prediction))
    return jsonify({'class': class_name, 'confidence': confidence})

# -----------------------------
# Add Observation
# -----------------------------
@app.route('/observations', methods=['POST'])
def add_observation():
    user_name = request.form.get('user_name')
    lat = request.form.get('lat', type=float)
    lon = request.form.get('lon', type=float)
    date_observed = request.form.get('date_observed')
    plant_type = request.form.get('plant_type')
    intensity = request.form.get('intensity')
    photo = request.files.get('photo')

    photo_filename = None
    if photo:
        photo_filename = secure_filename(photo.filename)
        photo_path = os.path.join(PHOTO_FOLDER, photo_filename)
        photo.save(photo_path)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO CitizenObservations
        (user_name, location_lat, location_lon, date_observed, plant_type, intensity, photo_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_name, lat, lon, date_observed, plant_type, intensity, photo_filename))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

# -----------------------------
# Get Observations
# -----------------------------
@app.route('/observations', methods=['GET'])
def get_observations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CitizenObservations")
    rows = cursor.fetchall()
    conn.close()

    observations = [
        {
            'id': r[0],
            'user_name': r[1],
            'lat': r[2],
            'lon': r[3],
            'date_observed': r[4],
            'plant_type': r[5],
            'intensity': r[6],
            'photo_path': r[7],
            'created_at': r[8]
        }
        for r in rows
    ]
    return jsonify({'observations': observations})

# -----------------------------
# Serve Photos
# -----------------------------
@app.route('/photos/<filename>')
def serve_photo(filename):
    return send_from_directory(PHOTO_FOLDER, filename)

# -----------------------------
# Weather Endpoint
# -----------------------------
WEATHER_API_KEY = "04836cb9d8ca43398f9201033250410"

@app.route('/weather/<float:lat>/<float:lon>')
def get_weather(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        data = response.json()
        if response.status_code != 200:
            return jsonify({'error': data.get('message', 'Failed to fetch weather')}), 500
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -----------------------------
# Run Flask
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
