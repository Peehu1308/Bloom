import os
import json
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from tensorflow.keras.callbacks import Callback
import threading
import requests
from io import BytesIO
import re  # For URL parsing
import time  # For retries

# Suppress TensorFlow warnings (uncomment if you want quieter output)
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# import warnings
# warnings.filterwarnings('ignore', category=User Warning)

# ---------------- FLASK APP ----------------
app = Flask(__name__)
CORS(app)

# ---------------- PATHS ----------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../public"))
TRAIN_JSON = os.path.join(BASE_DIR, "train_plants.json")
TEST_JSON = os.path.join(BASE_DIR, "test_plants.json")
TRAIN_DIR = os.path.join(BASE_DIR, "train_dir")
TEST_DIR = os.path.join(BASE_DIR, "test_dir")
MODEL_PATH = os.path.join(BASE_DIR, "plant_cnn.keras")  # native Keras format
LABELS_PATH = os.path.join(BASE_DIR, "labels.json")
HISTORY_PATH = os.path.join(BASE_DIR, "training_history.json")

# ---------------- CALLBACK FOR TRAINING PROGRESS ----------------
class TrainingProgress(Callback):
    def on_epoch_begin(self, epoch, logs=None):
        print(f"\n=== Starting Epoch {epoch+1}/10 ===")
    def on_epoch_end(self, epoch, logs=None):
        train_loss = logs.get("loss")
        train_acc = logs.get("accuracy")
        val_loss = logs.get("val_loss")
        val_acc = logs.get("val_accuracy")
        print(
            f"=== Epoch {epoch+1} Finished ===\n"
            f"Train loss: {train_loss:.4f}, Train accuracy: {train_acc:.4f}\n"
            f"Val loss: {val_loss:.4f}, Val accuracy: {val_acc:.4f}\n"
        )
    def on_batch_end(self, batch, logs=None):
        batch_loss = logs.get("loss")
        batch_acc = logs.get("accuracy")
        print(f"  Batch {batch+1} - loss: {batch_loss:.4f}, acc: {batch_acc:.4f}", end="\r")

# ---------------- FUNCTION TO EXTRACT UNIQUE FILENAME FROM URL ----------------
def get_unique_filename(img_url, label, counter):
    # Extract photo ID from URL like /photos/123456/square.jpg -> 123456
    match = re.search(r'/photos/(\d+)', img_url)
    if match:
        photo_id = match.group(1)
        return f"photo_{photo_id}.jpg"  # Use .jpg as default extension
    # Fallback to label + counter
    return f"{label}_{counter}.jpg"

