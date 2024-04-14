from docLoader import read_and_chunk_pdf
import google.generativeai as genai
import numpy as np
import pandas as pd
import sqlite3
import json

import os
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])



instruction = "You are a friendly electricity and magnetism Professor with a very methodical teaching style"
model = genai.GenerativeModel(
    "models/gemini-1.5-pro-latest",
    system_instruction=instruction,
)


pdf_path = "/System/Volumes/Data/Users/amansikka/Documents/Google Hackathon/data.pdf"
chunks = read_and_chunk_pdf(pdf_path, chunk_size=5000)

for index, chunk in enumerate(chunks):
    chunkSTR = chunk[:100]

#df = pd.DataFrame(chunks)
#df.columns = ['Title', 'Text']

#THIS FUNCTION POPULATED THE DB

def create_key_value_dict(chunks):
  """
  This function loops through a list of text chunks and creates a dictionary
  where the key is a sequential number and the value is the chunk of text.

  Args:
      chunks: A list of text chunks.

  Returns:
      A dictionary where the key is a sequential number and the value is the chunk of text.
  """
  key_value_dict = {}
  for i, chunk in enumerate(chunks):
    key_value_dict[i] = chunk
  return key_value_dict




model = 'models/embedding-001'
embedding = genai.embed_content(model=model, content = chunks)
dictionary = create_key_value_dict(embedding['embedding'])
