import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.models.crop_yield_model import CropYieldPredictor
from backend.models.disease_detection_model import DiseaseDetector

def train_all_models():
    """Train all models for the smart agriculture system"""
    
    print("Starting model training process...")
    
    # Train crop yield prediction model
    print("\n" + "="*50)
    print("Training Crop Yield Prediction Model")
    print("="*50)
    
    yield_predictor = CropYieldPredictor()
    yield_history = yield_predictor.train()
    
    # Train disease detection model
    print("\n" + "="*50)
    print("Training Disease Detection Model")
    print("="*50)
    
    disease_detector = DiseaseDetector()
    disease_history = disease_detector.train()
    
    print("\n" + "="*50)
    print("Model Training Complete!")
    print("="*50)
    print("All models have been trained and saved successfully.")
    print("You can now run the Flask application.")

if __name__ == "__main__":
    train_all_models()