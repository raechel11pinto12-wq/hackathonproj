from pydantic import BaseModel, Field
from typing import Optional, List

# Request schema for reporting a lost/found item
class ItemCreate(BaseModel):
    item_type: str = Field(..., description="'Lost' or 'Found'")
    title: str = Field(..., description="Item name e.g., 'Blue Water Bottle'")
    category: str = Field(..., description="e.g., Electronics, Documents, Keys, Clothing")
    date: str = Field(..., description="Date lost or found (YYYY-MM-DD)")
    location: str = Field(..., description="e.g., 'Main Canteen', 'Lab 3'")
    description: str = Field(..., description="Details about the item")
    reporter_name: str = Field(..., description="User's full name")
    contact_info: str = Field(..., description="Email or Phone number")
    photo_url: Optional[str] = Field(None, description="Image URL or file path")

# Response schema returned by the API
class ItemResponse(ItemCreate):
    id: int
    is_verified: bool = False
    status: str = "Active"  # "Active" or "Claimed"