from pydantic import BaseModel
from typing import List

# Auth Models
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Medical AI request and response models
class MedicalRequest(BaseModel):
    age: int
    gender: str
    weight: float
    symptoms: str
    medical_history: str

class Diagnosis(BaseModel):
    disease: str
    summary: str
    severity: str

class ImmediateActions(BaseModel):
    steps: List[str]
    emergency_signs: List[str]

class MedicalRecommendations(BaseModel):
    specialist_to_consult: str
    recommended_tests: List[str]
    treatment_options: List[str]

class RiskFactors(BaseModel):
    causes: List[str]
    high_risk_groups: List[str]

class PreventiveMeasures(BaseModel):
    prevention_tips: List[str]
    lifestyle_changes: List[str]

class MedicalReport(BaseModel):
    diagnosis: Diagnosis
    immediate_actions: ImmediateActions
    medical_recommendations: MedicalRecommendations
    risk_factors: RiskFactors
    preventive_measures: PreventiveMeasures
