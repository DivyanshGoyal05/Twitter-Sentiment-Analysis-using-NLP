# 🚀 Complete Deployment Guide for YouTube Sentiment Analyzer

This guide covers multiple deployment options for your YouTube Comment Sentiment Analyzer project, from simple cloud platforms to advanced containerized deployments.

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:
- ✅ Project working locally in PyCharm
- ✅ YouTube API key configured
- ✅ All required model files (LR_Pipeline.pickle, etc.)
- ✅ Dependencies listed in requirements.txt
- ✅ Environment variables configured

## 🌐 Deployment Options Overview

| Platform | Difficulty | Cost | Best For |
|----------|------------|------|----------|
| **Railway** | ⭐ Easy | Free tier | Beginners |
| **Render** | ⭐ Easy | Free tier | Simple deployment |
| **Heroku** | ⭐⭐ Medium | Paid | Professional apps |
| **PythonAnywhere** | ⭐ Easy | Free tier | Python-focused |
| **DigitalOcean** | ⭐⭐⭐ Hard | $5/month | Full control |
| **AWS/GCP** | ⭐⭐⭐⭐ Expert | Variable | Enterprise |

---

## 🚂 Option 1: Railway (Recommended for Beginners)

Railway is the easiest platform for beginners with automatic deployments.

### Step 1: Prepare Your Project

1. **Create a Procfile** in your project root:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. **Update main.py** for Railway:
```python
import os
port = int(os.environ.get("PORT", 8000))
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### Step 2: Deploy to Railway

1. **Go to:** https://railway.app/
2. **Sign up** with GitHub account
3. **Click "New Project"** → "Deploy from GitHub repo"
4. **Select your repository**
5. **Add environment variables:**
   - Key: `YOUTUBE_API_KEY`
   - Value: Your actual API key
6. **Deploy automatically starts**
7. **Get your URL** from Railway dashboard

### Step 3: Configure Domain (Optional)
- Railway provides a free subdomain
- You can add a custom domain in settings

---

## 🎨 Option 2: Render (Great Free Option)

Render offers excellent free hosting with automatic SSL.

### Step 1: Prepare for Render

1. **Create render.yaml** in project root:
```yaml
services:
  - type: web
    name: youtube-sentiment-analyzer
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: YOUTUBE_API_KEY
        sync: false
```

### Step 2: Deploy to Render

1. **Go to:** https://render.com/
2. **Sign up** with GitHub
3. **Click "New"** → "Web Service"
4. **Connect your GitHub repository**
5. **Configure:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. **Add environment variable:**
   - `YOUTUBE_API_KEY` = your API key
7. **Click "Create Web Service"**

### Step 3: Access Your App
- Render provides a free .onrender.com URL
- Automatic SSL certificate included

---

## 🟣 Option 3: Heroku (Professional Choice)

Heroku is reliable but requires payment (no free tier anymore).

### Step 1: Install Heroku CLI

**Windows:**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Prepare for Heroku

1. **Create Procfile:**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. **Create runtime.txt:**
```
python-3.9.18
```

3. **Update requirements.txt** (add gunicorn):
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
gunicorn==21.2.0
pandas==2.1.3
numpy==1.24.3
scikit-learn==1.3.2
google-api-python-client==2.108.0
python-multipart==0.0.6
jinja2==3.1.2
aiofiles==23.2.1
python-dotenv==1.0.0
requests==2.31.0
nltk==3.8.1
contractions==0.1.73
```

### Step 3: Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set YOUTUBE_API_KEY=your_api_key_here

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open your app
heroku open
```

---

## 🐍 Option 4: PythonAnywhere (Python-Focused)

Great for Python projects with easy setup.

### Step 1: Sign Up
1. **Go to:** https://www.pythonanywhere.com/
2. **Create free account**
3. **Go to dashboard**

### Step 2: Upload Your Project
1. **Open "Files" tab**
2. **Upload your project files** or clone from GitHub:
```bash
git clone https://github.com/yourusername/your-repo.git
```

### Step 3: Install Dependencies
1. **Open "Consoles" tab**
2. **Start a Bash console**
3. **Navigate to your project:**
```bash
cd your-project-folder
pip3.10 install --user -r requirements.txt
```

### Step 4: Configure Web App
1. **Go to "Web" tab**
2. **Click "Add a new web app"**
3. **Choose "Manual configuration"**
4. **Select Python 3.10**
5. **Set source code:** `/home/yourusername/your-project-folder`
6. **Edit WSGI file** to point to your FastAPI app

### Step 5: Set Environment Variables
1. **In "Files" tab**, edit `.bashrc`
2. **Add:** `export YOUTUBE_API_KEY=your_api_key_here`
3. **Reload web app**

---

## 🌊 Option 5: DigitalOcean Droplet (Advanced)

For those who want full control over their server.

### Step 1: Create Droplet
1. **Go to:** https://www.digitalocean.com/
2. **Create account** and get $200 credit
3. **Create Droplet:**
   - **Image:** Ubuntu 22.04 LTS
   - **Size:** Basic $6/month
   - **Add SSH key** for security

### Step 2: Server Setup
```bash
# Connect to your droplet
ssh root@your_droplet_ip

