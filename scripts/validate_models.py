#!/usr/bin/env python3
"""
Model Validation Script for CI/CD Pipeline
Validates ML models before deployment
"""

import os
import sys
import pickle
import json
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

class ModelValidator:
    def __init__(self):
        self.validation_results = []
        self.required_models = [
            'LR_Pipeline.pickle',
            'sentiment_analyzer.py'
        ]
        self.optional_models = [
            'BestModel.h5',
            'tokenizer.pickle'
        ]
        
    def validate_model_files(self):
        """Validate that all required model files exist and are accessible"""
        print("🔍 Validating model files...")
        
        for model_file in self.required_models:
            if not os.path.exists(model_file):
                self.validation_results.append({
                    'file': model_file,
                    'status': 'FAILED',
                    'error': 'File not found'
                })
                print(f"❌ {model_file}: File not found")
            else:
                self.validation_results.append({
                    'file': model_file,
                    'status': 'PASSED',
                    'error': None
                })
                print(f"✅ {model_file}: File exists")
                
        return all(result['status'] == 'PASSED' for result in self.validation_results)
    
    def validate_pickle_files(self):
        """Validate pickle files can be loaded and contain expected structure"""
        print("\n🔍 Validating pickle files...")
        
        pickle_files = [f for f in self.required_models + self.optional_models if f.endswith('.pickle')]
        
        for pickle_file in pickle_files:
            if not os.path.exists(pickle_file):
                continue
                
            try:
                with open(pickle_file, 'rb') as f:
                    model = pickle.load(f)
                    
                # Check if it's a scikit-learn pipeline
                if isinstance(model, Pipeline):
                    print(f"✅ {pickle_file}: Valid scikit-learn pipeline")
                    self.validation_results.append({
                        'file': pickle_file,
                        'status': 'PASSED',
                        'error': None,
                        'type': 'Pipeline'
                    })
                else:
                    print(f"⚠️  {pickle_file}: Not a pipeline, but loadable")
                    self.validation_results.append({
                        'file': pickle_file,
                        'status': 'WARNING',
                        'error': 'Not a pipeline',
                        'type': type(model).__name__
                    })
                    
            except Exception as e:
                print(f"❌ {pickle_file}: Failed to load - {str(e)}")
                self.validation_results.append({
                    'file': pickle_file,
                    'status': 'FAILED',
                    'error': str(e)
                })
                
    def validate_model_functionality(self):
        """Test basic model functionality with sample data"""
        print("\n🔍 Testing model functionality...")
        
        try:
            # Import and test sentiment analyzer
            from sentiment_analyzer import SentimentAnalyzer
            
            analyzer = SentimentAnalyzer()
            
            # Test with sample texts
            test_texts = [
                "I love this video! Amazing content!",
                "This is terrible, waste of time",
                "Great tutorial, very helpful"
            ]
            
            for text in test_texts:
                sentiment = analyzer.analyze_sentiment(text)
                if sentiment is not None:
                    print(f"✅ Sentiment analysis working: '{text[:30]}...' → {sentiment}")
                else:
                    print(f"❌ Sentiment analysis failed for: '{text[:30]}...'")
                    
        except Exception as e:
            print(f"❌ Model functionality test failed: {str(e)}")
            self.validation_results.append({
                'test': 'functionality',
                'status': 'FAILED',
                'error': str(e)
            })
            
    def validate_model_performance(self):
        """Basic performance validation"""
        print("\n🔍 Validating model performance...")
        
        try:
            from sentiment_analyzer import SentimentAnalyzer
            import time
            
            analyzer = SentimentAnalyzer()
            
            # Test response time
            test_text = "This is a test comment for performance validation"
            
            start_time = time.time()
            sentiment = analyzer.analyze_sentiment(test_text)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response_time < 1000:  # Less than 1 second
                print(f"✅ Response time: {response_time:.2f}ms (Good)")
                self.validation_results.append({
                    'test': 'performance',
                    'status': 'PASSED',
                    'response_time_ms': response_time
                })
            else:
                print(f"⚠️  Response time: {response_time:.2f}ms (Slow)")
                self.validation_results.append({
                    'test': 'performance',
                    'status': 'WARNING',
                    'response_time_ms': response_time
                })
                
        except Exception as e:
            print(f"❌ Performance validation failed: {str(e)}")
            
    def generate_validation_report(self):
        """Generate a comprehensive validation report"""
        print("\n📊 Validation Report")
        print("=" * 50)
        
        passed = sum(1 for result in self.validation_results if result['status'] == 'PASSED')
        failed = sum(1 for result in self.validation_results if result['status'] == 'FAILED')
        warnings = sum(1 for result in self.validation_results if result['status'] == 'WARNING')
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Warnings: {warnings}")
        
        if failed > 0:
            print("\n❌ Failed Validations:")
            for result in self.validation_results:
                if result['status'] == 'FAILED':
                    print(f"  - {result.get('file', result.get('test', 'Unknown'))}: {result['error']}")
                    
        if warnings > 0:
            print("\n⚠️  Warnings:")
            for result in self.validation_results:
                if result['status'] == 'WARNING':
                    print(f"  - {result.get('file', result.get('test', 'Unknown'))}: {result['error']}")
                    
        # Save report to file
        report_path = 'validation_report.json'
        with open(report_path, 'w') as f:
            json.dump(self.validation_results, f, indent=2, default=str)
            
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        return failed == 0
        
    def run_full_validation(self):
        """Run complete validation pipeline"""
        print("🚀 Starting ML Model Validation Pipeline")
        print("=" * 50)
        
        # Run all validation steps
        self.validate_model_files()
        self.validate_pickle_files()
        self.validate_model_functionality()
        self.validate_model_performance()
        
        # Generate report
        success = self.generate_validation_report()
        
        if success:
            print("\n🎉 All validations passed! Models are ready for deployment.")
            return True
        else:
            print("\n❌ Some validations failed. Please fix issues before deployment.")
            return False

def main():
    """Main validation function"""
    validator = ModelValidator()
    
    try:
        success = validator.run_full_validation()
        
        if success:
            print("✅ Validation pipeline completed successfully")
            sys.exit(0)
        else:
            print("❌ Validation pipeline failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Validation pipeline crashed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
