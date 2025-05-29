from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import generar_articulo

app = FastAPI()

# Permitir CORS desde cualquier origen (puedes restringirlo luego si deseas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto por el dominio del frontend si quieres restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada esperado
class GenerationRequest(BaseModel):
    keyword: str
    count: int = 1

@app.get("/")
def root():
    return {"message": "API de generación de artículos SEO con OpenRouter"}

@app.post("/generate")
def generate_articles(data: GenerationRequest):
    try:
        print(f"🚀 Solicitando generación de {data.count} artículo(s) para: '{data.keyword}'")
        articles = []

        for i in range(data.count):
            print(f"📝 Generando artículo {i+1} de {data.count}...")
            article_data = generar_articulo(data.keyword)

            if not article_data or not article_data.get("content"):
                raise RuntimeError("Falló la generación del artículo.")

            articles.append(article_data)

        print("✅ Generación completada.")
        return {
            "keyword": data.keyword,
            "articles": articles
        }

    except Exception as e:
        print(f"🔥 Excepción atrapada: {e}")
        raise HTTPException(status_code=500, detail=f"Error al generar el artículo: {str(e)}")



