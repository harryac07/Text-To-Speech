from fastapi import FastAPI
from num2words import num2words

app = FastAPI()

@app.get("/number-to-word")
async def number_to_word(number: int = 0, language = 'en'):
  word = num2words(number, lang = language)
  return {
    "number": number, 
    "word": word, 
    "language": language
  }