import streamlit as st
import pandas as pd
from io import StringIO
import requests
import google.generativeai as genai
import os
from PIL import Image
from google.cloud import texttospeech

st.title("Generate a Lecture")
# Access API key from environment variable (ensure it's named "API_KEY")
api_key = "api_key"

#text to speech api key:
api_KEY = "api_key"

# File uploader for user input
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

#instantiate a client
client = texttospeech.TextToSpeechClient()


if (uploaded_file is not None) & (api_key is not None):
  # Read the uploaded image data
  image_data = uploaded_file.read()
  # Convert image data to PIL Image object
  img = Image.open(uploaded_file)

  #if there is an api key...and if it's successful
  genai.configure(api_key=api_key)
  model = genai.GenerativeModel('gemini-pro-vision')
  prompt = "You are a Physics: Electricity and Magnetism professor at MIT. I missed my lecture today on the inputted lecture notes. Can you be a physics II lecturer and lecture those concepts to me. "
  response = model.generate_content([prompt, img])
  transcript = response.text

    # Set the text input to be synthesized
  synthesis_input = texttospeech.SynthesisInput(text=transcript)

  # Build the voice request, select the language code ("en-US") and the ssml voice gender ("neutral")
  voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Journey-D"
)

  # Select the type of audio file you want returned
  audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

  # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
  speechResponse = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

  # The response's audio_content is binary.
  with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(speechResponse.audio_content)
    print('Audio content written to file "output.mp3"')
  
  # Play the downloaded audio file automatically
  st.audio("output.mp3", format="audio/mpeg", loop=True)




  st.write(transcript)
