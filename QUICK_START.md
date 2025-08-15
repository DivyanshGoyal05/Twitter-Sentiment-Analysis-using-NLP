# ⚡ Quick Start Guide (5 Minutes)

If you're in a hurry, follow these essential steps:

## 1. Install Python & PyCharm
- Download Python 3.8+ from python.org
- Download PyCharm Community from jetbrains.com

## 2. Open Project in PyCharm
- File → Open → Select project folder

## 3. Install Dependencies
Open PyCharm terminal and run:
```bash
pip install -r requirements.txt
pip install nltk contractions
python -c "import nltk; nltk.download('wordnet')"
```

## 4. Get YouTube API Key
- Go to console.cloud.google.com
- Create project → Enable YouTube Data API v3
- Create API Key

## 5. Create .env File
Create `.env` file in project root:
```
YOUTUBE_API_KEY=your_api_key_here
```

## 6. Run the Project
```bash
python run.py
```

## 7. Open Browser
Go to: http://localhost:8000

**That's it! You're ready to analyze YouTube comments!**