import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

 @app.post("/generate")
def generate_articles(data: GenerationRequest):
    print("🔧 Iniciando generación de artículos...")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    print("🔐 API KEY:", "CARGADA" if api_key else "NO ENCONTRADA")

    if not api_key:
        raise RuntimeError("❌ No se encontró la API Key. Verifica tu archivo .env.")

    articles = []

    try:
        for i in range(data.count):
            prompt = random.choice(prompt_variants).format(data.keyword)
            print(f"📨 Prompt {i+1}: {prompt}")

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-r1-0528:free",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 1.0
                }
            )

            print(f"🔄 Status HTTP {response.status_code}")

            if response.ok:
                content = response.json()["choices"][0]["message"]["content"]
                print(f"✅ Artículo generado: {content[:60]}...")
                cleaned = limpiar_articulo(content)
                articles.append(cleaned)
            else:
                print("❌ Error al llamar a la API:", response.text)
                raise HTTPException(status_code=500, detail=f"Error al generar el artículo: {response.text}")

        return {"articles": articles}

    except Exception as e:
        print("💥 EXCEPCIÓN DETECTADA:", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor.")





        
