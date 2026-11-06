from pydantic import BaseModel
from typing import List, Dict, Any

# Your existing single customer schema (e.g., ChurnInput)
class ChurnInput(BaseModel):
    # Make sure these match your actual dataset fields (Gender, MonthlyCharges, etc.)
    customerID: str
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: str

# --- ADD THESE FOR LAB 10 BATCH PREDICTION ---
class BatchPredictionRequest(BaseModel):
    inputs: List[ChurnInput]

class BatchPredictionResponse(BaseModel):
    predictions: List[int]
    status: str
