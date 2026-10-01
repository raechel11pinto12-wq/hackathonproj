from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional, List
import os

from hackathon.schemas import ItemCreate, ItemResponse
from hackathon.classifier import add_item, get_items, verify_item

app = FastAPI(title="Digital Lost & Found API")

# Allow CORS for frontend fetches
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static CSS & JS
app.mount("/static", StaticFiles(directory="hackathon/static"), name="static")

# Home route serving the HTML frontend
@app.get("/")
def read_root():
    template_path = "hackathon/templates/index.html"
    if os.path.exists(template_path):
        return FileResponse(template_path)
    return {"message": "API Running. Front end template missing."}

# 1. Fetch/Search items (GET /api/items)
@app.get("/api/items", response_model=List[ItemResponse])
def search_and_filter_items(
    query: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    item_type: Optional[str] = Query(None)
):
    return get_items(query, category, item_type)

# 2. Submit report (POST /api/items)
@app.post("/api/items", response_model=ItemResponse)
def report_item(item: ItemCreate):
    return add_item(item)

# 3. Admin verification (PATCH /api/items/{item_id}/verify)
@app.patch("/api/items/{item_id}/verify", response_model=ItemResponse)
def approve_item_by_admin(item_id: int):
    updated_item = verify_item(item_id)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item ID not found")
    return updated_item