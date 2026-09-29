import json
from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="Akıllı Restoran Menüsü")

# Menü verisini oku
with open("data/menu.json", "r", encoding="utf-8") as f:
    MENU_DATA = json.load(f)

# Static dosyaları bağla (HTML/CSS/JS için)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

# Menü listeleme ve filtreleme endpoint'i (Ajanın ileride çağıracağı temel mantık)
@app.get("/api/menu")
def get_menu(
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    exclude_allergen: Optional[str] = None,
    tag: Optional[str] = None
):
    results = MENU_DATA

    if category:
        results = [item for item in results if item["category"].lower() == category.lower()]
    
    if max_price is not None:
        results = [item for item in results if item["price"] <= max_price]
        
    if exclude_allergen:
        allergens_to_exclude = [a.strip().lower() for a in exclude_allergen.split(",")]
        results = [
            item for item in results 
            if not any(a.lower() in allergens_to_exclude for a in item["allergens"])
        ]
        
    if tag:
        results = [item for item in results if tag.lower() in [t.lower() for t in item["tags"]]]

    return results