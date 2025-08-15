# 🔧 Troubleshooting Guide

## Common PyCharm Setup Issues

### 1. Python Interpreter Not Found
**Problem:** PyCharm can't find Python
**Solution:**
1. File → Settings → Project → Python Interpreter
2. Click gear icon → Add → System Interpreter
3. Browse to Python installation (usually C:\Python39\python.exe)

### 2. Package Installation Fails
**Problem:** pip install commands fail
**Solutions:**
```bash
# Try upgrading pip first
python -m pip install --upgrade pip

# Use alternative index
pip install -i https://pypi.org/simple/ package-name

# Install with user flag
pip install --user package-name
```

### 3. YouTube API Key Issues
**Problem:** API not working
**Check:**
- API key is correct in .env file
- YouTube Data API v3 is enabled in Google Cloud
- API key has no restrictions or is restricted to YouTube Data API v3
- You haven't exceeded quota limits

### 4. Port Already in Use
**Problem:** "Address already in use" error
**Solutions:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (Windows)
taskkill /PID [process_id] /F

# Or change port in main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### 5. Module Import Errors
**Problem:** "ModuleNotFoundError"
**Solutions:**
1. Check if package is installed: `pip list`
2. Install missing package: `pip install package-name`
3. Verify Python interpreter in PyCharm settings

### 6. NLTK Data Missing
**Problem:** NLTK errors about missing data
**Solution:**
```bash
python -c "import nltk; nltk.download('all')"
```

### 7. File Path Issues
**Problem:** "File not found" errors
**Solution:**
- Ensure working directory is set to project root in run configuration
- Check that all required files (LR_Pipeline.pickle, etc.) are present

### 8. Permission Errors (Windows)
**Problem:** Permission denied errors
**Solutions:**
- Run PyCharm as Administrator
- Use: `python -m pip install package-name`
- Check antivirus isn't blocking Python

## Quick Diagnostic Commands

Run these in PyCharm terminal to check your setup:

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Test imports
python -c "import fastapi, uvicorn, pandas, sklearn; print('All packages imported successfully')"

# Test sentiment analyzer
python sentiment_analyzer.py

# Test YouTube analyzer
python youtube_analyzer.py

# Check if model files exist
python -c "import os; print('LR_Pipeline.pickle exists:', os.path.exists('LR_Pipeline.pickle'))"
```

## Getting More Help

If you're still stuck:
1. Check the error message in PyCharm's console
2. Look at the terminal output for specific error details
3. Verify all files from the project are present
4. Make sure your internet connection is working
5. Try running individual components to isolate the issue