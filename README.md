# Mobile Device Assistant

A FastAPI service for extracting structured mobile phone details from free-form text and searching a small device catalog. Extraction uses a Groq-hosted chat model and validates its response with Pydantic. Catalog search combines BM25 keyword ranking with dense sentence embeddings and reciprocal-rank fusion.

## Features

- **Device extraction**: Convert a short description into brand, model, specifications, release year, and price tier.
- **Hybrid catalog search**: Retrieve matching device descriptions using lexical and semantic rankings.
- **Interactive API docs**: Explore and call endpoints through FastAPI's Swagger UI.

## Project structure

```text
mobile-device-assistant/
├── mobile-device-assistant/
│   ├── app/
│   │   ├── data/          # Sample device catalog
│   │   ├── prompts/       # Extraction prompt templates
│   │   ├── schema/        # Pydantic request and response models
│   │   ├── services/      # Extraction and hybrid search
│   │   └── utils/         # Embeddings and BM25 index
│   ├── .env.example
│   └── requirements.txt
├── pyproject.toml
└── README.md
```

## Requirements

- Python **3.14.6 or newer**, as declared in the root `pyproject.toml`.
- A Groq API key and a model name accepted by your Groq account for the `/extract` endpoint.
- Internet access the first time the sentence-transformers embedding model is loaded, unless it is already cached.

## Setup

From the project root, create and activate a virtual environment, then install the application dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r mobile-device-assistant/requirements.txt groq
```

macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install -r mobile-device-assistant/requirements.txt groq
```

The extraction implementation imports the Groq Python client, so `groq` is installed explicitly above.

Create `mobile-device-assistant/.env` from the example file and set your credentials:

```dotenv
Groq_API_KEY=your_groq_api_key
MODEL_NAME=your_groq_model_name
```

The application loads this file when the extraction service is imported. Keep your API key private and do not commit the populated `.env` file.

## Run the API

Start the development server from the nested application directory:

```bash
cd mobile-device-assistant
python -m uvicorn app.main:app --reload
```

By default, the service is available at <http://127.0.0.1:8000>. Open <http://127.0.0.1:8000/docs> for interactive API documentation.

## API

### `POST /extract`

Extract a device record from text. The request text must be non-empty and no longer than 500 characters.

Request:

```json
{
  "text": "Apple iPhone 15 Pro Max, released in 2023, flagship tier, 256 GB storage and 48 MP camera"
}
```

The response is a validated device object:

```json
{
  "brand": "Apple",
  "model": "iPhone 15 Pro Max",
  "specs": {
    "storage": "256 GB",
    "camera": "48 MP"
  },
  "release_year": 2023,
  "price_tier": "flagship"
}
```

Allowed price tiers are `budget`, `mid-range`, and `flagship`. Invalid input is rejected; extraction requests containing phrases such as “ignore previous” or “system prompt” are also rejected by the input guard.

### `POST /search`

Search the bundled sample device catalog. The request query must be non-empty and no longer than 500 characters. Use the optional `top_k` query parameter to control the number of results (default: 3).

Request:

```json
{
  "q": "phone for mobile gaming with a fast display"
}
```

Example call:

```text
POST /search?top_k=2
```

The response contains catalog descriptions and their fusion scores:

```json
{
  "results": [
    {
      "document": "ASUS ROG Phone 7 is designed for mobile gaming with a 165Hz display.",
      "score": 0.0325
    }
  ]
}
```


## Demo

This section demonstrates the main capabilities of the Mobile Device Assistant API, including structured information extraction, prompt-injection input validation, and semantic search.

### 1. Information Extraction

Extract structured smartphone information from natural-language input through the API.

![Information Extraction Demo](<img width="1209" height="642" alt="image" src="https://github.com/user-attachments/assets/4cc2a90f-ff9d-4bcf-a4e5-c4f9ce43c1d5" />)
![Information Extraction Demo_](<img width="1209" height="776" alt="image" src="https://github.com/user-attachments/assets/fde24dad-3dc5-40af-a6d2-ab9128215068" />)

### 2. Prompt Injection Validation

Test how the API handles potentially malicious or unauthorized instructions. The demonstrated request is rejected with a `400 Bad Request` response.

![Prompt Injection Validation Demo](docs/screenshots/prompt-injection.png)

### 3. Semantic Search

Submit a natural-language query and retrieve relevant documents with associated similarity scores.

![Semantic Search Demo](docs/screenshots/search.png)

### Full Demonstration

For the complete request and response examples, see the [Demo Documentation](docs/demo.pdf).





## Development notes

The app creates its BM25 index and document embeddings when `app.main` is imported. Search therefore does not require a Groq key, but extraction does. The `/extract` endpoint returns a structured device response, while model or provider errors are surfaced as HTTP 500 responses.
