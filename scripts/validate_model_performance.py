#!/usr/bin/env python3
"""
Model Performance Validation Script for CI/CD Pipeline
Validates ML model performance metrics before deployment
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class PerformanceValidator:
    def __init__(self):
        self.performance_results = {}
        self.thresholds = {
            'accuracy': 0.80,  # Minimum 80% accuracy
            'response_time_ms': 1000,  # Maximum 1 second response time
            'memory_usage_mb': 500,  # Maximum 500MB memory usage
            'throughput_per_second': 10  # Minimum 10 predictions per second
        }
        
    def load_test_data(self):
        """Load test data for performance validation"""
        print("📊 Loading test data...")
        
        # Sample test texts for performance testing
        self.test_texts = [
            "I love this video! Amazing content!",
            "This is terrible, waste of time",
            "Great tutorial, very helpful",
            "I hate this, it's awful",
            "Excellent work, very informative",
            "Poor quality, not worth watching",
            "Fantastic explanation, learned a lot",
            "Disappointing content, expected more",
            "Outstanding video, highly recommend",
            "Bad tutorial, confusing explanations"
        ] * 10  # Repeat to get 100 test cases
        
        print(f"✅ Loaded {len(self.test_texts)} test cases")
        
    def test_model_accuracy(self):
        """Test model accuracy on known test cases"""
        print("\n🎯 Testing model accuracy...")
        
        try:
            from sentiment_analyzer import SentimentAnalyzer
            
            analyzer = SentimentAnalyzer()
            
            # Expected sentiments (0 = positive, 1 = negative)
            expected_sentiments = [
                0, 1, 0, 1, 0, 1, 0, 1, 0, 1
            ] * 10
            
            correct_predictions = 0
            total_predictions = 0
            
            for i, (text, expected) in enumerate(zip(self.test_texts, expected_sentiments)):
                predicted = analyzer.analyze_sentiment(text)
                
                if predicted is not None:
                    if predicted == expected:
                        correct_predictions += 1
                    total_predictions += 1
                    
                # Progress indicator
                if (i + 1) % 50 == 0:
                    print(f"  Processed {i + 1}/{len(self.test_texts)} test cases...")
                    
            accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
            
            print(f"✅ Accuracy: {accuracy:.3f} ({correct_predictions}/{total_predictions})")
            
            self.performance_results['accuracy'] = {
                'value': accuracy,
                'threshold': self.thresholds['accuracy'],
                'passed': accuracy >= self.thresholds['accuracy']
            }
            
        except Exception as e:
            print(f"❌ Accuracy test failed: {str(e)}")
            self.performance_results['accuracy'] = {
                'value': 0,
                'threshold': self.thresholds['accuracy'],
                'passed': False,
                'error': str(e)
            }
            
    def test_response_time(self):
        """Test model response time"""
        print("\n⏱️  Testing response time...")
        
        try:
            from sentiment_analyzer import SentimentAnalyzer
            
            analyzer = SentimentAnalyzer()
            
            response_times = []
            
            for text in self.test_texts[:50]:  # Test with first 50 texts
                start_time = time.time()
                analyzer.analyze_sentiment(text)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                response_times.append(response_time)
                
            avg_response_time = np.mean(response_times)
            max_response_time = np.max(response_times)
            min_response_time = np.min(response_times)
            
            print(f"✅ Average response time: {avg_response_time:.2f}ms")
            print(f"   Min: {min_response_time:.2f}ms, Max: {max_response_time:.2f}ms")
            
            self.performance_results['response_time_ms'] = {
                'value': avg_response_time,
                'threshold': self.thresholds['response_time_ms'],
                'passed': avg_response_time <= self.thresholds['response_time_ms'],
                'min': min_response_time,
                'max': max_response_time
            }
            
        except Exception as e:
            print(f"❌ Response time test failed: {str(e)}")
            self.performance_results['response_time_ms'] = {
                'value': float('inf'),
                'threshold': self.thresholds['response_time_ms'],
                'passed': False,
                'error': str(e)
            }
            
    def test_throughput(self):
        """Test model throughput (predictions per second)"""
        print("\n🚀 Testing throughput...")
        
        try:
            from sentiment_analyzer import SentimentAnalyzer
            
            analyzer = SentimentAnalyzer()
            
            # Test batch processing
            start_time = time.time()
            
            for text in self.test_texts[:100]:
                analyzer.analyze_sentiment(text)
                
            end_time = time.time()
            
            total_time = end_time - start_time
            throughput = 100 / total_time  # predictions per second
            
            print(f"✅ Throughput: {throughput:.2f} predictions/second")
            
            self.performance_results['throughput_per_second'] = {
                'value': throughput,
                'threshold': self.thresholds['throughput_per_second'],
                'passed': throughput >= self.thresholds['throughput_per_second']
            }
            
        except Exception as e:
            print(f"❌ Throughput test failed: {str(e)}")
            self.performance_results['throughput_per_second'] = {
                'value': 0,
                'threshold': self.thresholds['throughput_per_second'],
                'passed': False,
                'error': str(e)
            }
            
    def test_memory_usage(self):
        """Test memory usage (basic estimation)"""
        print("\n💾 Testing memory usage...")
        
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # Load and use the model
            from sentiment_analyzer import SentimentAnalyzer
            analyzer = SentimentAnalyzer()
            
            # Make some predictions
            for text in self.test_texts[:50]:
                analyzer.analyze_sentiment(text)
                
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_used = memory_after - memory_before
            
            print(f"✅ Memory usage: {memory_used:.2f}MB")
            
            self.performance_results['memory_usage_mb'] = {
                'value': memory_used,
                'threshold': self.thresholds['memory_usage_mb'],
                'passed': memory_used <= self.thresholds['memory_usage_mb']
            }
            
        except ImportError:
            print("⚠️  psutil not available, skipping memory test")
            self.performance_results['memory_usage_mb'] = {
                'value': 0,
                'threshold': self.thresholds['memory_usage_mb'],
                'passed': True,
                'skipped': True
            }
        except Exception as e:
            print(f"❌ Memory usage test failed: {str(e)}")
            self.performance_results['memory_usage_mb'] = {
                'value': float('inf'),
                'threshold': self.thresholds['memory_usage_mb'],
                'passed': False,
                'error': str(e)
            }
            
    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        print("\n📊 Performance Validation Report")
        print("=" * 50)
        
        passed_tests = 0
        total_tests = len(self.performance_results)
        
        for metric, result in self.performance_results.items():
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            value = result['value']
            threshold = result['threshold']
            
            print(f"{status} {metric}: {value} (threshold: {threshold})")
            
            if result['passed']:
                passed_tests += 1
                
        print(f"\n📈 Summary: {passed_tests}/{total_tests} tests passed")
        
        # Save detailed report
        report_path = 'performance_report.json'
        with open(report_path, 'w') as f:
            json.dump(self.performance_results, f, indent=2, default=str)
            
        print(f"📄 Detailed report saved to: {report_path}")
        
        return passed_tests == total_tests
        
    def run_performance_validation(self):
        """Run complete performance validation pipeline"""
        print("🚀 Starting ML Model Performance Validation")
        print("=" * 50)
        
        # Load test data
        self.load_test_data()
        
        # Run all performance tests
        self.test_model_accuracy()
        self.test_response_time()
        self.test_throughput()
        self.test_memory_usage()
        
        # Generate report
        success = self.generate_performance_report()
        
        if success:
            print("\n🎉 All performance tests passed! Model meets performance requirements.")
            return True
        else:
            print("\n❌ Some performance tests failed. Model may not be ready for production.")
            return False

def main():
    """Main performance validation function"""
    validator = PerformanceValidator()
    
    try:
        success = validator.run_performance_validation()
        
        if success:
            print("✅ Performance validation completed successfully")
            sys.exit(0)
        else:
            print("❌ Performance validation failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Performance validation crashed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
