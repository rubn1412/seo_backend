import os
import requests
from dotenv import load_dotenv
import markdown  # Para convertir Markdown a HTML
import re
import json

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "deepseek/deepseek-r1-0528:free"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "Referer": "http://localhost:3000",
    "X-Title": "SEO Generator"
}



def generar_articulo_individual(keyword: str) -> dict:
    print("🖋️ Generando un artículo individual...")

    prompt = f"""
Eres un generador de contenido SEO. Tu tarea es crear una idea de artículo long-tail específica basada en la keyword: "{keyword}".

Devuelve exclusivamente un JSON válido como este:
{{
  "title": "Zapatos cómodos para mujeres con pies anchos",
  "content": "Elegir zapatos adecuados para pies anchos es esencial para la comodidad diaria. Aquí te mostramos opciones prácticas..."
}}

Reglas:
- NO escribas nada fuera del JSON.
- El campo "title" debe ser una variación long-tail de la keyword.
- El campo "content" debe tener 2-3 párrafos.
- No uses Markdown, ni etiquetas, ni texto adicional.
"""

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9,
        "max_tokens": 1024
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        print(f"📥 Status code: {response.status_code}")
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"].strip()

        # Validación simple antes del parseo
        if not content.startswith("{") or not content.endswith("}"):
            print("❌ La respuesta no es un JSON válido.")
            return {}

        article = json.loads(content)
        return article

    except Exception as e:
        print(f"❌ Error al procesar la respuesta: {e}")
        return {}

