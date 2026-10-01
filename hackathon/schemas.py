from pydantic import BaseModel

class GrievanceRequest(BaseModel):
    text: str

class GrievanceResponse(BaseModel):
    summary: str
    category: str
    priority: str
    action: str