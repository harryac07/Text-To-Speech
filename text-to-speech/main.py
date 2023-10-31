import numpy as np
import logging
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.datasets import mnist  # Import MNIST from TensorFlow
from tensorflow.keras.models import Sequential  # Use the TensorFlow version
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten  # Use the TensorFlow version
from tensorflow.keras.utils import to_categorical  # Use the TensorFlow version
from tensorflow.keras.optimizers import SGD  # Use the TensorFlow version
from PIL import Image, ImageOps 
from tensorflow.keras import models  # Use the TensorFlow version
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Define the CORS settings
origins = ["*"]

# Add the CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods if needed
    allow_headers=["*"],  # You can specify specific headers if needed
)

# Load MNIST dataset using TensorFlow
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Preprocess the data as needed
train_images = (train_images / 255) - 0.5
test_images = (test_images / 255) - 0.5

train_images = np.expand_dims(train_images, axis=3)
test_images = np.expand_dims(test_images, axis=3)

# ... (your model, training, and model loading code) ...
'''
model = Sequential([
  Conv2D(8, 3, input_shape=(28, 28, 1), use_bias=False),
  MaxPooling2D(pool_size=2),
  Flatten(),
  Dense(10, activation='softmax'),
])

model.summary()

model.compile(SGD(lr=.005), loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(
  train_images,
  to_categorical(train_labels),
  batch_size=1,
  epochs=3,
  validation_data=(test_images, to_categorical(test_labels)),
)

model.save('numbers')
'''

model = models.load_model('numbers')

@app.get("/predict_simple")
async def predict_simple():
  im = Image.open(r"five.jpg").convert('L').resize((28, 28))
  im = ImageOps.invert(im)
  
  img = np.array(im)
  img = (img / 255) - 0.5
  img = np.expand_dims(img, axis = 0)

  predictions = model.predict(img)
  label = np.argmax(predictions, axis = 1)
  return {"number": str(label[0])}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        logging.info(f'File received: {file.filename}')
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
        
        im = Image.open(file.filename).convert('L').resize((28, 28))
        im = ImageOps.invert(im)
        
        img = np.array(im)
        img = (img / 255) - 0.5
        img = np.expand_dims(img, axis=0)

        predictions = model.predict(img)
        label = np.argmax(predictions, axis=1)
        logging.info(f'Number received: {str(label[0])}')
        response_data = {"number": str(label[0])}

        return JSONResponse(content=response_data)
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        return JSONResponse(content={"message": "There was an error uploading or processing the file"}, status_code=500)
    finally:
        file.file.close()