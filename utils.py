import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Verifica la URL actual en la documentación


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
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload: Dict[str, Any] = {
        "model": "deepseek-chat",  # Ajusta según los modelos disponibles
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2000  # Ajusta según necesites
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()

        return response_data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de DeepSeek: {e}")
        return ""
    except KeyError:
        print("Error: La respuesta de la API no tiene el formato esperado")
        return ""