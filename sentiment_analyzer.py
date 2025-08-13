import pickle
import re
import contractions
from nltk.stem import WordNetLemmatizer
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import os

class SentimentAnalyzer:
    def __init__(self):
        """Initialize the sentiment analyzer with trained models"""
        self.lemmatizer = WordNetLemmatizer()
        self.load_models()
        
    def load_models(self):
        """Load the trained sentiment analysis models"""
        try:
            # Load the Logistic Regression pipeline
            with open('LR_Pipeline.pickle', 'rb') as handle:
                self.lr_model = pickle.load(handle)
            
            # Load the tokenizer if available
            if os.path.exists('tokenizer.pickle'):
                with open('tokenizer.pickle', 'rb') as handle:
                    self.tokenizer = pickle.load(handle)
            else:
                self.tokenizer = None
                
            print("✅ Models loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            self.lr_model = None
            self.tokenizer = None
    
    def clean_text(self, text):
        """Clean and preprocess text using the same pipeline as training"""
        if not isinstance(text, str):
            return ""
        
        # Apply the same cleaning steps used during training
        new_text = re.sub(r"'s\b", " is", text)
        new_text = re.sub("#", "", new_text)
        new_text = re.sub("@[A-Za-z0-9]+", "", new_text)
        new_text = re.sub(r"http\S+", "", new_text)
        new_text = contractions.fix(new_text)
        new_text = re.sub(r"[^a-zA-Z]", " ", new_text)
        new_text = new_text.lower().strip()
        
        # Apply lemmatization
        cleaned_text = ''
        for token in new_text.split():
            cleaned_text = cleaned_text + self.lemmatizer.lemmatize(token) + ' '
        
        return cleaned_text.strip()
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of given text
        Returns: 0 for positive, 1 for negative
        """
        if not self.lr_model:
            print("❌ Model not loaded. Please check if LR_Pipeline.pickle exists.")
            return None
        
        try:
            # Clean the text
            cleaned_text = self.clean_text(text)
            
            if not cleaned_text.strip():
                # If text is empty after cleaning, return neutral (0)
                return 0
            
            # Make prediction using the loaded model
            prediction = self.lr_model.predict([cleaned_text])
            
            # Return the prediction (0 = positive, 1 = negative)
            return int(prediction[0])
            
        except Exception as e:
            print(f"❌ Error analyzing sentiment: {e}")
            return None
    
    def analyze_batch_sentiments(self, texts):
        """
        Analyze sentiment of multiple texts
        Returns: List of sentiment scores
        """
        if not self.lr_model:
            return None
        
        try:
            # Clean all texts
            cleaned_texts = [self.clean_text(text) for text in texts]
            
            # Filter out empty texts
            valid_texts = [text for text in cleaned_texts if text.strip()]
            valid_indices = [i for i, text in enumerate(cleaned_texts) if text.strip()]
            
            if not valid_texts:
                return [0] * len(texts)  # Return neutral for all if no valid texts
            
            # Make batch predictions
            predictions = self.lr_model.predict(valid_texts)
            
            # Create results array with neutral (0) for invalid texts
            results = [0] * len(texts)
            for idx, pred in zip(valid_indices, predictions):
                results[idx] = int(pred)
            
            return results
            
        except Exception as e:
            print(f"❌ Error in batch sentiment analysis: {e}")
            return None
    
    def get_sentiment_label(self, sentiment_score):
        """Convert sentiment score to human-readable label"""
        if sentiment_score == 0:
            return "Positive"
        elif sentiment_score == 1:
            return "Negative"
        else:
            return "Unknown"
    
    def get_sentiment_confidence(self, text):
        """
        Get sentiment prediction with confidence score
        Returns: (sentiment, confidence)
        """
        if not self.lr_model:
            return None, None
        
        try:
            cleaned_text = self.clean_text(text)
            
            if not cleaned_text.strip():
                return 0, 0.5  # Neutral with 50% confidence
            
            # Get prediction probabilities
            probabilities = self.lr_model.predict_proba([cleaned_text])
            
            # Get the predicted class and its confidence
            predicted_class = np.argmax(probabilities[0])
            confidence = np.max(probabilities[0])
            
            return int(predicted_class), float(confidence)
            
        except Exception as e:
            print(f"❌ Error getting sentiment confidence: {e}")
            return None, None
    
    def get_model_info(self):
        """Get information about the loaded model"""
        if not self.lr_model:
            return "No model loaded"
        
        try:
            # Get model type and parameters
            model_type = type(self.lr_model).__name__
            
            # Get feature names if available
            if hasattr(self.lr_model, 'named_steps') and 'CV' in self.lr_model.named_steps:
                feature_count = len(self.lr_model.named_steps['CV'].vocabulary_)
            else:
                feature_count = "Unknown"
            
            return {
                "model_type": model_type,
                "feature_count": feature_count,
                "model_loaded": True
            }
            
        except Exception as e:
            return f"Error getting model info: {e}"

# Test the sentiment analyzer
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    # Test with sample texts
    test_texts = [
        "I love this video! Amazing content!",
        "This is terrible, waste of time",
        "Great tutorial, very helpful",
        "I hate this, it's awful"
    ]
    
    print("🧪 Testing Sentiment Analyzer:")
    print("=" * 50)
    
    for text in test_texts:
        sentiment = analyzer.analyze_sentiment(text)
        label = analyzer.get_sentiment_label(sentiment) if sentiment is not None else "Error"
        print(f"Text: {text}")
        print(f"Sentiment: {sentiment} ({label})")
        print("-" * 30)
    
    # Test batch analysis
    print("\n📊 Batch Analysis Results:")
    batch_results = analyzer.analyze_batch_sentiments(test_texts)
    if batch_results:
        for i, (text, result) in enumerate(zip(test_texts, batch_results)):
            label = analyzer.get_sentiment_label(result)
            print(f"{i+1}. {text} → {result} ({label})")
    
    # Get model info
    print(f"\n🔍 Model Information:")
    model_info = analyzer.get_model_info()
    print(model_info)
