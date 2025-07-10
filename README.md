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

### Configuration

This application requires an API key for the xAI service. You must create a `.env` file in the root directory of the project (the same directory as `README.md`) and add your API key to it.

Create a file named `.env` with the following content, replacing `YOUR_XAI_API_KEY` with your actual key:

```
XAI_API_KEY=YOUR_XAI_API_KEY
```

## Running the Application

You can run the application either directly using `uvicorn` or by using Docker.

### Running with Uvicorn (Local Development)

1.  **Ensure your `.env` file is present in the root directory.**
2.  **Start the backend server:**

    ```bash
    uvicorn app.main:app --reload
    ```

3.  **Access the frontend:**

    Open your web browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Running with Docker

1.  **Build the Docker image:**

    Navigate to the root directory of the project in your terminal and run:

    ```bash
    docker build -t press-notes-agent .
    ```

2.  **Run the Docker container:**

    Ensure your `.env` file is present in the root directory. Then, run the container, mapping the port and loading the environment variables:

    ```bash
    docker run -p 8000:8000 --name press-notes-app --env-file ./.env press-notes-agent
    ```

3.  **Access the frontend:**

    Open your web browser and navigate to [http://localhost:8000](http://localhost:8000).

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
