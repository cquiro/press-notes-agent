# Press Notes Agent

This project is a FastAPI application that automates the process of creating press notes from a list of article URLs. It fetches content, extracts key information, and generates a consolidated PDF document.

## Features

- **Content Fetching:** Retrieves article content from a list of URLs.
- **Information Extraction:** Uses a large language model to extract key information from the articles.
- **PDF Generation:** Creates a PDF document with the extracted press notes.
- **Web Interface:** A simple web interface to interact with the application.

## Getting Started

### Prerequisites

- Python 3.8+
- Pip

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/press-notes-agent.git
    cd press-notes-agent
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Start the backend server:**

    ```bash
    uvicorn app.main:app --reload
    ```

2.  **Access the frontend:**

    Open your web browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Endpoints

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
├── requirements.txt
└── tests
    └── __init__.py
```
