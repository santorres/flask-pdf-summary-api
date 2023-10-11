from flask import Flask, request, jsonify
import os
import pdfplumber
import openai
import glob2
import textwrap
from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address
import json

# Function to open a file and read its content
def open_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()
    except Exception as e:
        print(f"An error occurred while opening the file '{filepath}': {str(e)}")
        return None

# Function to save content to a file
def save_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(content)
    except Exception as e:
        print(f"An error occurred while saving the file '{filepath}': {str(e)}")
        return False
    return True

# Function to convert PDFs to text
def convert_pdf2txt(src_dir, dest_dir):
    files = os.listdir(src_dir)
    files = [i for i in files if '.pdf' in i]
    for file in files:
        try:
            with pdfplumber.open(src_dir + file) as pdf:
                output = ''
                for page in pdf.pages:
                    output += page.extract_text()
                    output += '\n\nNEW PAGE\n\n'
                    print('Destination directory File Path:', dest_dir + file.replace('.pdf', '.txt'))
                save_file(dest_dir + file.replace('.pdf', '.txt'), output.strip())
        except Exception as oops:
            print("An error occurred:", oops, file)

# Function to interact with GPT-3 model
def gpt_3(prompt):
    chatbot = open_file('pdfbot.txt')

    messages = [
        {"role": "system", "content": chatbot},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        frequency_penalty=0,
        presence_penalty=0,
    )
    text = response['choices'][0]['message']['content']
    return text

# Create a Flask application instance
app = Flask(__name__)


# Initialize rate limiting with flask-limiter
limiter = Limiter(
    app,
    default_limits=["3 per minute"],
)

# Define a route for the endpoint with rate limiting
@app.route('/pdfsummary', methods=['POST'])
@limiter.limit("3 per minute")
def pdfsummary():
    try:
        # Load the OpenAI API key
        openai.api_key = open_file('openai_key.txt')

        print('Request received', request)

        # Get the PDF files from the request (use the key 'pdfs')
        pdf_files = request.files.getlist('pdfs')
        print("PDF files:", pdf_files)

        # Create a directory to save the results
        results_dir = 'RESULTS'
        os.makedirs(results_dir, exist_ok=True)

        # Initialize an empty list to store the results for each PDF
        pdf_results = []

        # Process each PDF separately
        for pdf_file in pdf_files:
            pdf_filename = pdf_file.filename
            pdf_name_without_extension = os.path.splitext(pdf_filename)[0]
            txt_filepath = os.path.join('textPDFs', pdf_filename.replace('.pdf', '.txt'))

            # Save the PDF file to a directory
            pdf_dir = 'PDFs'
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_path = os.path.join(pdf_dir, pdf_filename)
            pdf_file.save(pdf_path)

            # Convert the PDF to text
            convert_pdf2txt(pdf_dir + '/', 'textPDFs/')

            # Read the text file
            with open(txt_filepath, 'r', encoding='utf-8') as infile:
                alltext = infile.read()

            # Split the contents into chunks
            chunks = textwrap.wrap(alltext, 4000)

            # Initialize lists to store the results for each chunk
            chunk_analysis = []
            #chunk_notes = []
            #chunk_notes_summaries = []
            #chunk_essential_info = []
            #programming_languages = []
            #bootcamp_durations = []

            # Process each chunk
            for chunk in chunks:
                # Generate analysis for the chunk
                prompt = open_file('pdfprompt.txt').replace('<<ANALYSIS>>', chunk)
                prompt = prompt.encode(encoding='ASCII', errors='ignore').decode()
                analysis = gpt_3(prompt)
                chunk_analysis.append(analysis)

                # # Generate notes for the chunk
                # notes_prompt = open_file('pdfprompt2.txt').replace('<<NOTES>>', chunk)
                # notes = gpt_3(notes_prompt)
                # chunk_notes.append(notes)

                # # Generate notes summary for the chunk
                # notes_summary_prompt = open_file('pdfprompt3.txt').replace('<<NOTES>>', chunk)
                # notes_summary = gpt_3(notes_summary_prompt)
                # chunk_notes_summaries.append(notes_summary)

                # # Generate essential information for the chunk
                # essential_prompt = open_file('pdfprompt4.txt').replace('<<NOTES>>', notes_summary)
                # essential_info = gpt_3(essential_prompt)
                # chunk_essential_info.append(essential_info)

                # # Extract programming languages
                # programming_prompt = open_file('programming_prompt.txt').replace('<<CONTENT>>', chunk)
                # programming_result = gpt_3(programming_prompt)
                # programming_languages.append(programming_result)

                # # Extract bootcamp duration
                # duration_prompt = open_file('duration_prompt.txt').replace('<<CONTENT>>', chunk)
                # duration_result = gpt_3(duration_prompt)
                # bootcamp_durations.append(duration_result)

            # Create a dictionary for the result of this PDF
            pdf_result = {
                'filename': pdf_filename,
                'summaries': chunk_analysis,
               # 'notes': chunk_notes,
               # 'notes_summaries': chunk_notes_summaries,
               # 'essential_info': chunk_essential_info,
                # 'programming_languages': programming_languages,
                # 'bootcamp_durations': bootcamp_durations,
            }

            # Append the result to the list of PDF results
            pdf_results.append(pdf_result)

        # Save separate JSON result files for each PDF
        for pdf_result in pdf_results:
            pdf_filename = pdf_result['filename']
            result_filename = os.path.join(results_dir, f'results_{pdf_filename}.json')
            with open(result_filename, 'w', encoding='utf-8') as json_file:
                json.dump(pdf_result, json_file, ensure_ascii=False, indent=4)

        # Return the results as a JSON response
        return jsonify(pdf_results), 200
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({"error": str(e)}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=8000)
