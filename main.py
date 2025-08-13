from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import re
import json
from typing import List, Dict, Any
import pandas as pd
import numpy as np
import pickle
from datetime import datetime
import sqlite3
from pathlib import Path

# Import YouTube API functionality
from youtube_analyzer import YouTubeCommentAnalyzer
from sentiment_analyzer import SentimentAnalyzer

# Initialize FastAPI app
app = FastAPI(
    title="YouTube Comment Sentiment Analyzer",
    description="Analyze sentiment of YouTube video comments using ML",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize analyzers
sentiment_analyzer = SentimentAnalyzer()
youtube_analyzer = YouTubeCommentAnalyzer()

# Database setup
def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('sentiment_analysis.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            video_title TEXT,
            total_comments INTEGER,
            positive_count INTEGER,
            negative_count INTEGER,
            analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            results TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with the main interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_youtube_comments(video_url: str = Form(...)):
    """Analyze sentiment of YouTube video comments"""
    try:
        # Extract video ID from URL
        video_id = extract_video_id(video_url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        # Get video info and comments
        video_info = youtube_analyzer.get_video_info(video_id)
        comments = youtube_analyzer.get_video_comments(video_id)
        
        if not comments:
            raise HTTPException(status_code=404, detail="No comments found for this video")
        
        # Analyze sentiment of each comment
        analysis_results = []
        positive_count = 0
        negative_count = 0
        
        for comment in comments:
            sentiment = sentiment_analyzer.analyze_sentiment(comment['text'])
            analysis_results.append({
                'text': comment['text'],
                'author': comment['author'],
                'likes': comment['likes'],
                'sentiment': sentiment,
                'sentiment_label': 'Positive' if sentiment == 0 else 'Negative'
            })
            
            if sentiment == 0:
                positive_count += 1
            else:
                negative_count += 1
        
        # Calculate statistics
        total_comments = len(comments)
        positive_percentage = (positive_count / total_comments) * 100
        negative_percentage = (negative_count / total_comments) * 100
        
        # Prepare results
        results = {
            'video_info': video_info,
            'statistics': {
                'total_comments': total_comments,
                'positive_count': positive_count,
                'negative_count': negative_count,
                'positive_percentage': round(positive_percentage, 2),
                'negative_percentage': round(negative_percentage, 2)
            },
            'comments': analysis_results,
            'positive_comments': [c for c in analysis_results if c['sentiment'] == 0],
            'negative_comments': [c for c in analysis_results if c['sentiment'] == 1]
        }
        
        # Save to database
        save_analysis_to_db(video_id, video_info.get('title', ''), total_comments, 
                           positive_count, negative_count, json.dumps(results))
        
        return JSONResponse(content=results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: int):
    """Retrieve stored analysis results"""
    try:
        conn = sqlite3.connect('sentiment_analysis.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM analyses WHERE id = ?', (analysis_id,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return {
            'id': result[0],
            'video_id': result[1],
            'video_title': result[2],
            'total_comments': result[3],
            'positive_count': result[4],
            'negative_count': result[5],
            'analysis_date': result[6],
            'results': json.loads(result[7])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyses")
async def get_all_analyses():
    """Get list of all analyses"""
    try:
        conn = sqlite3.connect('sentiment_analysis.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, video_id, video_title, total_comments, positive_count, negative_count, analysis_date FROM analyses ORDER BY analysis_date DESC')
        results = cursor.fetchall()
        conn.close()
        
        analyses = []
        for result in results:
            analyses.append({
                'id': result[0],
                'video_id': result[1],
                'video_title': result[2],
                'total_comments': result[3],
                'positive_count': result[4],
                'negative_count': result[5],
                'analysis_date': result[6]
            })
        
        return analyses
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from various URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def save_analysis_to_db(video_id: str, video_title: str, total_comments: int, 
                        positive_count: int, negative_count: int, results: str):
    """Save analysis results to database"""
    conn = sqlite3.connect('sentiment_analysis.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analyses (video_id, video_title, total_comments, positive_count, negative_count, results)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (video_id, video_title, total_comments, positive_count, negative_count, results))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
