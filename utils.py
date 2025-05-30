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
    for linea in reversed(texto.strip().splitlines()):
        if 50 < len(linea.strip()) <= 160 and not linea.startswith("#"):
            return linea.strip()
    return ""

def extraer_titulo(texto: str) -> str:
    # Buscar línea que empiece con exactamente un '# '
    for linea in texto.strip().splitlines():
        if linea.strip().startswith("# "):
            return linea.strip("# ").strip()

    # Si no se encuentra, usar la primera línea no vacía
    for linea in texto.strip().splitlines():
        if linea.strip():
            return linea.strip()

    return "Artículo SEO"


def generar_articulo(keyword: str) -> dict:
    print("🖋️ Iniciando generación de artículo...")

    if not OPENROUTER_API_KEY:
        print("❌ API Key no encontrada.")
        return {}

    prompt = f"""
Actúa como un redactor SEO profesional. Escribe un artículo completo y bien estructurado usando **formato Markdown simple**, optimizado para la palabra clave: "{keyword}".

### Instrucciones:
- No uses bloques de código (no encierres el contenido entre triple backtick ```).
- No agregues etiquetas HTML ni encabezados externos.
- Entrega directamente el contenido como texto plano en formato Markdown.

### Estructura solicitada:
- Un título H1 claro, llamativo y optimizado.
- Una introducción breve (máx. 3 líneas).
- Tres secciones principales con H2, cada una con subtítulos H3.
  - Usa párrafos breves y frases concisas (2-3 líneas por subtítulo).
- Una sección de 3 preguntas frecuentes (FAQs) con respuestas de 2 líneas cada una.
- Un blockquote final que resuma el artículo en una sola frase poderosa.
- Una conclusión clara.
- Finalmente, al final del todo, agrega una meta descripción (máx. 160 caracteres, una sola línea).

Asegúrate de completar todo el artículo antes de enviarlo.
"""

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2000  # Aumentado para evitar cortes
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

