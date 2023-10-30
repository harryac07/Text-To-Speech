#from playsound import playsound

import requests
import os

BASE_URL = "http://127.0.0.1:8000"
END_POINT = "image-to-speech"

language = 'sv'

file = open('five.jpg', 'rb')

payload = {'language': language}

response = requests.post(f'{BASE_URL}/{END_POINT}', params = payload, files = {'file': file})

with open('speech.mp3', 'wb') as f:
  f.write(response.content)
