from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Updated to match your Vite frontend port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model and preprocessors
try:
    model_data = joblib.load('models/cropmodel.pkl')
    model = model_data['model']
    scaler = model_data['scaler']
    le_soil = model_data['le_soil']
    le_seedling = model_data['le_seedling']
except Exception as e:
    print(f"Error loading model: {e}")
    raise Exception("Model files not found. Please ensure model is trained and saved correctly.")

class PredictionInput(BaseModel):
    crop_id: int
    soil_type: int
    seedling_stage: int
    moi: float
    temp: float
    humidity: float

@app.post("/predict")
async def predict_irrigation(input_data: PredictionInput):
    try:
        # Prepare input features - ONLY numerical features for scaling
        features = np.array([
            input_data.moi,
            input_data.temp,
            input_data.humidity
        ]).reshape(1, -1)
        
        # Scale only the numerical features
        features_scaled = scaler.transform(features)
        
        # Add categorical features AFTER scaling
        features_final = np.hstack([
            np.array([[input_data.crop_id]]),  # Add crop_id
            features_scaled,
            np.array([[
                input_data.soil_type,
                input_data.seedling_stage
            ]])
        ])
        
        # Make prediction with complete feature set
        prediction = model.predict(features_final)[0]
        probability = float(prediction[0]) if hasattr(prediction, '__len__') else float(prediction)
        
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
            "needs_irrigation": bool(probability > 0.5),
            "confidence": probability,
            "recommendation": recommendation,
            "input_parameters": {
                "crop_id": input_data.crop_id,
                "soil_type": input_data.soil_type,
                "seedling_stage": input_data.seedling_stage,
                "moi": input_data.moi,
                "temp": input_data.temp,
                "humidity": input_data.humidity
            }
        }
        
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

@app.post("/retrain")
async def retrain_model(file: UploadFile = File(...)):
    try:
        # Read the uploaded CSV file
        contents = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(contents))
        
        # Prepare features
        numerical_features = ['MOI', 'temp', 'humidity']
        X = df[numerical_features].values
        y = df['result'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        
        # Create and train new model
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(optimizer='adam', 
                     loss='binary_crossentropy',
                     metrics=['accuracy'])
        
        history = model.fit(X_train_scaled, y_train,
                          epochs=30,
                          batch_size=32,
                          validation_split=0.2)
        
        # Save new model and scaler
        model_data = {
            'model': model,
            'scaler': scaler,
            'le_soil': le_soil,
            'le_seedling': le_seedling
        }
        joblib.dump(model_data, 'models/cropmodel.pkl')
        
        # Return training results
        return {
            "message": "Model retrained successfully",
            "history": {
                "accuracy": float(history.history['accuracy'][-1]),
                "val_accuracy": float(history.history['val_accuracy'][-1])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining error: {str(e)}")