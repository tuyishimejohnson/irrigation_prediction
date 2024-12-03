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
    moi: float
    temp: float
    humidity: float
    soil_type: str
    seedling_stage: str

@app.post("/predict")
async def predict_irrigation(input_data: PredictionInput):
    try:
        # Create features array with only numerical features
        features = np.array([[
            input_data.moi,
            input_data.temp, 
            input_data.humidity
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probability = float(prediction[0]) if hasattr(prediction, '__len__') else float(prediction)
        
        print(f"Debug - Features: {features}")  # Debug logging
        print(f"Debug - Scaled features: {features_scaled}")  # Debug logging
        print(f"Debug - Raw prediction: {prediction}")  # Debug logging
        print(f"Debug - Probability: {probability}")  # Debug logging
        
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
                "soil_type": input_data.soil_type,
                "seedling_stage": input_data.seedling_stage,
                "moi": input_data.moi,
                "temp": input_data.temp,
                "humidity": input_data.humidity
            }
        }
        
    except Exception as e:
        print(f"Detailed error: {str(e)}")  # Debug logging
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
        contents = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(contents))
        
        # Prepare numerical features only
        numerical_features = ['MOI', 'temp', 'humidity']
        X = df[numerical_features].values
        y = df['result'].values
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Create model with regularization and different architecture
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(32, activation='relu', input_shape=(3,),
                                kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(16, activation='relu',
                                kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(8, activation='relu',
                                kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
                     loss='binary_crossentropy',
                     metrics=['accuracy'])
        
        # Add early stopping to prevent overfitting
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        )
        
        history = model.fit(X_scaled, y,
                          epochs=50,
                          batch_size=32,
                          validation_split=0.2,
                          callbacks=[early_stopping])
        
        # Save model and scaler
        model_data = {
            'model': model,
            'scaler': scaler,
            'le_soil': le_soil,
            'le_seedling': le_seedling
        }
        joblib.dump(model_data, 'models/cropmodel.pkl')
        
        return {
            "message": "Model retrained successfully",
            "history": {
                "accuracy": float(history.history['accuracy'][-1]),
                "val_accuracy": float(history.history['val_accuracy'][-1])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining error: {str(e)}")
    
@app.post("/predict")
async def predict(data: dict):
    try:
        # Load the saved model and preprocessing objects
        model_data = joblib.load('models/cropmodel.pkl')
        model = model_data['model']
        scaler = model_data['scaler']
        le_soil = model_data['le_soil']
        le_seedling = model_data['le_seedling']

        # Transform categorical inputs
        soil_type_encoded = le_soil.transform([data['soil_type']])[0]
        seedling_stage_encoded = le_seedling.transform([data['seedling_stage']])[0]

        # Create input array
        input_data = np.array([[
            data['moi'],
            data['temp'], 
            data['humidity']
        ]])

        # Scale the numerical features
        input_scaled = scaler.transform(input_data)

        # Make prediction
        prediction = model.predict(input_scaled)
        confidence = float(prediction[0][0])
        needs_irrigation = bool(confidence >= 0.5)

        # Generate recommendation
        if needs_irrigation:
            recommendation = "Based on the current conditions, irrigation is recommended."
        else:
            recommendation = "Based on the current conditions, irrigation is not necessary at this time."

        return {
            "needs_irrigation": needs_irrigation,
            "confidence": confidence,
            "recommendation": recommendation,
            "input_parameters": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
