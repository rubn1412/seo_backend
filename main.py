from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import generar_articulo
from fastapi.responses import JSONResponse

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
async def generate_article(request: Request):
    try:
        data = await request.json()
        keyword = data.get("keyword", "")
        article = generar_articulo(keyword)  # Quitar await
        return article
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
