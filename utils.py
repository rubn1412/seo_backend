import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "openrouter/cinematika-7b:free" # 🔒 Forzamos el modelo gratuito

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:3000",  # O la URL real de tu frontend
    "X-Title": "SEO Generator" }

def generar_articulo(keyword: str) -> str:
    print("🖋️ Iniciando generación de artículo...")
    
    if not OPENROUTER_API_KEY:
        print("❌ API Key no encontrada. Verifica tu archivo .env.")
        return ""

    prompt = f"""
    Crea un artículo SEO optimizado para la keyword long-tail relacionada con: "{keyword}".
    Estructura:
    - H1 (Título principal)
    - Introducción breve (2-3 párrafos)
    - 3-5 H2 (Subtítulos principales)
    - Varios H3 bajo cada H2 (Detalles)
    - 3-5 FAQs con respuestas
    - Meta descripción (160 caracteres)
    - Fragmento destacado (para featured snippet)
    Formato de salida: Markdown
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

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

        if response.status_code == 401:
            print("❌ No autorizado: revisa que tu API key esté activa y asociada al modelo gratuito.")
            print("🔐 Modelo usado:", OPENROUTER_MODEL)
            return ""

        response.raise_for_status()

        respuesta = response.json()
        return respuesta["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con OpenRouter: {e}")
        return ""
    except (KeyError, IndexError):
        print("❌ Error: La respuesta de la API no tiene el formato esperado.")
        print("📄 Respuesta cruda:", response.text)
        return ""



        
