🌌 Astro-Insight API

A production-ready micro-service that turns birth details into personal, uplifting horoscopes powered by Google Gemini 1.5-Flash and served over FastAPI.

| Feature               | Implementation                                         |
| --------------------- | ------------------------------------------------------ |
| **Zodiac Sign Logic** | deterministic date-range rules (`core/zodiac.py`)      |
| **LLM Engine**        | Google Gemini 1.5-Flash via **LangChain-Google-GenAI** |
| **Translation**       | Google-Translate **+ cache** (`core/translator.py`)    |
| **Caching**           | 1-hour in-memory TTL (`core/cache.py`)                 |
| **API Framework**     | **FastAPI** with auto-generated OpenAPI docs           |
| **Secrets**           | `.env` file (Twelve-Factor App)                        |
| **Hot-reload**        | Uvicorn dev server                                     |


Architecture

Client ──HTTP──► FastAPI ─►Validation─►Zodiac ─►LLM(Gemini) ─► Translate ─► Cache ─► JSON Response

| Step            | What happens                                                                                                   | Stack                      |
| --------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------- |
| **Ingress**     | FastAPI route `/predict` accepts the exact sample JSON `{name, birth_date, birth_time, birth_place, language}` | **FastAPI**                |
| **Validation**  | Pydantic `BirthData` rejects bad payloads with `422`                                                           | **Pydantic**               |
| **Zodiac**      | Date-range table returns the sign in O(1)                                                                      | **core/zodiac.py**         |
| **LLM**         | LangChain’s `ChatGoogleGenerativeAI` wraps Gemini 1.5-Flash                                                    | **LangChain-Google-GenAI** |
| **Translation** | Google-Translate via `googletrans==3.1.0a0`                                                                    | **core/translator.py**     |
| **Caching**     | LRU-dict keyed on `(sign, lang)` for 1 hour                                                                    | **core/cache.py**          |
| **Response**    | FastAPI serializes `{zodiac, insight, language}` in < 1 s                                                      | **FastAPI**                |


1. **Ingress** – FastAPI route `/predict` receives a `POST` request with JSON:  
   ```json
   {
     "name": "John Doe",
     "birth_date": "1990-01-01",
     "birth_time": "12:30",
     "birth_place": "New York",
     "language": "en"
   }
2 . Validation – Pydantic BirthData schema guarantees type-safe input; any malformed payload is rejected with 422.
3 . Zodiac layer – a deterministic date-range lookup returns the sign in O(1) without any network call.
4 . LLM layer – LangChain’s ChatGoogleGenerativeAI wraps Gemini 1.5-Flash; we prompt it with the sign + full birth context and cap output to 40 tokens.
5 . Translation layer – if language == "hi" we call Google-Translate via googletrans==3.1.0a0; results are LRU-cached for one hour keyed on (sign, lang).
6 . Caching – in-memory dict keyed by (sign, lang) prevents duplicate Gemini/Translate calls, saving cost and latency.
7 . Response – FastAPI serializes {zodiac, insight, language} and returns it in < 1 s total round-trip.


# 1. clone
git clone https://github.com/<you>/astro-insight.git
cd astro-insight

# 2. install
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. secrets
echo "GEMINI_API_KEY=YOUR_KEY" > .env

# 4. run
python app.py
# → http://localhost:8000/docs  (interactive docs)




📖 API Contract

POST /predict
Request (exact sample payload) : 
{
  "name": "Ritika",
  "birth_date": "1995-08-20",
  "birth_time": "14:30",
  "birth_place": "Jaipur, India",
  "language": "en"
}

Response:
{
  "zodiac": "Leo",
  "insight": "Ritika, your Leo heart radiates courage today—lead with kindness and manifest joy.",
  "language": "en"
}
