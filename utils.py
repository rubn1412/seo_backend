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
    for linea in texto.strip().splitlines():
        if 50 < len(linea.strip()) <= 160 and not linea.startswith("#"):
            return linea.strip()
    return ""

def extraer_titulo(texto: str) -> str:
    match = re.search(r"^# (.+)", texto, re.MULTILINE)
    return match.group(1).strip() if match else "Artículo SEO"

def generar_articulo(keyword: str) -> dict:
    print("🖋️ Iniciando generación de artículo...")

    if not OPENROUTER_API_KEY:
        print("❌ API Key no encontrada.")
        return {}

    prompt = f"""
Actúa como un redactor SEO profesional. Escribe un artículo completo y bien estructurado en formato Markdown optimizado para la keyword: "{keyword}".

Estructura del contenido:
- Un título H1 claro, llamativo y optimizado.
- Una introducción (máximo 3 líneas) que enganche al lector y resuma el contenido.
- Tres secciones principales H2 con subtítulos H3 dentro de cada una.
  - Usa párrafos breves y frases concisas (2-3 líneas por subtítulo).
- Una sección de 3 preguntas frecuentes (FAQs) con respuestas cortas (2 líneas cada una).
- Un blockquote al final que resuma el artículo en una frase poderosa.
- Cierra con una conclusión clara que sintetice el contenido.
- Incluye una meta descripción de máximo 160 caracteres al final (en una sola línea separada).

Devuelve exclusivamente el artículo en formato Markdown. No incluyas explicaciones, ni encabezados adicionales.
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
        print("📤 Respuesta JSON completa:")
        print(result)

        if "choices" not in result:
            print("❌ La respuesta no contiene 'choices'.")
            return {}

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


