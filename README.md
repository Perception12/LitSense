# LitSense – AI-Powered Literary Recommendation Backend

LitSense is an AI-powered literary recommendation and decision-support system designed to help users make informed book-buying decisions based on their preferences and reading history. This repository contains the **backend inference engine and API**, responsible for processing user inputs, analyzing book cover images, and generating personalized recommendations.

This backend is designed to be frontend-agnostic and is containerized using Docker for easy deployment.

---

## Key Features

* **Personalized Book Recommendations** based on:

  * Favorite genres
  * Reading history
  * Age, location, and occupation

* **Book Cover Image Understanding**

  * Extracts title, author(s), and genre(s) from a book cover image using an LLM-based vision pipeline

* **Inference Engine Abstraction**

  * Clean separation between API layer and AI logic
  * Prompt-driven inference using Jinja templates

* **RESTful API**

  * Single inference endpoint designed for frontend integration

* **Dockerized Deployment**

  * Consistent runtime across environments

---

## Project Structure

```text
LitSense/
├── api/
│   ├── app.py                  # Flask application entry point
│   ├── routes/
│   │   └── inference.py         # /inference endpoint
│   └── services/
│       └── inference_service.py # Bridge between API and inference engine
│
├── inference_engine/
│   ├── engine.py                # Core BookInferenceEngine
│   ├── utils.py                 # Data transformation pipelines
│   ├── data_models.py                 # Data transformation pipelines  
│   └── prompts/
│       ├── extract_book_information.jinja
│       └── preference_prompt.jinja
│
├── requirements.txt
├── dockerfile
├── docker-compose.yml
├── .env                         # Environment variables (not committed)
└── README.md
```

---

## Inference Flow (High Level)

1. Client sends a **POST** request with:

   * A book cover image
   * User information (JSON)

2. API validates inputs and forwards them to the inference service

3. Inference engine pipeline:

   * Loads and encodes the image
   * Extracts book metadata from the image
   * Compares extracted data with user preferences
   * Produces a recommendation and explanation

4. API returns a structured JSON response

---

## API Usage

### Endpoint

```http
POST /api/inference
```

### Request (multipart/form-data)

| Field     | Type   | Description                     |
| --------- | ------ | ------------------------------- |
| image     | File   | Book cover image                |
| user_info | String | JSON string of user preferences |

#### Example `user_info`

```json
{
  "favorite_genres": ["Fantasy", "Science Fiction"],
  "reading_history": ["Dune", "The Hobbit"],
  "age": 25,
  "location": "Nigeria",
  "occupation": "Student"
}
```

### Response (200 OK)

```json
{
  "recommended": true,
  "confidence": 0.87,
  "reason": "The book aligns strongly with the user's preferred genres and past reading history."
}
```

### Error Responses

| Status | Meaning                           |
| -----: | --------------------------------- |
|    400 | Missing or invalid input          |
|    500 | Internal server / inference error |

---

## Prompt System

The inference engine uses **Jinja-based prompt templates**:

* `extract_book_information.jinja`

  * Extracts title, author(s), and genre(s) from a book cover image

* `preference_prompt.jinja`

  * Determines alignment between user preferences and extracted book metadata

This design allows prompt updates without changing application logic.

---

## Running with Docker

### Build and Run

```bash
docker-compose up --build
```

The API will be available at:

```
http://localhost:8080
```

### Environment Variables

Environment variables are loaded securely using `.env` and `docker-compose`:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## Testing

You can test the API using:

* PowerShell (`Invoke-WebRequest`)
* curl (Linux/macOS)
* Postman
* Any frontend client

The backend expects **multipart/form-data**, not raw JSON.

---

## Design Principles

* Clear separation of concerns (API vs inference engine)
* Stateless request handling
* Pipeline-based transformations
* Prompt-driven reasoning
* Docker-first deployment mindset

---

## Next Steps (Frontend)

The backend is now stable and ready for frontend integration. Suggested frontend features:

* Image upload UI
* User preference form
* Recommendation explanation view
* Confidence score visualization

---

## Status

✅ Backend inference engine complete
✅ Docker deployment working
🚧 Frontend development in progress

---

If you have questions or want to extend the system (auth, persistence, analytics, etc.), this backend is designed to scale with you.

