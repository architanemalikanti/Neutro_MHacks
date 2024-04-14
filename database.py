import textwrap
import numpy as np
import pandas as pd
import os
import google.generativeai as genai
import google.ai.generativelanguage as glm
from docLoader import read_and_chunk_pdf
from implementation import create_key_value_dict



genai.configure(api_key=os.environ['GOOGLE_API_KEY'])


model = 'models/embedding-001'
pdf_path = "/System/Volumes/Data/Users/amansikka/Documents/Google Hackathon/data.pdf"
chunks = read_and_chunk_pdf(pdf_path, chunk_size=5000)
embedding = genai.embed_content(model=model, content = chunks)
key_value = create_key_value_dict(embedding)

query = "What is electric field?"
query_embed = genai.embed_content(model=model, content = query)

df = pd.DataFrame(embedding, columns=['Embedding'])
if len(df.columns) == 2:
    df.columns = ['Title', 'Text']
elif len(df.columns) == 1:
    df.columns = ['Embedding']  # If only one column, name it appropriately
else:
    print("Unexpected number of columns in DataFrame")
    
print(df.head())  # To see the first few rows and verify structure


def embed_fn(title, text):
  return genai.embed_content(model=model,
                             content=text,
                             task_type="retrieval_document",
                             title=title)["embedding"]

df['Embeddings'] = df.apply(lambda row: embed_fn(row['Title'], row['Text']), axis=1)
embeddings = []

for chunk in chunks:
    # Assuming chunk is a string of text from the PDF
    embedding = genai.embed_content(model=model, content=chunks)
    current_df = pd.DataFrame([{'Embedding': embedding}])
    # Add the embedding to the DataFrame
    df = pd.concat([df, current_df], ignore_index=True)


def find_best_passage(query, dataframe):
  """
  Compute the distances between the query and each document in the dataframe
  using the dot product.
  """
  query_embedding = genai.embed_content(model=model,
                                        content=query,
                                        task_type="retrieval_query")
  dot_products = np.dot(np.stack(dataframe['Embeddings']), query_embedding["embedding"])
  idx = np.argmax(dot_products)
  return dataframe.iloc[idx]['Text'] # Return text from index with max value

passage = find_best_passage(query, df)
passage

