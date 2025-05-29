import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

  @app.post("/generate")
def generate_articles(data: GenerationRequest):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("❌ No se encontró la API Key. Verifica tu archivo .env.")

    articles = []

    for _ in range(data.count):
        prompt = random.choice(prompt_variants).format(data.keyword)

        try:
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

            if response.ok:
                content = response.json()["choices"][0]["message"]["content"]
                cleaned = limpiar_articulo(content)
                articles.append(cleaned)
            else:
                print("❌ Error en la respuesta:", response.status_code, response.text)
                raise HTTPException(status_code=500, detail=f"Error al generar el artículo: {response.text}")
        
        except Exception as e:
            print("❌ Excepción detectada:", str(e))  # Agregado para depurar
            raise HTTPException(status_code=500, detail="Error inesperado en el servidor.")

    return {"articles": articles}




        
