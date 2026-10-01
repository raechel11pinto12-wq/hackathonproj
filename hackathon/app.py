from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from hackathon.schemas import GrievanceRequest, GrievanceResponse
from hackathon.classifier import classify_grievance

app = FastAPI()

# 1. Mount the static directory so CSS and JS load properly
app.mount("/static", StaticFiles(directory="hackathon/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Serve index.html from inside the templates folder
@app.get("/")
def home():
    return FileResponse("hackathon/templates/index.html")

# 3. Handle the grievance classification API
@app.post("/api/classify", response_model=GrievanceResponse)
def analyze_grievance(data: GrievanceRequest):
    result = classify_grievance(data.text)
    return result