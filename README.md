# Press Notes Agent

This project is a FastAPI application that automates the process of creating press notes from a list of article URLs. It fetches content, extracts key information, and generates a consolidated PDF document.

## Features

- **Content Fetching:** Retrieves article content from a list of URLs.
- **Information Extraction:** Uses a large language model to extract key information from the articles.
- **PDF Generation:** Creates a PDF document with the extracted press notes.
- **Web Interface:** A simple web interface to interact with the application.

## Getting Started

### Local Environment

This project uses the following local setup flow:

```text
pyenv -> Python 3.11.9
      -> .venv
      -> requirements.txt
      -> requirements-dev.txt (for tests)
```

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/press-notes-agent.git
   cd press-notes-agent
   ```

2. **Install and select Python 3.11.9 with pyenv:**

   ```bash
   pyenv install 3.11.9
   pyenv local 3.11.9
   python --version
   ```

3. **Create the project virtual environment:**

   ```bash
   python -m venv .venv
   ```

4. **Activate the virtual environment:**

   ```bash
   source .venv/bin/activate
   ```

5. **Install dependencies from `requirements.txt`:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Install development dependencies when you want to run tests:**

   ```bash
   pip install -r requirements-dev.txt
   ```

### Configuration

This application requires an API key for the xAI service. You must create a `.env` file in the root directory of the project (the same directory as `README.md`) and add your API key to it.

Create a file named `.env` with the following content, replacing `YOUR_XAI_API_KEY` with your actual key:

```
XAI_API_KEY=YOUR_XAI_API_KEY
```

## Running the Application

1. **Activate the virtual environment if it is not already active:**

   ```bash
   source .venv/bin/activate
   ```

2. **Ensure your `.env` file is present in the project root.**

3. **Start the application:**

   ```bash
   python -m uvicorn app.main:app --reload
   ```

4. **Access the frontend:**

   Open your web browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Running Tests

1. **Activate the virtual environment:**

   ```bash
   source .venv/bin/activate
   ```

2. **Install development dependencies if needed:**

   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Run the test suite:**

   ```bash
   pytest
   ```

- **`GET /`**: Serves the main HTML page.
- **`POST /extract-content`**: Extracts content from a list of URLs and returns the extracted articles and a path to the generated PDF.
  - **Request Body:**
    ```json
    {
      "urls": [
        "https://example.com/article1",
        "https://example.com/article2"
      ]
    }
    ```
- **`GET /download/{pdf_filename}`**: Downloads the generated PDF file.

## Project Structure

```
.
├── app
│   ├── __init__.py
│   ├── logging_config.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── article.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── content_fetcher.py
│   │   ├── pdf_generator.py
│   │   ├── press_notes_orchestrator.py
│   │   └── xai_client.py
│   ├── static
│   │   └── index.html
│   └── utils
│       └── html_cleaner.py
├── Dockerfile
├── README.md
├── requirements-dev.txt
├── requirements.txt
└── tests
    └── __init__.py
```
