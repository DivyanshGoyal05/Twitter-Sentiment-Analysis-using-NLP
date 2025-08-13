#!/usr/bin/env python3
"""
YouTube Comment Sentiment Analyzer - Launch Script
Simple script to run the FastAPI application
"""

import uvicorn
import os
import sys
from pathlib import Path

def check_requirements():
    """Check if required files exist"""
    required_files = [
        'LR_Pipeline.pickle',
        'main.py',
        'sentiment_analyzer.py',
        'youtube_analyzer.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all required files are in the current directory.")
        return False
    
    return True

def check_api_key():
    """Check if YouTube API key is set"""
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("⚠️  Warning: YOUTUBE_API_KEY not found!")
        print("   Please set your YouTube API key:")
        print("   - Create a .env file with: YOUTUBE_API_KEY=your_key_here")
        print("   - Or set environment variable: export YOUTUBE_API_KEY=your_key_here")
        print("   - Get your API key from: https://console.cloud.google.com/apis/credentials")
        print()
        return False
    
    print("✅ YouTube API key found!")
    return True

def main():
    """Main launch function"""
    print("🚀 YouTube Comment Sentiment Analyzer")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check API key
    check_api_key()
    
    print("\n🎯 Starting the application...")
    print("📱 Open your browser and go to: http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        # Run the FastAPI application
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,  # Enable auto-reload for development
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
