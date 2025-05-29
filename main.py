from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import generar_articulo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes limitar a tu dominio de frontend si quieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationRequest(BaseModel):
    keyword: str

@app.get("/")
def root():
    return {"message": "Generador de artículos SEO"}

@app.post("/generate")
def generate_article(data: GenerationRequest):
    try:
        print(f"🚀 Generando artículo para: '{data.keyword}'")
        result = generar_articulo(data.keyword)

        if not result:
            raise RuntimeError("Falló la generación del artículo")

        return result

    except Exception as e:
        print(f"🔥 Excepción atrapada: {e}")
        raise HTTPException(status_code=500, detail=f"Error al generar el artículo: {str(e)}")


