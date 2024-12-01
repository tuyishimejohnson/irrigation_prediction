from .preprocessing import IrrigationPreprocessor
from .model import IrrigationModel

class IrrigationPredictionService:
    def __init__(self, model_path):
        self.preprocessor = IrrigationPreprocessor()
        self.model = IrrigationModel()
        self.model.load_model(model_path)
        
    def predict_irrigation(self, soil_type, seedling_stage, moi, temp, humidity):
        """Predict irrigation requirement"""
        processed_features = self.preprocessor.prepare_single_prediction(
            soil_type, seedling_stage, moi, temp, humidity
        )
        
        prediction = self.model.predict(processed_features)[0]
        probability = self.model.predict_proba(processed_features)[0]
        
        return {
            'needs_irrigation': bool(prediction),
            'confidence': float(probability[1]),
            'recommendation': self._get_recommendation(probability[1])
        }
        
    def _get_recommendation(self, probability):
        """Generate recommendation based on prediction probability"""
        if probability > 0.8:
            return "Immediate irrigation recommended"
        elif probability > 0.6:
            return "Consider irrigation in the next 24 hours"
        elif probability > 0.4:
            return "Monitor conditions closely"
        else:
            return "No immediate irrigation needed"