# hackathon/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hackathon.schemas import GrievanceRequest, GrievanceResponse
from hackathon.classifier import classify_grievance

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "FastAPI is running!"}

@app.post("/api/classify", response_model=GrievanceResponse)
def analyze_grievance(data: GrievanceRequest):
    result = classify_grievance(data.text)
    return result