# ---------------- FUNCTION TO DOWNLOAD WITH RETRIES ----------------
def download_image(url, save_path, max_retries=3):
    for attempt in range(max_retries):
        try:
            print(f"  Downloading {os.path.basename(save_path)} (attempt {attempt+1})...")
            r = requests.get(url, stream=True, timeout=30)
            if r.status_code == 200:
                with open(save_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            else:
                print(f"  Failed: Status {r.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:
            print(f"  Failed attempt {attempt+1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    return False

# ---------------- FUNCTION TO PREPARE DATASET ----------------
def prepare_dataset(json_path, base_dir):
    print(f"Preparing dataset from {json_path} to {base_dir}...")
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found! Please ensure the JSON file exists.")
        return 0  # No images downloaded
    
    os.makedirs(base_dir, exist_ok=True)
    with open(json_path) as f:
        data = json.load(f)

    downloaded_count = 0
    skipped_count = 0
    total_items = len(data)
    print(f"Processing {total_items} items from JSON...")

    for idx, item in enumerate(data):
        if idx % 100 == 0:  # Progress indicator
            print(f"  Progress: {idx}/{total_items}")
        
        label = item.get("species_guess") or "unknown"
        img_url = item.get("photos")
        if not img_url:
            skipped_count += 1
            continue
        # Handle if photos is a list (take first URL)
        if isinstance(img_url, list):
            img_url = img_url[0] if img_url else None
        if not img_url:
            skipped_count += 1
            continue
        
        label_dir = os.path.join(base_dir, label)
        os.makedirs(label_dir, exist_ok=True)

        img_name = get_unique_filename(img_url, label, idx)
        save_path = os.path.join(label_dir, img_name)
        
        if os.path.exists(save_path):
            skipped_count += 1
            if skipped_count % 10 == 0:  # Reduce spam
                print(f"  Already exists (skipped {skipped_count}): {img_name}")
        else:
            if download_image(img_url, save_path):
                downloaded_count += 1
            else:
                skipped_count += 1
                print(f"  Failed to download after retries: {img_url}")

    print(f"Dataset preparation complete.")
    print(f"  - Total items processed: {total_items}")
    print(f"  - New images downloaded: {downloaded_count}")
    print(f"  - Skipped (existing or failed): {skipped_count}")
    return downloaded_count

# ---------------- TRAIN MODEL FUNCTION ----------------
def train_model():
    print("Starting model training...")

    # Prepare train and test directories
    train_downloaded = prepare_dataset(TRAIN_JSON, TRAIN_DIR)
    test_downloaded = prepare_dataset(TEST_JSON, TEST_DIR)
    
    total_images = train_downloaded + test_downloaded
    if total_images < 10:
        print(f"Warning: Only {total_images} images downloaded. Need more data for training. Skipping.")
        return

    # Image generators
    train_gen = ImageDataGenerator(rescale=1./255).flow_from_directory(
        TRAIN_DIR, target_size=(128,128), batch_size=32, class_mode="categorical"
    )
    test_gen = ImageDataGenerator(rescale=1./255).flow_from_directory(
        TEST_DIR, target_size=(128,128), batch_size=32, class_mode="categorical"
    )

    print(f"Training on {train_gen.samples} images across {train_gen.num_classes} classes.")
    print(f"Validation on {test_gen.samples} images.")

    # CNN Model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3,3), activation="relu", input_shape=(128,128,3)),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(64, (3,3), activation="relu"),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(train_gen.num_classes, activation="softmax")
    ])

    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    # Train with progress callback
    history = model.fit(
        train_gen,
        validation_data=test_gen,
        epochs=10,  # Exactly 10 epochs as requested
        callbacks=[TrainingProgress()]
    )

    # Save model, labels, and history
    model.save(MODEL_PATH)
    with open(LABELS_PATH, "w") as f:
        json.dump(list(train_gen.class_indices.keys()), f)
    with open(HISTORY_PATH, "w") as f:
        json.dump(history.history, f)

    print("Training completed! Model saved.")

# ---------------- LOAD OR CREATE MODEL ----------------
# Quick path verification
print(f"Looking for train JSON at: {TRAIN_JSON}")
print(f"Looking for test JSON at: {TEST_JSON}")
print(f"Train JSON exists? {os.path.exists(TRAIN_JSON)}")
print(f"Test JSON exists? {os.path.exists(TEST_JSON)}")

if os.path.exists(MODEL_PATH) and os.path.exists(LABELS_PATH):
    print("Loading existing model...")
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(LABELS_PATH) as f:
        labels = json.load(f)
    print(f"Model loaded with {len(labels)} classes: {labels}")
else:
    print("No model found, starting background training...")
    # Dummy model to keep API running during training
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(128,128,3)),
        tf.keras.layers.Dense(10, activation="softmax")
    ])
    labels = [f"Class{i}" for i in range(10)]
    # Start training in background thread
    threading.Thread(target=train_model, daemon=True).start()
    print("Dummy model active. Training in background... Check console for progress.")

# ---------------- PREDICT ENDPOINT ----------------
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    try:
        img = load_img(BytesIO(file.read()), target_size=(128,128))
        x = img_to_array(img)/255.0
        x = np.expand_dims(x, axis=0)
        preds = model.predict(x)
        class_idx = np.argmax(preds[0])
        confidence = float(preds[0][class_idx])
        return jsonify({"prediction": labels[class_idx], "confidence": confidence})
    except Exception as e:
        return jsonify({"error": "Prediction failed", "details": str(e)}), 500

# ---------------- RUN FLASK ----------------
if __name__ == "__main__":
    print("Starting Flask server on http://localhost:5000...")
    print("Use /predict endpoint for image classification.")
    app.run(debug=False, port=5000, host='0.0.0.0')  # debug=False for cleaner output
