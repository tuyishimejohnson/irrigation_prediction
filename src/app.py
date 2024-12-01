from fastapi import FastAPI
import pickle
import pandas as pd

# Create FastAPI instance
app = FastAPI()

# Load the saved model
with open("models/cropmodel.pkl", "rb") as f:
    model = pickle.load(f)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Irrigation Prediction API"}

@app.post("/predict")
async def predict(
    crop_id: int,
    soil_type: int,
    seedling_stage: int,
    moi: float,
    temp: float,
    humidity: float
):
    # Create DataFrame with input data
    input_data = pd.DataFrame([[crop_id, soil_type, seedling_stage, moi, temp, humidity]], 
                            columns=['crop ID', 'soil_type', 'Seedling Stage', 'MOI', 'temp', 'humidity'])
    
    # Make prediction
    prediction = model.predict(input_data)[0][0]
    
    return {
        "prediction": float(prediction),
        "needs_irrigation": bool(prediction > 0.5)
    }