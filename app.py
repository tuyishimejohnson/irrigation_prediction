from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import pickle

# Define the FastAPI app
app = FastAPI()

# Base directory and model path (relative path)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = "./models/cropmodel.pkl"

# Function to load the trained model
def load_trained_model():
    # Check if the model file exists
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Ensure 'cropmodel.pkl' is in the 'models' directory.")
    
    try:
        # Load the model with pickle
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print("Model loaded successfully.")
        return model
    except pickle.UnpicklingError:
        raise HTTPException(status_code=500, detail="Error unpickling the model. It might be corrupted or incompatible.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")

# Pydantic model for input data
class PredictionInput(BaseModel):
    crop_id: int
    soil_type: int  
    seedling_stage: int  
    moi: float  # Moisture (MOI) - assuming a float
    temp: float  # Temperature - assuming a float
    humidity: float  # Humidity - assuming a float

# Load the model at startup
model = None
try:
    model = load_trained_model()
except HTTPException as e:
    print(f"Model loading error: {e.detail}")

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.post("/predict")
async def predict(input_data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please check the model file.")

    # Convert input data to the required format for the model
    input_features = [
        [
            input_data.crop_id,
            input_data.soil_type,
            input_data.seedling_stage,
            input_data.moi,
            input_data.temp,
            input_data.humidity
        ]
    ]

    try:
        # Make a prediction
        prediction = model.predict(input_features)
        return {"prediction": prediction[0]}  # Assuming the model outputs a single value
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
