import os
os.environ["TFDS_DATA_DIR"] = "C:/tfds-data"

import tensorflow as tf
import tensorflow_datasets as tfds

# 1. Load the tf_flowers dataset
(ds_train, ds_test), ds_info = tfds.load(
    'tf_flowers',
    split=['train[:80%]', 'train[80%:]'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True
)

# 2. Preprocessing function
IMG_SIZE = 224  # Common size for pre-trained models

def preprocess(image, label):
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
    image = image / 255.0
    return image, label

ds_train = ds_train.map(preprocess).shuffle(1000).batch(32).prefetch(tf.data.AUTOTUNE)
ds_test = ds_test.map(preprocess).batch(32).prefetch(tf.data.AUTOTUNE)

# 3. Build CNN model
num_classes = ds_info.features['label'].num_classes

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(128, 3, activation='relu'),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# 5. Train model
history = model.fit(ds_train, validation_data=ds_test, epochs=20)
model.save("src/data/flower_classifier.h5")



test_loss, test_acc = model.evaluate(ds_test)
print(f"Test Accuracy: {test_acc:.2f}")

