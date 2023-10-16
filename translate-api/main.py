from fastapi import FastAPI
from fastapi.responses import FileResponse
from num2words import num2words
from gtts import gTTS
from fastapi.middleware.cors import CORSMiddleware

import os

app = FastAPI()

# Define the CORS settings
origins = [
    "http://localhost", 
    "http://localhost:3000",
]

# Add the CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods if needed
    allow_headers=["*"],  # You can specify specific headers if needed
)

@app.get("/")
async def root():
  return {"message": "Hello World"}
	
@app.get("/translate")
async def translate(number: int = 0, language = 'en'):
  word = num2words(number, lang = language)
  return {"number": number, "language": language, "word": word}

@app.get("/speak")
async def translate(number: int = 0, language = 'en'):
  word = num2words(number, lang = language)
  myobj = gTTS(text=word, lang=language, slow=False)
  myobj.save("welcome.mp3") 
  print('saved')
  return FileResponse(
    os.path.dirname(__file__) + '/welcome.mp3',
    media_type="audio/mpeg"
  )