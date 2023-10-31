from fastapi import FastAPI, File, UploadFile, Response
import circuitbreaker
import requests
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S %z', level=logging.INFO)
logger = logging.getLogger()

class BackendCircuitBreaker(circuitbreaker.CircuitBreaker):
    FAILURE_THRESHOLD = 5
    RECOVERY_TIMEOUT = 60
    EXPECTED_EXCEPTION = requests.RequestException

@BackendCircuitBreaker()    
def call_image_to_number(filename, data):
  BASE_URL = "http://localhost:3001"
  END_POINT = "predict"
  response = requests.post(f"{BASE_URL}/{END_POINT}", files = {'file':(filename, data)})
  data = {}
  if response.status_code == 200:
    data = response.json()['number']
  return data

@BackendCircuitBreaker()    
def call_number_to_word(number, language):
  BASE_URL = "http://localhost:3003"
  END_POINT = "number-to-word"
  payload = {'number': number, 'language': language }
  response = requests.get(f"{BASE_URL}/{END_POINT}", params=payload)
  data = {}
  if response.status_code == 200:
    data = response.json()['word']
  return data

@BackendCircuitBreaker()    
def call_word_to_speech(word, language):
  BASE_URL = "http://localhost:3002"
  END_POINT = "word-to-speech"
  payload = {'word': word, 'language': language }
  response = requests.get(f"{BASE_URL}/{END_POINT}", params=payload)
  data = []
  if response.status_code == 200:
    with open('speech.mp3', 'wb') as f:
      f.write(response.content) 
    data = response.content
  return data

@app.post("/image-to-speech")
def image_to_speech(file: UploadFile = File(...), language = 'en'):
  logging.info(f'File received: {file.filename}')
  try:  
    number = call_image_to_number(file.filename, file.file.read())
    logging.info(f'Number discovered: {number}')
    word = call_number_to_word(number, language)
    logging.info(f'Number converted to word: {word}')
    speech = call_word_to_speech(number, language)
    return Response(speech)
    '''
    return {
      "status_code": 200,
      "success": True,
      "message": "Success converting image into speech", 
      "data": speech
    }
    '''
  except circuitbreaker.CircuitBreakerError as e:
    return {
      "status_code": 503,
      "success": False,
      "message": f"Circuit breaker active: {e}"
    }
  except requests.exceptions.ConnectionError as e:
    return {
      "status_code": 500,
      "success": False,
      "message": f"Failed to resolve image: {e}"
    }