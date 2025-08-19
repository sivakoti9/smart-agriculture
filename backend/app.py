from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import pandas as pd
from PIL import Image
import cv2
import json
import pickle
from models.crop_yield_model import CropYieldPredictor
from models.disease_detection_model import DiseaseDetector
from models.recommendation_engine import RecommendationEngine

app = Flask(__name__)
CORS(app)

# Initialize models
yield_predictor = CropYieldPredictor()
disease_detector = DiseaseDetector()
recommendation_engine = RecommendationEngine()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict_yield', methods=['POST'])
def predict_yield():
    try:
        data = request.json
        
        # Extract features
        features = {
            'area': float(data.get('area', 0)),
            'rainfall': float(data.get('rainfall', 0)),
            'temperature': float(data.get('temperature', 0)),
            'humidity': float(data.get('humidity', 0)),
            'ph': float(data.get('ph', 0)),
            'nitrogen': float(data.get('nitrogen', 0)),
            'phosphorus': float(data.get('phosphorus', 0)),
            'potassium': float(data.get('potassium', 0)),
            'crop_type': data.get('crop_type', 'wheat')
        }
        
        prediction = yield_predictor.predict(features)
        recommendations = yield_predictor.get_yield_recommendations(features)
        
        return jsonify({
            'success': True,
            'predicted_yield': prediction,
            'recommendations': recommendations,
            'unit': 'tons/hectare'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/detect_disease', methods=['POST'])
def detect_disease():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No image selected'})
        
        # Process image
        image = Image.open(file.stream)
        
        # Detect disease
        disease_result = disease_detector.predict(image)
        
        # Get medicine recommendations
        if disease_result['confidence'] > 0.7:
            medicine_suggestions = recommendation_engine.get_medicine_suggestions(
                disease_result['disease']
            )
            treatment_tips = recommendation_engine.get_treatment_tips(
                disease_result['disease']
            )
        else:
            medicine_suggestions = []
            treatment_tips = ["Image quality insufficient for accurate diagnosis"]
        
        return jsonify({
            'success': True,
            'disease': disease_result['disease'],
            'confidence': disease_result['confidence'],
            'medicine_suggestions': medicine_suggestions,
            'treatment_tips': treatment_tips
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.json
        crop_type = data.get('crop_type')
        season = data.get('season')
        location = data.get('location')
        
        recommendations = recommendation_engine.get_crop_recommendations(
            crop_type, season, location
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)