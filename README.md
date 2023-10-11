# PDF Analysis and Summary with ChatGPT

## Overview

**Author**: Santiago Torres
The PDF Analysis with ChatGPT is a web application that harnesses the power of AI and the Flask framework to simplify the process of analyzing and extracting valuable insights from PDF documents. This tool is not limited to summarization; it allows you to have dynamic conversations with OpenAI's GPT-3.5 Turbo, making it ideal for a wide range of use cases, from extracting summaries to answering questions, generating notes, and more. The application provides a RESTful API endpoint that accepts PDF files as input and returns a JSON object containing the generated analyses, summaries, notes, and additional content.

The app uses the pdfplumber library to extract text from PDF files, and the openai library to interact with the GPT-3.5-turbo API. The application is built using the Flask web framework, making it easy to deploy and use.

## Features

* **Efficient PDF-to-Text Conversion** : The application seamlessly converts PDF documents into text, making the content easily accessible for analysis by ChatGPT.
* **Dynamic AI Conversations** : Harnessing the power of OpenAI's GPT-3.5 Turbo, the tool enables dynamic conversations with the AI model. You can customize prompts to engage in conversations and receive tailored responses.
* **Rate Limiting** : To ensure fair usage, the application incorporates rate limiting, allowing a maximum of three requests per minute.
* **Customizable Analysis** : You can customize the prompts used for analysis by editing the prompt files (e.g., 'pdfprompt.txt') to fit your specific needs.
* Generate notes and summaries of notes from the text.
* Provide a RESTful API endpoint for easy integration with other applications.

## Prerequisites

To use the PDF Summary Generator, you need the following:

Python 3.6 or higher

An OpenAI API key (you can obtain one by signing up for an account on the OpenAI platform)

The following Python libraries: flask, pdfplumber, openai, glob2, and textwrap

## Getting Started

1. Clone this repository to your local machine.
2. Install the necessary dependencies by running `pip install -r requirements.txt`.
3. Set up your OpenAI API key by creating an 'openai_key.txt' file with your key.
4. Customize the analysis prompts and other configuration files as needed.
5. Run the application with `python app.py`.
6. Send POST requests to the `/pdfsummary` endpoint with your PDF files to receive dynamic AI-based analyses.

(Optional) Customize the GPT-3.5-turbo prompts and chatbot responses by modifying the text files in the project directory.

## Example Usage

You can use the application to analyze PDF documents with the following steps:

1. Ensure you have the necessary dependencies installed and the application is running.
2. Send a POST request to `http://localhost:8000/pdfsummary` with your PDF files attached.
3. Engage in dynamic conversations with ChatGPT to explore and analyze the content of the uploaded PDFs.

To run the PDF Summary Generator application, execute the following command in the project directory:

```
python main.py
```

This will start the Flask development server, and the application will be accessible at http://localhost:8000/pdfsummary.

To use the API endpoint, send a POST request to http://localhost:8000/pdfsummary with the PDF files you want to summarize as multipart file attachments. The endpoint will return a JSON object containing the generated summaries, notes, and additional content.

You can use tools like Postman or curl to send requests to the API endpoint.

Example Request

```
curl -X POST -F "pdfs=@example.pdf" http://localhost:8000/pdfsummary
```

Example Response

```
{

  "summary": "This is the summary of the PDF document...",

  "notes": "These are the notes extracted from the document...",

  "notes_summary": "This is the summary of the notes...",

  "essential_info": "This is the essential information extracted..."

}
```

## Contributing

Contributions to this project are welcome! Whether you'd like to improve the AI prompts, enhance the user interface, or add new features, your input is valuable. Please follow our [contributing guidelines](https://chat.openai.com/c/CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](https://chat.openai.com/c/LICENSE) file for details.Disclaimer

## Aknowledgements

* This project was made possible with the help of the [Flask](https://flask.palletsprojects.com/en/2.0.x/) web framework & Anthoine
* Conversational capabilities are powered by [OpenAI&#39;s GPT-3.5 Turbo](https://beta.openai.com/signup/).

Unlock the full potential of your PDF documents by engaging in insightful conversations and analyses with ChatGPT. Simplify your PDF analysis process and leverage AI to extract valuable information from your documents.
