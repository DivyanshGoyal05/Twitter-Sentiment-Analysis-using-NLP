import os
import re
from typing import List, Dict, Any, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

class YouTubeCommentAnalyzer:
    def __init__(self):
        """Initialize YouTube API client"""
        self.api_key = self._get_api_key()
        self.youtube = None
        self._initialize_api()
    
    def _get_api_key(self) -> Optional[str]:
        """Get YouTube API key from environment variable"""
        api_key = os.getenv('YOUTUBE_API_KEY')
        if not api_key:
            # Try to load from .env file
            try:
                from dotenv import load_dotenv
                load_dotenv()
                api_key = os.getenv('YOUTUBE_API_KEY')
            except ImportError:
                pass
        
        if not api_key:
            print("⚠️  Warning: YOUTUBE_API_KEY not found!")
            print("   Please set your YouTube API key in .env file or environment variable")
            print("   Get your API key from: https://console.cloud.google.com/apis/credentials")
        
        return api_key
    
    def _initialize_api(self):
        """Initialize YouTube API client"""
        if self.api_key:
            try:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
                print("✅ YouTube API initialized successfully!")
            except Exception as e:
                print(f"❌ Error initializing YouTube API: {e}")
                self.youtube = None
        else:
            self.youtube = None
    
    def get_video_info(self, video_id: str) -> Dict[str, Any]:
        """
        Get basic information about a YouTube video
        Returns: Dictionary with video details
        """
        if not self.youtube:
            return {"error": "YouTube API not initialized"}
        
        try:
            # Get video details
            request = self.youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            response = request.execute()
            
            if not response['items']:
                return {"error": "Video not found"}
            
            video = response['items'][0]
            snippet = video['snippet']
            statistics = video.get('statistics', {})
            
            video_info = {
                'id': video_id,
                'title': snippet.get('title', 'Unknown Title'),
                'description': snippet.get('description', '')[:200] + '...' if snippet.get('description', '') else '',
                'channel_title': snippet.get('channelTitle', 'Unknown Channel'),
                'published_at': snippet.get('publishedAt', 'Unknown Date'),
                'view_count': int(statistics.get('viewCount', 0)),
                'like_count': int(statistics.get('likeCount', 0)),
                'comment_count': int(statistics.get('commentCount', 0)),
                'thumbnail': snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
                'tags': snippet.get('tags', [])[:5]  # First 5 tags
            }
            
            return video_info
            
        except HttpError as e:
            error_details = json.loads(e.content.decode())
            return {"error": f"YouTube API error: {error_details.get('error', {}).get('message', str(e))}"}
        except Exception as e:
            return {"error": f"Error fetching video info: {str(e)}"}
    
    def get_video_comments(self, video_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Get comments from a YouTube video
        Returns: List of comment dictionaries
        """
        if not self.youtube:
            return []
        
        try:
            comments = []
            next_page_token = None
            
            # Get comments in batches
            while len(comments) < max_results:
                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=min(100, max_results - len(comments)),
                    pageToken=next_page_token,
                    order="relevance"  # Most relevant comments first
                )
                
                response = request.execute()
                
                for item in response['items']:
                    snippet = item['snippet']['topLevelComment']['snippet']
                    
                    comment = {
                        'id': item['id'],
                        'text': snippet.get('textDisplay', ''),
                        'author': snippet.get('authorDisplayName', 'Anonymous'),
                        'author_channel': snippet.get('authorChannelUrl', ''),
                        'likes': snippet.get('likeCount', 0),
                        'published_at': snippet.get('publishedAt', ''),
                        'updated_at': snippet.get('updatedAt', ''),
                        'total_reply_count': item['snippet'].get('totalReplyCount', 0)
                    }
                    
                    # Clean comment text (remove HTML tags)
                    comment['text'] = self._clean_html(comment['text'])
                    
                    # Only add non-empty comments
                    if comment['text'].strip():
                        comments.append(comment)
                    
                    if len(comments) >= max_results:
                        break
                
                # Check if there are more pages
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
            
            print(f"✅ Fetched {len(comments)} comments from video {video_id}")
            return comments
            
        except HttpError as e:
            error_details = json.loads(e.content.decode())
            error_message = error_details.get('error', {}).get('message', str(e))
            
            if 'commentsDisabled' in error_message:
                print(f"⚠️  Comments are disabled for video {video_id}")
                return []
            elif 'quotaExceeded' in error_message:
                print("❌ YouTube API quota exceeded. Please try again later.")
                return []
            else:
                print(f"❌ YouTube API error: {error_message}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching comments: {str(e)}")
            return []
    
    def _clean_html(self, text: str) -> str:
        """Remove HTML tags from text"""
        # Remove common HTML tags
        clean_text = re.sub(r'<[^>]+>', '', text)
        # Remove HTML entities
        clean_text = re.sub(r'&[a-zA-Z]+;', '', clean_text)
        # Remove extra whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text
    
    def get_channel_comments(self, channel_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent comments from a YouTube channel
        Returns: List of comment dictionaries
        """
        if not self.youtube:
            return []
        
        try:
            comments = []
            next_page_token = None
            
            while len(comments) < max_results:
                request = self.youtube.commentThreads().list(
                    part="snippet",
                    allThreadsRelatedToChannelId=channel_id,
                    maxResults=min(100, max_results - len(comments)),
                    pageToken=next_page_token,
                    order="time"  # Most recent comments first
                )
                
                response = request.execute()
                
                for item in response['items']:
                    snippet = item['snippet']['topLevelComment']['snippet']
                    
                    comment = {
                        'id': item['id'],
                        'text': self._clean_html(snippet.get('textDisplay', '')),
                        'author': snippet.get('authorDisplayName', 'Anonymous'),
                        'video_id': item['snippet'].get('videoId', ''),
                        'likes': snippet.get('likeCount', 0),
                        'published_at': snippet.get('publishedAt', '')
                    }
                    
                    if comment['text'].strip():
                        comments.append(comment)
                    
                    if len(comments) >= max_results:
                        break
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
            
            return comments
            
        except Exception as e:
            print(f"❌ Error fetching channel comments: {str(e)}")
            return []
    
    def search_videos(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for YouTube videos
        Returns: List of video dictionaries
        """
        if not self.youtube:
            return []
        
        try:
            request = self.youtube.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=max_results,
                order="relevance"
            )
            
            response = request.execute()
            videos = []
            
            for item in response['items']:
                snippet = item['snippet']
                video = {
                    'id': item['id']['videoId'],
                    'title': snippet.get('title', 'Unknown Title'),
                    'description': snippet.get('description', '')[:100] + '...' if snippet.get('description', '') else '',
                    'channel_title': snippet.get('channelTitle', 'Unknown Channel'),
                    'published_at': snippet.get('publishedAt', 'Unknown Date'),
                    'thumbnail': snippet.get('thumbnails', {}).get('medium', {}).get('url', '')
                }
                videos.append(video)
            
            return videos
            
        except Exception as e:
            print(f"❌ Error searching videos: {str(e)}")
            return []
    
    def get_api_status(self) -> Dict[str, Any]:
        """Get YouTube API status and quota information"""
        if not self.youtube:
            return {"status": "API not initialized"}
        
        try:
            # Try a simple API call to check status
            request = self.youtube.videos().list(
                part="snippet",
                id="dQw4w9WgXcQ"  # Rick Roll video ID for testing
            )
            response = request.execute()
            
            return {
                "status": "API working",
                "api_key_set": bool(self.api_key),
                "quota_available": True
            }
            
        except HttpError as e:
            error_details = json.loads(e.content.decode())
            error_message = error_details.get('error', {}).get('message', str(e))
            
            if 'quotaExceeded' in error_message:
                return {
                    "status": "Quota exceeded",
                    "api_key_set": bool(self.api_key),
                    "quota_available": False
                }
            else:
                return {
                    "status": f"API error: {error_message}",
                    "api_key_set": bool(self.api_key),
                    "quota_available": False
                }
                
        except Exception as e:
            return {
                "status": f"Error: {str(e)}",
                "api_key_set": bool(self.api_key),
                "quota_available": False
            }

# Test the YouTube analyzer
if __name__ == "__main__":
    analyzer = YouTubeCommentAnalyzer()
    
    print("🧪 Testing YouTube Comment Analyzer:")
    print("=" * 50)
    
    # Check API status
    status = analyzer.get_api_status()
    print(f"API Status: {status}")
    
    if status['status'] == 'API working':
        # Test with a popular video (Rick Roll)
        video_id = "dQw4w9WgXcQ"
        
        print(f"\n📹 Testing with video: {video_id}")
        
        # Get video info
        video_info = analyzer.get_video_info(video_id)
        if 'error' not in video_info:
            print(f"Title: {video_info['title']}")
            print(f"Channel: {video_info['channel_title']}")
            print(f"Views: {video_info['view_count']:,}")
            print(f"Comments: {video_info['comment_count']:,}")
        
        # Get comments (limit to 10 for testing)
        comments = analyzer.get_video_comments(video_id, max_results=10)
        print(f"\n💬 Fetched {len(comments)} comments")
        
        if comments:
            print("\nSample comments:")
            for i, comment in enumerate(comments[:3]):
                print(f"{i+1}. {comment['author']}: {comment['text'][:100]}...")
    
    else:
        print("\n❌ Cannot test without working API key")
        print("Please set YOUTUBE_API_KEY environment variable")
