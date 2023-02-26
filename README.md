# metaplayers-hackathon-2023

## Frontend

- initialize
  - ```bash
    cd frontend
    npm install
    ```
- start
  - ```bash
    npm start
    ```
  

## Backend
- prerequisites
  - Poetry (https://python-poetry.org)
  - OpenAI api key
- initialize
  - ```bash
    cd backend
    poetry install
    ```
  - Copy `.env.example` to `.env` and fill values.
- start
  - ```bash
    poetry run start
    
    poetry run uvicorn backend.document_retrieval.api:app --port 8001
    
    poetry run uvicorn backend.server.api:app --host 0.0.0.0
    ```
- scraping
  - `mkdir -p data/scraped/raw`
  - `poetry run scrape-all`
