import google.generativeai as genai
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import shutil
import PyPDF2


#THIS FILE READS PDF IN 

def read_and_chunk_pdf(pdf_path, chunk_size=5000):
    try:
        # Open the PDF file
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            full_text = ""

            # Extract text from each page
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:  # Ensure that text extraction is successful
                    full_text += page_text + " "  # Add a space between texts of different pages

        # Clean text by replacing multiple whitespaces with a single space
        clean_text = ' '.join(full_text.split())

        # Split the text into chunks
        chunks = [clean_text[i:i + chunk_size] for i in range(0, len(clean_text), chunk_size)]

        return chunks
    except Exception as e:
            print(f"Failed to process PDF {pdf_path}: {str(e)}")
            return []

def count_pdf_chunks(pdf_path, chunk_size=5000):
    # Open the PDF file
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        full_text = ""

        # Extract text from each page
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # Ensure that text extraction is successful
                full_text += page_text + " "  # Add a space between texts of different pages

    # Clean text by replacing multiple whitespaces with a single space
    clean_text = ' '.join(full_text.split())

    # Calculate the number of chunks
    num_chunks = (len(clean_text) + chunk_size - 1) // chunk_size  # This ensures all text is counted

    return num_chunks




app = Flask(__name__)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = os.path.join('/path/to/save', filename)
        file.save(file_path)
        chunks = read_and_chunk_pdf(file_path)
        return jsonify({"chunks": chunks}), 200
    else:
        return jsonify({"error": "Unsupported file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)


#main

pdf_path = "/System/Volumes/Data/Users/amansikka/Documents/Google Hackathon/data.pdf"
chunks = read_and_chunk_pdf(pdf_path, chunk_size=5000)

#Now you have the chunks ready for further processing or analysis
#for index, chunk in enumerate(chunks):
    #print(f"Chunk {index + 1}:", chunk[:1000])  # Print the first 100 characters of each chunk for preview

number_of_chunks = count_pdf_chunks(pdf_path, 5000)
print(f"Number of chunks in the PDF: {number_of_chunks}")





