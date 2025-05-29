import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generar_articulo(keyword: str) -> str:
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
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2048
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con OpenRouter: {e}")
        return ""
    except KeyError:
        print("❌ Error: La respuesta de la API no tiene el formato esperado.")
        return ""



        
