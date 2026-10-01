from typing import List, Optional

# In-memory database with initial sample records
db_items = [
    {
        "id": 1,
        "item_type": "Lost",
        "title": "College ID Card",
        "category": "Documents",
        "date": "2026-10-01",
        "location": "Main Canteen",
        "description": "Lost ID card near counter 2.",
        "reporter_name": "Raechel",
        "contact_info": "raechel@example.com",
        "photo_url": "https://via.placeholder.com/150",
        "is_verified": True,
        "status": "Active"
    },
    {
        "id": 2,
        "item_type": "Found",
        "title": "Black Boat Earbuds",
        "category": "Electronics",
        "date": "2026-10-01",
        "location": "Lab 3",
        "description": "Found charging case on desk 4.",
        "reporter_name": "Sam",
        "contact_info": "sam@example.com",
        "photo_url": "https://via.placeholder.com/150",
        "is_verified": False,
        "status": "Active"
    }
]

def add_item(data) -> dict:
    new_item = data.dict()
    new_item["id"] = len(db_items) + 1
    new_item["is_verified"] = False  # Defaults to False until Admin verifies
    new_item["status"] = "Active"
    db_items.append(new_item)
    return new_item

def get_items(query: Optional[str] = None, category: Optional[str] = None, item_type: Optional[str] = None) -> List[dict]:
    results = db_items
    if item_type and item_type.lower() != "all":
        results = [item for item in results if item["item_type"].lower() == item_type.lower()]
    if category and category.lower() != "all":
        results = [item for item in results if item["category"].lower() == category.lower()]
    if query:
        q = query.lower()
        results = [item for item in results if q in item["title"].lower() or q in item["location"].lower()]
    return results

def verify_item(item_id: int) -> Optional[dict]:
    for item in db_items:
        if item["id"] == item_id:
            item["is_verified"] = True
            return item
    return None