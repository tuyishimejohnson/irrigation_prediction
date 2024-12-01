from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from datetime import datetime
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score

class IrrigationModel:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight='balanced'
        )
        
    def train(self, X, y):
        """Train the irrigation prediction model"""
        self.model.fit(X, y)
        
    def predict(self, X):
        """Make irrigation predictions"""
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Get probability scores"""
        return self.model.predict_proba(X)
    
    def evaluate(self, X, y):
        """Evaluate model performance"""
        predictions = self.predict(X)
        prob_predictions = self.predict_proba(X)[:, 1]
        
        return {
            'accuracy': accuracy_score(y, predictions),
            'roc_auc': roc_auc_score(y, prob_predictions),
            'classification_report': classification_report(y, predictions),
            'confusion_matrix': confusion_matrix(y, predictions)
        }
    
    def get_feature_importance(self):
        """Get feature importance scores"""
        features = ['MOI', 'Temperature', 'Humidity', 'Soil Type', 'Seedling Stage']
        importance = self.model.feature_importances_
        return pd.DataFrame({'feature': features, 'importance': importance})