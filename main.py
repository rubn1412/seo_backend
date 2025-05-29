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
async def generate_article(request: Request, data: dict):
    keyword = data.get("keyword", "")
    try:
        article = await generar_articulo(keyword)
        return article
    except Exception as e:
        print("❌ ERROR AL GENERAR:", e)
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

