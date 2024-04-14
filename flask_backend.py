import sqlite3
import numpy as np
import google.generativeai as genai
from implementation import create_key_value_dict
from docLoader import read_and_chunk_pdf




import sqlite3
import numpy as np


#THIS FILE FINDS THE BEST VECTOR TO MATCH

import numpy as np

def find_highest_similarity(key_value_dict, query_embedding):
  """
  This function finds the key in a key-value dictionary with the highest similarity
  to a given query embedding using the dot product.

  Args:
      key_value_dict: A dictionary where the key is a sequential number and the value
          is an embedded value.
      query_embedding: The query embedding to compare against.

  Returns:
      A tuple containing two elements:
          - The key in the dictionary with the highest similarity to the query embedding.
          - The highest similarity score between the query embedding and any value in the dictionary.
  """
  highest_similarity = -float('inf')  # Initialize with negative infinity
  highest_similarity_key = None

  for key, value in key_value_dict.items():
    similarity = np.dot(query_embedding, value)  # Calculate dot product
    if similarity > highest_similarity:
      highest_similarity = similarity
      highest_similarity_key = key

  return highest_similarity_key, highest_similarity

# Example usage (assuming you have functions to create embeddings)

model = 'models/embedding-001'
pdf_path = "/System/Volumes/Data/Users/amansikka/Documents/Google Hackathon/data.pdf"
chunks = read_and_chunk_pdf(pdf_path, chunk_size=5000)
embedding = genai.embed_content(model=model, content = chunks)
key_value = create_key_value_dict(embedding)

query = "What is electric field?"
query_embed = genai.embed_content(model=model, content = query)

KV = find_highest_similarity(key_value, query_embed)

print(KV)

# Example usage


