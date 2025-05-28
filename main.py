from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from utils import generar_articulo

app = FastAPI()

class RequestData(BaseModel):
    keyword: str
    count: int = 10

@app.post("/generate")
def generate(data: RequestData):
    articles = []
    for i in range(data.count):
        article = generar_articulo(data.keyword)
        articles.append({"title": f"Artículo #{i+1}", "content": article})
    return {"articles": articles}
