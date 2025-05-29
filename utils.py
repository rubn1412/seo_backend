import os
import requests
from dotenv import load_dotenv
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

def extraer_meta_descripcion(texto: str) -> str:
    """
    Intenta extraer una línea que parezca una meta descripción (<=160 caracteres y con buena estructura).
    """
    for linea in texto.strip().splitlines():
        if 50 < len(linea.strip()) <= 160 and not linea.startswith("#"):
            return linea.strip()
    return ""

def extraer_titulo(texto: str) -> str:
    """
    Extrae el primer título H1 que aparece.
    """
    match = re.search(r"^# (.+)", texto, re.MULTILINE)
    return match.group(1).strip() if match else "Artículo SEO"

def generar_articulo(keyword: str) -> dict:
    print("🖋️ Iniciando generación de artículo...")

    if not OPENROUTER_API_KEY:
        print("❌ API Key no encontrada.")
        return {}

    prompt = f"""
    Actúa como un redactor SEO. Escribe un artículo optimizado en formato Markdown para la keyword: "{keyword}".

    Estructura:
    - Título principal (H1)
    - Introducción con 2 párrafos
    - 3 secciones principales (H2) con subtítulos H3
    - FAQs con 3 preguntas y respuestas
    - Meta descripción (máximo 160 caracteres)
    - Fragmento destacado en una cita (blockquote)

    Usa subtítulos claros y contenido enfocado en la intención de búsqueda.

    Devuelve solo el artículo en formato Markdown sin explicación.
    """

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1400
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        print(f"📥 Status code: {response.status_code}")

        if response.status_code != 200:
            print("❌ Respuesta inválida de OpenRouter.")
            return {}

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        title = extraer_titulo(content)
        meta = extraer_meta_descripcion(content)

        return {
            "title": title,
            "content": content,
            "meta_description": meta
        }

    except Exception as e:
        print(f"❌ Error al generar artículo: {e}")
        return {}


