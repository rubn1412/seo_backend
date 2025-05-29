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
    print("🖋️ Iniciando generación de artículo...")

    if not OPENROUTER_API_KEY:
        print("❌ API Key no encontrada. Verifica tu archivo .env.")
        return ""

    prompt = f"""
    Crea un artículo SEO optimizado para la keyword long-tail relacionada con: "{keyword}".
    Estructura:
    - H1 (Título principal)
    - Introducción breve 
    - No mas de 800 palabras
    - 3-5 H2 (Subtítulos principales)
    - Varios H3 bajo cada H2 (Detalles)
    - 3-5 FAQs con respuestas
    - Meta descripción (160 caracteres)
    - Fragmento destacado (para featured snippet)
    Formato de salida: Markdown
    """

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1200
    }

    try:
        print(f"📤 Enviando prompt para la keyword: '{keyword}'")
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        print(f"📥 Status code: {response.status_code}")

        if response.status_code == 401:
            print("❌ No autorizado: revisa que tu API key esté activa y asociada al modelo gratuito.")
            return ""

        response.raise_for_status()
        
        respuesta = response.json()

        # ✅ Validar que 'choices' esté en la respuesta
        if "choices" in respuesta and respuesta["choices"]:
            return respuesta["choices"][0]["message"]["content"]
        else:
            print("❌ La respuesta no contiene 'choices'. Respuesta completa:", respuesta)
            return ""

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con OpenRouter: {e}")
        return ""
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return ""
