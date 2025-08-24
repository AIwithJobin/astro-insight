from fastapi import FastAPI
from core.zodiac import get_sign
from core.llm_stub import generate_insight
from core.translator import translate
from core.cache import cache_get, cache_set
from models.request import BirthData
import uvicorn

app = FastAPI(title="Daily Astro Insight API")

@app.post("/predict")
def predict(data: BirthData):
    sign = get_sign(data.birth_date)
    cache_key = (sign, data.language)

    insight = cache_get(cache_key)
    if not insight:
        insight = generate_insight(
            sign=sign,
            name=data.name,
            birth_date=str(data.birth_date),
            birth_time=data.birth_time,
            birth_place=data.birth_place
        )
        if data.language == "hi":
            insight = translate(insight, dest="hi")
        cache_set(cache_key, insight)

    return {"zodiac": sign, "insight": insight, "language": data.language}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)