from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import random
import re
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto a tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    try:
        print("🖋️ Iniciando generación de artículos...")

        api_key = os.getenv("OPENROUTER_API_KEY")
        print("🔑 API KEY:", "CARGADA" if api_key else "NO ENCONTRADA")

        if not api_key:
            raise RuntimeError("❌ No se encontró la API Key. Verifica tu archivo .env o variables en Render.")

        articles = []

        for _ in range(data.count):
            prompt = random.choice(prompt_variants).format(data.keyword)
            print(f"📤 Enviando prompt: {prompt}")

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-r1-0528:free",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 1.0
                }
            )

            print("📥 Status:", response.status_code)
            if response.ok:
                content = response.json()["choices"][0]["message"]["content"]
                cleaned = limpiar_articulo(content)
                articles.append(cleaned)
            else:
                print("❌ Error en respuesta:", response.text)
                raise HTTPException(status_code=500, detail=f"Error al generar el artículo: {response.text}")

        return {"articles": articles}

    except Exception as e:
        print("🔥 Excepción atrapada:", str(e))
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


