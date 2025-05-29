from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils import generar_articulo

app = FastAPI()

# Configurar CORS para permitir cualquier origen (útil en desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar esto por tu dominio real en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos para recibir el JSON del frontend
class GenerationRequest(BaseModel):
    keyword: str

@app.get("/")
def root():
    return {"message": "Generador de artículos SEO"}

@app.post("/generate")
def generate_article(data: GenerationRequest):
    try:
        article = generar_articulo(data.keyword)
        return article
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

