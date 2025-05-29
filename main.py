from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import random
import re
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class GenerationRequest(BaseModel):
    keyword: str
    count: int = 1

prompt_variants = [
    "Escribe un artículo SEO detallado sobre '{}'. Usa formato markdown.",
    "Redacta un post informativo y optimizado para Google con el tema: '{}'.",
    "Genera un artículo optimizado para SEO sobre '{}'. Incluye encabezados H2 y listas.",
    "Escribe una guía práctica SEO basada en la keyword: '{}'.",
    "Crea un artículo que ayude a posicionar en Google con la keyword '{}'."
]

def limpiar_articulo(texto: str) -> str:
    patron = r"Este artículo sigue las mejores prácticas SEO:(.|\n)*"
    return re.sub(patron, "", texto).strip()

@app.post("/generate")
def generate_articles(data: GenerationRequest):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("❌ No se encontró la API Key. Verifica tu archivo .env.")

    articles = []

    for _ in range(data.count):
        prompt = random.choice(prompt_variants).format(data.keyword)

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-r1-0528:free",  # <- modelo correcto
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 1.0
            }
        )

        if response.ok:
            content = response.json()["choices"][0]["message"]["content"]
            cleaned = limpiar_articulo(content)
            articles.append(cleaned)
        else:
            raise HTTPException(status_code=500, detail=f"Error al generar el artículo: {response.text}")

    return {"articles": articles}
