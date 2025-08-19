import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import pickle
import os

class CropYieldPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        self.load_model()
    
    def create_model(self, input_shape):
        """Create neural network model for yield prediction"""
        model = keras.Sequential([
            keras.layers.Dense(128, activation='relu', input_shape=(input_shape,)),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='linear')  # Regression output
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        return model
    
    def prepare_data(self):
        """Generate synthetic training data for demonstration"""
        np.random.seed(42)
        n_samples = 10000
        
        # Generate synthetic agricultural data
        data = {
            'area': np.random.uniform(0.5, 100, n_samples),
            'rainfall': np.random.uniform(200, 2000, n_samples),
            'temperature': np.random.uniform(15, 45, n_samples),
            'humidity': np.random.uniform(30, 90, n_samples),
            'ph': np.random.uniform(4.5, 8.5, n_samples),
            'nitrogen': np.random.uniform(0, 200, n_samples),
            'phosphorus': np.random.uniform(0, 100, n_samples),
            'potassium': np.random.uniform(0, 200, n_samples),
            'crop_type': np.random.choice(['wheat', 'rice', 'corn', 'soybean', 'cotton'], n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Create synthetic yield based on features (simplified model)
        df['yield'] = (
            df['area'] * 0.5 +
            df['rainfall'] * 0.002 +
            (40 - abs(df['temperature'] - 25)) * 0.1 +
            df['humidity'] * 0.01 +
            (7 - abs(df['ph'] - 6.5)) * 2 +
            df['nitrogen'] * 0.05 +
            df['phosphorus'] * 0.03 +
            df['potassium'] * 0.02 +
            np.random.normal(0, 2, n_samples)  # Add noise
        )
        
        return df
    
    def train(self):
        """Train the crop yield prediction model"""
        print("Preparing training data...")
        df = self.prepare_data()
        
        # Encode categorical variables
        df['crop_type_encoded'] = self.label_encoder.fit_transform(df['crop_type'])
        
        # Prepare features
        feature_columns = ['area', 'rainfall', 'temperature', 'humidity', 'ph', 
                          'nitrogen', 'phosphorus', 'potassium', 'crop_type_encoded']
        X = df[feature_columns].values
        y = df['yield'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Create and train model
        self.model = self.create_model(X_train_scaled.shape[1])
        
        print("Training model...")
        history = self.model.fit(
            X_train_scaled, y_train,
            epochs=100,
            batch_size=32,
            validation_data=(X_test_scaled, y_test),
            verbose=1
        )
        
        # Save model and preprocessors
        self.save_model()
        self.is_trained = True
        
        print("Model training completed!")
        return history
    
    def predict(self, features):
        """Predict crop yield"""
        if not self.is_trained:
            print("Training model...")
            self.train()
        
        # Convert crop type to encoded value
        crop_types = ['wheat', 'rice', 'corn', 'soybean', 'cotton']
        if features['crop_type'] in crop_types:
            crop_encoded = crop_types.index(features['crop_type'])
        else:
            crop_encoded = 0
        
        # Prepare feature array
        feature_array = np.array([[
            features['area'],
            features['rainfall'],
            features['temperature'],
            features['humidity'],
            features['ph'],
            features['nitrogen'],
            features['phosphorus'],
            features['potassium'],
            crop_encoded
        ]])
        
        # Scale features
        feature_scaled = self.scaler.transform(feature_array)
        
        # Make prediction
        prediction = self.model.predict(feature_scaled)[0][0]
        
        return max(0, prediction)  # Ensure non-negative yield
    
    def get_yield_recommendations(self, features):
        """Get recommendations to improve yield"""
        recommendations = []
        
        # Analyze pH
        if features['ph'] < 6.0:
            recommendations.append("Soil is too acidic. Consider adding lime to increase pH.")
        elif features['ph'] > 7.5:
            recommendations.append("Soil is too alkaline. Consider adding sulfur or organic matter.")
        
        # Analyze nutrients
        if features['nitrogen'] < 50:
            recommendations.append("Nitrogen levels are low. Consider nitrogen-rich fertilizers.")
        if features['phosphorus'] < 20:
            recommendations.append("Phosphorus levels are low. Apply phosphate fertilizers.")
        if features['potassium'] < 50:
            recommendations.append("Potassium levels are low. Use potash fertilizers.")
        
        # Analyze environmental conditions
        if features['rainfall'] < 400:
            recommendations.append("Low rainfall detected. Implement irrigation systems.")
        if features['temperature'] > 35:
            recommendations.append("High temperature stress. Consider shade nets or cooling systems.")
        if features['humidity'] < 40:
            recommendations.append("Low humidity. Increase irrigation frequency.")
        
        return recommendations
    
    def save_model(self):
        """Save trained model and preprocessors"""
        os.makedirs('models/trained_models', exist_ok=True)
        
        self.model.save('models/trained_models/crop_yield_model.h5')
        
        with open('models/trained_models/yield_scaler.pkl', 'wb') as f:
            pickle.dump(self.scaler, f)
        
        with open('models/trained_models/yield_label_encoder.pkl', 'wb') as f:
            pickle.dump(self.label_encoder, f)
    
    def load_model(self):
        """Load trained model and preprocessors"""
        try:
            self.model = keras.models.load_model('models/trained_models/crop_yield_model.h5')
            
            with open('models/trained_models/yield_scaler.pkl', 'rb') as f:
                self.scaler = pickle.load(f)
            
            with open('models/trained_models/yield_label_encoder.pkl', 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            self.is_trained = True
            print("Yield prediction model loaded successfully!")
            
        except Exception as e:
            print(f"Could not load yield model: {e}")
            self.is_trained = False