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

def generar_articulo(keyword: str) -> dict:
    print("🖋️ Iniciando generación de artículo...")

    if not OPENROUTER_API_KEY:
        print("❌ API Key no encontrada. Verifica tu archivo .env.")
        return {}

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

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2048
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        print(f"📥 Status code: {response.status_code}")

        if response.status_code == 401:
            print("❌ No autorizado: revisa que tu API key esté activa y asociada al modelo gratuito.")
            return {}

        response.raise_for_status()
        markdown_raw = response.json()["choices"][0]["message"]["content"]

        # Extraer el título (primer H1)
        title_match = re.search(r"# (.+)", markdown_raw)
        title = title_match.group(1).strip() if title_match else "Artículo generado"

        # Extraer meta descripción (si viene al final)
        meta_match = re.search(r"(?i)meta descripción[:\-]*\s*(.{30,160})", markdown_raw)
        meta_description = meta_match.group(1).strip() if meta_match else ""

        # Extraer featured snippet
        snippet_match = re.search(r"(?i)fragmento destacado[:\-]*\s*(.+)", markdown_raw)
        snippet = snippet_match.group(1).strip() if snippet_match else ""

        # Convertir todo el markdown a HTML
        html_content = markdown.markdown(markdown_raw)

        return {
            "title": title,
            "content": html_content,
            "meta_description": meta_description,
            "snippet": snippet
        }

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con OpenRouter: {e}")
        return {}
    except (KeyError, IndexError, ValueError) as e:
        print(f"❌ Error inesperado: {e}")
        return {}

        
