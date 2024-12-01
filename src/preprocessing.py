import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

class IrrigationPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.soil_encoder = LabelEncoder()
        self.seedling_encoder = LabelEncoder()
        
    def load_data(self, filepath='data/cropdata_updated.csv'):
        """Load irrigation dataset"""
        return pd.read_csv(filepath)
    
    def preprocess_data(self, data):
        """Preprocess the irrigation prediction data"""
        # Encode categorical variables
        data['soil_type_encoded'] = self.soil_encoder.fit_transform(data['soil_type'])
        data['seedling_stage_encoded'] = self.seedling_encoder.fit_transform(data['Seedling Stage'])
        
        # Select features for scaling
        numeric_features = ['MOI', 'temp', 'humidity']
        categorical_features = ['soil_type_encoded', 'seedling_stage_encoded']
        
        X = data[numeric_features + categorical_features]
        y = data['result']
        
        # Scale numeric features
        X_scaled = X.copy()
        X_scaled[numeric_features] = self.scaler.fit_transform(X[numeric_features])
        
        return X_scaled, y
    
    def prepare_single_prediction(self, soil_type, seedling_stage, moi, temp, humidity):
        """Prepare single input for prediction"""
        # Encode categorical inputs
        soil_encoded = self.soil_encoder.transform([soil_type])[0]
        seedling_encoded = self.seedling_encoder.transform([seedling_stage])[0]
        
        # Create and scale features
        features = np.array([[moi, temp, humidity, soil_encoded, seedling_encoded]])
        features_scaled = features.copy()
        features_scaled[:, :3] = self.scaler.transform(features[:, :3])
        
        return features_scaled