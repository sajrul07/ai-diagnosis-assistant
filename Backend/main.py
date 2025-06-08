from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging

from models import (UserRegister, UserLogin, MedicalRequest, MedicalReport)
from auth import register_user, login_user, verify_token
from ai_service import generate_medical_report_ai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/register")
async def register(user: UserRegister):
    return await register_user(user)

@app.post("/login")
async def login(user: UserLogin):
    return await login_user(user)

@app.post("/analyze", response_model=MedicalReport, dependencies=[Depends(verify_token)])
async def analyze(request: MedicalRequest):
    try:
        ai_response = await generate_medical_report_ai(request.dict())
        return ai_response
    except Exception as e:
        logger.error(f"Error in /analyze: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate medical report")
