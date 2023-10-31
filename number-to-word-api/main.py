from fastapi import FastAPI
from num2words import num2words
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

@app.get("/number-to-word")
async def number_to_word(number: int = 0, language = 'en'):
  word = num2words(number, lang = language)
  return {
    "number": number, 
    "word": word, 
    "language": language
  }