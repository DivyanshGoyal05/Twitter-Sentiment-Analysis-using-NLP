# 🚀 Complete PyCharm Setup Guide for YouTube Sentiment Analyzer

This guide will help you set up and run the YouTube Comment Sentiment Analyzer project in PyCharm from scratch.

## 📋 Prerequisites

Before starting, make sure you have:
- PyCharm Community Edition (free) or Professional installed
- Python 3.8 or higher installed on your system
- A YouTube Data API v3 key (we'll get this together)

## 🔧 Step 1: Download and Install PyCharm

1. **Download PyCharm:**
   - Go to https://www.jetbrains.com/pycharm/download/
   - Download PyCharm Community Edition (it's free)
   - Install it following the installation wizard

2. **Install Python (if not already installed):**
   - Go to https://www.python.org/downloads/
   - Download Python 3.8 or higher
   - During installation, **CHECK** "Add Python to PATH"

## 📁 Step 2: Set Up the Project in PyCharm

### 2.1 Open the Project
1. **Open PyCharm**
2. **Click "Open"** (not "New Project")
3. **Navigate to your project folder** where you downloaded/cloned this project
4. **Select the folder** and click "OK"

### 2.2 Configure Python Interpreter
1. **Go to:** File → Settings (or PyCharm → Preferences on Mac)
2. **Navigate to:** Project → Python Interpreter
3. **Click the gear icon** → Add...
4. **Select "System Interpreter"**
5. **Choose your Python installation** (usually in C:\Python39\ or similar)
6. **Click "OK"**

## 🔑 Step 3: Get YouTube API Key

### 3.1 Create Google Cloud Project
1. **Go to:** https://console.cloud.google.com/
2. **Sign in** with your Google account
3. **Click "Create Project"**
4. **Enter project name:** "YouTube Sentiment Analyzer"
5. **Click "Create"**

### 3.2 Enable YouTube Data API
1. **In Google Cloud Console**, go to "APIs & Services" → "Library"
2. **Search for:** "YouTube Data API v3"
3. **Click on it** and then **click "Enable"**

### 3.3 Create API Key
1. **Go to:** "APIs & Services" → "Credentials"
2. **Click "Create Credentials"** → "API Key"
3. **Copy the API key** (keep it safe!)
4. **Click "Restrict Key"** (recommended)
5. **Under "API restrictions"**, select "YouTube Data API v3"
6. **Click "Save"**

## 🔧 Step 4: Install Required Libraries

### 4.1 Using PyCharm Terminal
1. **In PyCharm**, go to View → Tool Windows → Terminal
2. **Run these commands one by one:**

```bash
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install pandas==2.1.3
pip install numpy==1.24.3
pip install scikit-learn==1.3.2
pip install google-api-python-client==2.108.0
pip install python-multipart==0.0.6
pip install jinja2==3.1.2
pip install aiofiles==23.2.1
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install nltk
pip install contractions
```

### 4.2 Install NLTK Data
After installing nltk, run this in the terminal:
```bash
python -c "import nltk; nltk.download('wordnet'); nltk.download('punkt')"
```

## 🔐 Step 5: Set Up Environment Variables

### 5.1 Create .env File
1. **In PyCharm**, right-click on the project root folder
2. **Select:** New → File
3. **Name it:** `.env`
4. **Add this content** (replace YOUR_API_KEY with your actual key):

```
YOUTUBE_API_KEY=YOUR_ACTUAL_API_KEY_HERE
```

**Example:**
```
YOUTUBE_API_KEY=AIzaSyBvOkBdqY5PIiYlOXuqJNjuogvaStBGjPc
```

## ⚙️ Step 6: Configure PyCharm Run Configuration

### 6.1 Create Run Configuration for Main App
1. **Click the "Add Configuration" dropdown** (top right)
2. **Click "Edit Configurations..."**
3. **Click the "+" button** → Python
4. **Fill in these details:**
   - **Name:** `YouTube Sentiment Analyzer`
   - **Script path:** Click folder icon and select `main.py`
   - **Working directory:** Should be your project root folder
   - **Environment variables:** Click folder icon and add:
     - **Name:** `YOUTUBE_API_KEY`
     - **Value:** Your actual API key
5. **Click "OK"**

### 6.2 Alternative: Create Run Configuration for run.py
1. **Follow same steps as above** but:
   - **Name:** `Run YouTube Analyzer`
   - **Script path:** Select `run.py`
   - **Parameters:** Leave empty

## 🚀 Step 7: Run the Project

### Method 1: Using run.py (Recommended for beginners)
1. **Right-click on `run.py`** in the project explorer
2. **Select "Run 'run'"**
3. **The terminal will show startup messages**
4. **Open your browser** and go to: http://localhost:8000

### Method 2: Using main.py directly
1. **Use the run configuration** you created
2. **Click the green play button** next to "YouTube Sentiment Analyzer"
3. **Open your browser** and go to: http://localhost:8000

### Method 3: Using Terminal
1. **Open PyCharm terminal**
2. **Run:**
```bash
python run.py
```

## 🧪 Step 8: Test the Application

### 8.1 Basic Test
1. **Open browser** to http://localhost:8000
2. **You should see** the YouTube Comment Sentiment Analyzer interface
3. **Try entering a YouTube URL** like: https://www.youtube.com/watch?v=dQw4w9WgXcQ
4. **Click "Analyze"**

### 8.2 Test Individual Components
**Test Sentiment Analyzer:**
1. **Right-click** on `sentiment_analyzer.py`
2. **Select "Run 'sentiment_analyzer'"**
3. **Check console output** for test results

**Test YouTube Analyzer:**
1. **Right-click** on `youtube_analyzer.py`
2. **Select "Run 'youtube_analyzer'"**
3. **Check console output** for API connection test

## 🔧 Step 9: PyCharm Debugging Setup

### 9.1 Set Breakpoints
1. **Click in the left margin** next to line numbers to set breakpoints
2. **Useful places to set breakpoints:**
   - Line 1 of `main.py`
   - Inside `analyze_youtube_comments` function
   - Inside `analyze_sentiment` method

### 9.2 Debug Mode
1. **Click the debug button** (bug icon) instead of run
2. **Use the debug console** to inspect variables
3. **Step through code** using F8 (step over) and F7 (step into)

## 📁 Step 10: Project Structure Understanding

```
YouTube-Sentiment-Analysis/
├── main.py                 # Main FastAPI application
├── run.py                  # Easy launcher script
├── sentiment_analyzer.py   # ML sentiment analysis
├── youtube_analyzer.py     # YouTube API integration
├── requirements.txt        # Python dependencies
├── .env                   # Your API keys (create this)
├── templates/
│   └── index.html         # Web interface
├── static/                # CSS, JS files
├── scripts/               # CI/CD and utility scripts
└── LR_Pipeline.pickle     # Trained ML model
```

## 🐛 Common Issues and Solutions

### Issue 1: "Module not found" errors
**Solution:**
```bash
pip install [missing-module-name]
```

### Issue 2: "YouTube API not initialized"
**Solution:**
- Check your `.env` file has the correct API key
- Verify the API key works in Google Cloud Console
- Make sure YouTube Data API v3 is enabled

### Issue 3: "Port already in use"
**Solution:**
- Change port in `main.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`
- Or kill the process using the port

### Issue 4: "Permission denied" on Windows
**Solution:**
- Run PyCharm as Administrator
- Or use: `python -m pip install [package-name]`

### Issue 5: SSL Certificate errors
**Solution:**
```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org [package-name]
```

## 🎯 Quick Start Checklist

- [ ] PyCharm installed and project opened
- [ ] Python interpreter configured
- [ ] All packages installed via pip
- [ ] YouTube API key obtained
- [ ] .env file created with API key
- [ ] Run configuration created
- [ ] Project runs successfully
- [ ] Web interface accessible at localhost:8000
- [ ] Test analysis with a YouTube video

## 🆘 Getting Help

If you encounter issues:

1. **Check the PyCharm terminal** for error messages
2. **Look at the console output** when running the application
3. **Verify all files are present** in the project directory
4. **Check your internet connection** (needed for YouTube API)
5. **Ensure your API key is valid** and has quota remaining

## 🎉 Success!

Once everything is working, you should be able to:
- ✅ Access the web interface at http://localhost:8000
- ✅ Enter YouTube video URLs
- ✅ See sentiment analysis results with charts
- ✅ View categorized comments (positive/negative)

**Congratulations! You've successfully set up the YouTube Comment Sentiment Analyzer in PyCharm!**