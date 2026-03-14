import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models

img_size = 224
batch_size = 32
epochs = 3

# Dataset folder (full PlantVillage color images)
train_dir = os.path.join("plantvillage", "color")

# Output paths
model_out = os.path.join("model", "plant_disease_model.h5")
labels_out = os.path.join("model", "labels.txt")

os.makedirs("model", exist_ok=True)

datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    train_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    subset="training"
)

val_data = datagen.flow_from_directory(
    train_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    subset="validation"
)

base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

x = layers.GlobalAveragePooling2D()(base_model.output)
x = layers.Dense(128, activation="relu")(x)
output = layers.Dense(train_data.num_classes, activation="softmax")(x)

model = models.Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(train_data, validation_data=val_data, epochs=epochs)

model.save(model_out)

# Save class labels in the exact order used during training
# (flow_from_directory uses alphabetical folder order)
labels_sorted = [k for k, _ in sorted(train_data.class_indices.items(), key=lambda x: x[1])]
with open(labels_out, "w", encoding="utf-8") as f:
    f.write("\n".join(labels_sorted))

print(f"Saved model to {model_out}")
print(f"Saved labels to {labels_out}")
