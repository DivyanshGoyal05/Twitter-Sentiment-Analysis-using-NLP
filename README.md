# 🎥 YouTube Comment Sentiment Analyzer

A powerful web application that analyzes the sentiment of YouTube video comments using advanced Machine Learning techniques. Built with FastAPI, this tool provides instant insights into audience reactions and engagement.

## ✨ Features

- **🔗 One-Click Analysis**: Just paste a YouTube URL and get instant sentiment analysis
- **📊 Beautiful Visualizations**: Interactive charts showing sentiment distribution
- **💬 Comment Categorization**: Automatically groups comments by sentiment
- **📈 Real-time Statistics**: View counts, percentages, and detailed metrics
- **💾 Data Persistence**: Save analysis results for future reference
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **🚀 Fast Performance**: Built with FastAPI for optimal speed

## 🎯 What It Does

1. **Fetches Comments**: Automatically retrieves all comments from any YouTube video
2. **Sentiment Analysis**: Uses trained ML models to classify each comment as positive or negative
3. **Data Visualization**: Creates beautiful charts and statistics
4. **Comment Organization**: Groups comments by sentiment for easy review
5. **Results Storage**: Saves analysis data for future reference

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS) → FastAPI Backend → ML Models → YouTube API
     ↓                        ↓              ↓           ↓
  Beautiful UI           REST API        Sentiment   Comment
  & Charts              Endpoints       Analysis    Fetching
```

## 🛠️ Tech Stack

- **Backend**: FastAPI + Python
- **Frontend**: HTML5 + CSS3 + JavaScript + Bootstrap 5
- **Charts**: Chart.js for data visualization
- **ML Models**: Your trained sentiment analysis models
- **Database**: SQLite for data persistence
- **APIs**: YouTube Data API v3
- **Deployment**: Uvicorn server

## 📋 Prerequisites

- Python 3.8 or higher
- YouTube Data API v3 key
- Internet connection

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Twitter-Sentiment-Analysis-using-NLP
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Copy your API key

### 4. Set Environment Variables
Create a `.env` file in the project root:
```bash
YOUTUBE_API_KEY=your_youtube_api_key_here
```

Or set it as an environment variable:
```bash
# Windows
set YOUTUBE_API_KEY=your_key_here

# macOS/Linux
export YOUTUBE_API_KEY=your_key_here
```

### 5. Verify Model Files
Ensure these files exist in your project directory:
- `LR_Pipeline.pickle` - Your trained Logistic Regression model
- `BestModel.h5` - Your trained Neural Network model (optional)
- `tokenizer.pickle` - Text tokenizer (optional)

## 🎮 Usage

### 1. Start the Application
```bash
python main.py
```

### 2. Open Your Browser
Navigate to: `http://localhost:8000`

### 3. Analyze YouTube Comments
1. Paste a YouTube video URL in the input field
2. Click "Analyze" button
3. Wait for the analysis to complete
4. View results with charts and categorized comments

## 📊 Understanding Results

### Sentiment Categories
- **🟢 Positive (0)**: Comments expressing positive sentiment
- **🔴 Negative (1)**: Comments expressing negative sentiment

### Statistics Displayed
- Total comment count
- Positive comment count and percentage
- Negative comment count and percentage
- Interactive pie chart visualization

### Comment Organization
- **All Comments**: Complete list with sentiment labels
- **Positive Comments**: Only positive sentiment comments
- **Negative Comments**: Only negative sentiment comments

## 🔧 API Endpoints

### Main Endpoints
- `GET /` - Home page with analysis interface
- `POST /analyze` - Analyze YouTube video comments
- `GET /analysis/{id}` - Retrieve stored analysis results
- `GET /analyses` - List all analyses

### API Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## 📁 Project Structure

```
Twitter-Sentiment-Analysis-using-NLP/
├── main.py                 # FastAPI main application
├── sentiment_analyzer.py   # ML model integration
├── youtube_analyzer.py     # YouTube API integration
├── requirements.txt        # Python dependencies
├── env_example.txt         # Environment variables template
├── templates/
│   └── index.html         # Main web interface
├── static/                 # Static files (CSS, JS, images)
├── README.md              # This file
└── Your ML Models:
    ├── LR_Pipeline.pickle # Trained Logistic Regression
    ├── BestModel.h5       # Trained Neural Network
    └── tokenizer.pickle   # Text tokenizer
```

## 🧪 Testing

### Test Sentiment Analyzer
```bash
python sentiment_analyzer.py
```

### Test YouTube Integration
```bash
python youtube_analyzer.py
```

### Test Complete Application
```bash
python main.py
# Then visit http://localhost:8000 in your browser
```

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production with Uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment Options
- **Heroku**: Easy deployment with free tier
- **PythonAnywhere**: Python-focused hosting
- **AWS/GCP**: Scalable cloud solutions
- **Railway**: Simple deployment platform

## 🔍 Troubleshooting

### Common Issues

#### 1. YouTube API Key Error
```
Error: YouTube API not initialized
```
**Solution**: Check your API key in `.env` file or environment variables

#### 2. Model Loading Error
```
Error: Model not loaded
```
**Solution**: Ensure `LR_Pipeline.pickle` exists in project directory

#### 3. API Quota Exceeded
```
Error: Quota exceeded
```
**Solution**: Wait for quota reset or upgrade your YouTube API plan

#### 4. Comments Disabled
```
Warning: Comments are disabled
```
**Solution**: Try a different video with enabled comments

### Performance Tips
- Limit comment analysis to 100-500 comments for faster processing
- Use videos with moderate comment counts for testing
- Monitor API quota usage

## 📈 Future Enhancements

- **Multi-language Support**: Analyze comments in different languages
- **Real-time Monitoring**: Track sentiment changes over time
- **Batch Processing**: Analyze multiple videos simultaneously
- **Advanced Analytics**: Trend analysis and insights
- **Export Features**: Download results as CSV/PDF
- **User Authentication**: Save user preferences and history

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **YouTube Data API**: For providing access to video and comment data
- **FastAPI**: For the modern, fast web framework
- **Chart.js**: For beautiful data visualizations
- **Bootstrap**: For responsive UI components
- **Your ML Models**: For the core sentiment analysis capabilities

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the API documentation at `/docs`
3. Open an issue on GitHub
4. Check your YouTube API quota and settings

## 🎉 Success Stories

This tool is perfect for:
- **Content Creators**: Understanding audience reactions
- **Marketers**: Analyzing campaign effectiveness
- **Researchers**: Studying public sentiment trends
- **Businesses**: Monitoring brand perception
- **Students**: Learning ML and web development

---

**Made with ❤️ using FastAPI and Machine Learning**

*Transform your YouTube research into actionable insights!*
