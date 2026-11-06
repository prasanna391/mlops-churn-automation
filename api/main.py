import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# 1. Initialize FastAPI with Lab 10 metadata specs
app = FastAPI(
    title="Churn Prediction API",
    description="Lab 10 - ML Model Serving and API Engineering",
    version="1.0.0"
)

# 2. Define standard path variables for deployment artifacts
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "deployment", "model.pkl")
PREPROCESSOR_PATH = os.path.join(BASE_DIR, "deployment", "preprocessor.pkl")

# 3. Load model and preprocessor pipelines safely
try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
except Exception as e:
    # Fallback to models directory if deployment folder artifacts are unaligned
    FALLBACK_MODEL_PATH = os.path.join(BASE_DIR, "models", "random_forest_model.pkl")
    FALLBACK_PREPROCESSOR_PATH = os.path.join(BASE_DIR, "models", "preprocessor.pkl")
    try:
        model = joblib.load(FALLBACK_MODEL_PATH)
        preprocessor = joblib.load(FALLBACK_PREPROCESSOR_PATH)
    except Exception as inner_e:
        model = None
        preprocessor = None

# 4. Define Pydantic schema structures for data validation
class ChurnInput(BaseModel):
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

class BatchPredictionRequest(BaseModel):
    inputs: List[ChurnInput]

# 5. Core Operational Routes & Endpoints
@app.get("/", tags=["default"])
@app.get("/Home", tags=["default"])  # Support both path styles gracefully
def read_root():
    return {"message": "Welcome to the Telco Customer Churn Prediction API"}

@app.get("/health", tags=["default"])
def health_check():
    if model is None or preprocessor is None:
        return {"status": "unhealthy", "error": "Model artifacts not loaded properly"}
    return {"status": "healthy"}

@app.get("/metadata", tags=["default"])
def get_metadata():
    return {
        "model_name": "RandomForestClassifier",
        "version": "1.0.0",
        "description": "Lab 10 - Model Serving and API Engineering pipeline",
        "features_required": 30
    }

@app.post("/predict", tags=["default"])
def predict_single(input_data: ChurnInput):
    if model is None or preprocessor is None:
        raise HTTPException(status_code=503, detail="Prediction engine uninitialized.")
    try:
        input_df = pd.DataFrame([input_data.dict()])
        processed_data = preprocessor.transform(input_df)
        prediction = model.predict(processed_data)
        return {"prediction": int(prediction[0]), "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict/batch", tags=["default"])
def predict_batch(request: BatchPredictionRequest):
    if model is None or preprocessor is None:
        raise HTTPException(status_code=503, detail="Prediction engine uninitialized.")
    try:
        input_dicts = [item.dict() for item in request.inputs]
        input_df = pd.DataFrame(input_dicts)
        processed_data = preprocessor.transform(input_df)
        predictions = model.predict(processed_data)
        return {
            "predictions": [int(p) for p in predictions],
            "status": "success",
            "count": len(predictions)
       }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
