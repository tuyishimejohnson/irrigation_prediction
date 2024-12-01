from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# Enable CORS - Update to match your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model and preprocessors
try:
    model_data = joblib.load('models/cropmodel.pkl')
    model = model_data['model']
    scaler = model_data['scaler']
    le_soil = model_data['le_soil']
    le_seedling = model_data['le_seedling']
except Exception as e:
    print(f"Error loading model: {e}")
    raise Exception("Model files not found. Please ensure model is trained and saved correctly.")

# Pydantic model for input validation
class PredictionInput(BaseModel):
    crop_id: str
    soil_type: str
    seedling_stage: str
    moi: float  
    temp: float
    humidity: float

class PredictionResponse(BaseModel):
    needs_irrigation: bool
    confidence: float
    recommendation: str
    input_parameters: dict

@app.post("/predict", response_model=PredictionResponse)
async def predict_irrigation(input_data: PredictionInput):
    try:
        # Transform categorical variables
        soil_type_encoded = le_soil.transform([input_data.soil_type])[0]
        seedling_stage_encoded = le_seedling.transform([input_data.seedling_stage])[0]
        
        # Prepare input features
        features = np.array([
            input_data.moi,
            input_data.temp,
            input_data.humidity,
            soil_type_encoded,
            seedling_stage_encoded
        ])
        
        # Scale features
        features_scaled = scaler.transform(features.reshape(1, -1))
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0][1]
        
        # Generate recommendation based on probability
        if probability > 0.8:
            recommendation = "Immediate irrigation recommended"
        elif probability > 0.6:
            recommendation = "Consider irrigation in the next 24 hours"
        elif probability > 0.4:
            recommendation = "Monitor conditions closely"
        else:
            recommendation = "No immediate irrigation needed"
        
        return {
            "needs_irrigation": bool(prediction),
            "confidence": float(probability),
            "recommendation": recommendation,
            "input_parameters": input_data.dict()
        }
        
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input value: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/model-info")
async def get_model_info():
    """Get information about the current model"""
    try:
        return {
            "features": ["MOI", "Temperature", "Humidity", "Soil Type", "Seedling Stage"],
            "soil_types": list(le_soil.classes_),
            "seedling_stages": list(le_seedling.classes_)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving model info: {str(e)}")