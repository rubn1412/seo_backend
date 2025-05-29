import os
import requests
from dotenv import load_dotenv
import markdown  # Para convertir Markdown a HTML
import re

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "deepseek/deepseek-r1-0528:free"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "Referer": "http://localhost:3000",
    "X-Title": "SEO Generator"
}

def generar_articulo(keyword: str) -> str:
    def generar_articulo(keyword: str) -> list[dict]:
    print("🖋️ Iniciando generación de artículos...")

    if not OPENROUTER_API_KEY:
        print("❌ API Key no encontrada. Verifica tu archivo .env.")
        return []

    prompt = f"""
Actúa como un generador de contenido SEO experto. Para la palabra clave "{keyword}", genera una lista de entre 10 y 20 artículos long-tail optimizados. Devuelve el resultado en formato JSON. Cada entrada debe tener:

- "title": el título del artículo
- "content": una introducción de 2-3 párrafos

Ejemplo de formato:

[
  {{
    "title": "Zapatos mujer cómodos para oficina",
    "content": "Los zapatos cómodos son esenciales para largas jornadas laborales..."
  }},
  ...
]

No incluyas explicaciones ni texto fuera del JSON.
"""

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2048
    }

    try:
        print(f"📤 Enviando prompt para la keyword: '{keyword}'")
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        print(f"📥 Status code: {response.status_code}")

        response.raise_for_status()
        respuesta = response.json()
        content = respuesta["choices"][0]["message"]["content"]

        # Intenta parsear el contenido como JSON
        articles = json.loads(content)
        return articles

    except (KeyError, IndexError, ValueError, json.JSONDecodeError) as e:
        print(f"❌ Error al procesar la respuesta: {e}")
        return []

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con OpenRouter: {e}")
        return []

