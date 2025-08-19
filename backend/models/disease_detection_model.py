import tensorflow as tf
from tensorflow import keras
import cv2
import numpy as np
from PIL import Image
import os

class DiseaseDetector:
    def __init__(self):
        self.model = None
        self.class_names = [
            'healthy', 'bacterial_blight', 'brown_spot', 'leaf_blast',
            'tungro', 'bacterial_leaf_streak', 'sheath_blight'
        ]
        self.is_trained = False
        self.load_model()
    
    def create_model(self):
        """Create CNN model for disease detection"""
        base_model = keras.applications.MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(224, 224, 3)
        )
        
        base_model.trainable = False
        
        model = keras.Sequential([
            base_model,
            keras.layers.GlobalAveragePooling2D(),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(len(self.class_names), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def preprocess_image(self, image):
        """Preprocess image for prediction"""
        # Convert PIL image to numpy array
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Resize image
        image = cv2.resize(image, (224, 224))
        
        # Normalize pixel values
        image = image.astype('float32') / 255.0
        
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        
        return image
    
    def generate_synthetic_data(self):
        """Generate synthetic training data for demonstration"""
        # This is a placeholder - in real implementation, you'd use actual plant disease images
        print("Generating synthetic training data...")
        
        X_train = np.random.random((1000, 224, 224, 3))
        y_train = keras.utils.to_categorical(
            np.random.randint(0, len(self.class_names), 1000),
            len(self.class_names)
        )
        
        X_val = np.random.random((200, 224, 224, 3))
        y_val = keras.utils.to_categorical(
            np.random.randint(0, len(self.class_names), 200),
            len(self.class_names)
        )
        
        return X_train, y_train, X_val, y_val
    
    def train(self):
        """Train the disease detection model"""
        print("Creating disease detection model...")
        self.model = self.create_model()
        
        # Generate synthetic data (replace with real data in production)
        X_train, y_train, X_val, y_val = self.generate_synthetic_data()
        
        print("Training disease detection model...")
        history = self.model.fit(
            X_train, y_train,
            epochs=10,  # Reduced for demo
            batch_size=32,
            validation_data=(X_val, y_val),
            verbose=1
        )
        
        self.save_model()
        self.is_trained = True
        
        print("Disease detection model training completed!")
        return history
    
    def predict(self, image):
        """Predict disease from image"""
        if not self.is_trained:
            print("Training disease detection model...")
            self.train()
        
        # Preprocess image
        processed_image = self.preprocess_image(image)
        
        # Make prediction
        predictions = self.model.predict(processed_image)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        return {
            'disease': self.class_names[predicted_class_idx],
            'confidence': confidence,
            'all_predictions': {
                self.class_names[i]: float(predictions[0][i])
                for i in range(len(self.class_names))
            }
        }
    
    def save_model(self):
        """Save trained model"""
        os.makedirs('models/trained_models', exist_ok=True)
        self.model.save('models/trained_models/disease_detection_model.h5')
    
    def load_model(self):
        """Load trained model"""
        try:
            self.model = keras.models.load_model('models/trained_models/disease_detection_model.h5')
            self.is_trained = True
            print("Disease detection model loaded successfully!")
            
        except Exception as e:
            print(f"Could not load disease detection model: {e}")
            self.is_trained = False