# Update system
apt update && apt upgrade -y

# Install Python and pip
apt install python3 python3-pip nginx -y

# Install git
apt install git -y

# Clone your project
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# Install dependencies
pip3 install -r requirements.txt

# Install process manager
pip3 install gunicorn
```

### Step 3: Configure Nginx
```bash
# Create Nginx config
nano /etc/nginx/sites-available/youtube-analyzer

# Add this configuration:
server {
    listen 80;
    server_name your_domain_or_ip;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
ln -s /etc/nginx/sites-available/youtube-analyzer /etc/nginx/sites-enabled/
systemctl restart nginx
```

### Step 4: Run Your App
```bash
# Set environment variable
export YOUTUBE_API_KEY=your_api_key_here

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 🐳 Option 6: Docker Deployment (Advanced)

For containerized deployment across any platform.

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Create docker-compose.yml
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - YOUTUBE_API_KEY=${YOUTUBE_API_KEY}
    volumes:
      - .:/app
```

### Step 3: Deploy with Docker
```bash
# Build and run
docker-compose up --build

# Or build and push to registry
docker build -t youtube-sentiment-analyzer .
docker tag youtube-sentiment-analyzer your-registry/youtube-sentiment-analyzer
docker push your-registry/youtube-sentiment-analyzer
```

---

## 🔧 Post-Deployment Configuration

### 1. Environment Variables
Always set these environment variables on your deployment platform:
- `YOUTUBE_API_KEY` - Your YouTube Data API key
- `PORT` - Port number (usually set automatically)

### 2. Domain Configuration
- Most platforms provide a free subdomain
- You can add custom domains in platform settings
- Enable HTTPS (usually automatic)

### 3. Monitoring and Logs
- Check application logs regularly
- Monitor API quota usage
- Set up error alerts if available

### 4. Database (Optional)
If you want persistent storage:
- Add PostgreSQL or MySQL database
- Update connection strings in environment variables
- Modify database initialization code

---

## 🚨 Common Deployment Issues

### Issue 1: Build Failures
**Problem:** Dependencies fail to install
**Solution:**
```bash
# Update requirements.txt with specific versions
# Remove any local-only packages
# Test locally first: pip install -r requirements.txt
```

### Issue 2: Port Issues
**Problem:** App doesn't start on correct port
**Solution:**
```python
# In main.py, always use environment PORT
import os
port = int(os.environ.get("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

### Issue 3: API Key Not Working
**Problem:** YouTube API returns errors
**Solution:**
- Verify API key is set correctly in platform
- Check API quotas in Google Cloud Console
- Ensure YouTube Data API v3 is enabled

### Issue 4: Large File Issues
**Problem:** Model files too large for deployment
**Solution:**
- Use Git LFS for large files
- Store models in cloud storage (AWS S3, Google Cloud Storage)
- Load models from URLs instead of local files

---

## 📊 Deployment Comparison

### Free Options:
1. **Railway** - Easiest, good free tier
2. **Render** - Reliable, automatic SSL
3. **PythonAnywhere** - Python-focused, good for learning

### Paid Options:
1. **Heroku** - Most reliable, professional features
2. **DigitalOcean** - Full control, scalable
3. **AWS/GCP** - Enterprise-grade, complex

---

## 🎯 Recommended Deployment Path

### For Beginners:
1. **Start with Railway** - Easiest setup
2. **Learn with Render** - Good free features
3. **Upgrade to Heroku** - When you need reliability

### For Advanced Users:
1. **Use Docker** - Consistent across environments
2. **Deploy to DigitalOcean** - Full control
3. **Scale with AWS/GCP** - Enterprise needs

---

## 🔗 Useful Resources

- **Railway Docs:** https://docs.railway.app/
- **Render Docs:** https://render.com/docs
- **Heroku Docs:** https://devcenter.heroku.com/
- **DigitalOcean Tutorials:** https://www.digitalocean.com/community/tutorials
- **Docker Docs:** https://docs.docker.com/

---

## 🎉 Success Checklist

After deployment, verify:
- [ ] App loads at your deployment URL
- [ ] YouTube URL analysis works
- [ ] Charts and visualizations display
- [ ] Comments are categorized correctly
- [ ] No console errors in browser
- [ ] API quota is not exceeded
- [ ] SSL certificate is active (HTTPS)

**Congratulations! Your YouTube Comment Sentiment Analyzer is now live and accessible to the world! 🚀**