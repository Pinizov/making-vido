#!/usr/bin/env python3
"""
YouTube Tutorial Data Scraper
Extracts data from YouTube tutorials and generates an AI database file.
"""

import json
import sqlite3
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
import argparse


try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed. Install it with: pip install yt-dlp")
    sys.exit(1)


class YouTubeScraper:
    """Scraper for extracting data from YouTube tutorials."""
    
    def __init__(self):
        """Initialize the YouTube scraper."""
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'skip_download': True,
        }
    
    def extract_video_data(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Extract data from a YouTube video URL.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dictionary containing video metadata or None if extraction fails
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Extract relevant information
                video_data = {
                    'video_id': info.get('id'),
                    'title': info.get('title'),
                    'description': info.get('description'),
                    'duration': info.get('duration'),
                    'upload_date': info.get('upload_date'),
                    'uploader': info.get('uploader'),
                    'uploader_id': info.get('uploader_id'),
                    'channel': info.get('channel'),
                    'channel_id': info.get('channel_id'),
                    'view_count': info.get('view_count'),
                    'like_count': info.get('like_count'),
                    'comment_count': info.get('comment_count'),
                    'categories': info.get('categories', []),
                    'tags': info.get('tags', []),
                    'thumbnail': info.get('thumbnail'),
                    'url': url,
                    'scraped_at': datetime.now().isoformat(),
                }
                
                # Extract subtitles/captions if available
                subtitles = []
                if info.get('subtitles'):
                    for lang, subs in info.get('subtitles', {}).items():
                        for sub in subs:
                            subtitles.append({
                                'language': lang,
                                'url': sub.get('url'),
                                'ext': sub.get('ext')
                            })
                
                video_data['subtitles'] = subtitles
                
                # Extract automatic captions
                auto_captions = []
                if info.get('automatic_captions'):
                    for lang, caps in info.get('automatic_captions', {}).items():
                        for cap in caps:
                            auto_captions.append({
                                'language': lang,
                                'url': cap.get('url'),
                                'ext': cap.get('ext')
                            })
                
                video_data['automatic_captions'] = auto_captions
                
                return video_data
                
        except Exception as e:
            print(f"Error extracting video data from {url}: {e}")
            return None
    
    def extract_playlist_data(self, url: str) -> List[Dict[str, Any]]:
        """
        Extract data from all videos in a YouTube playlist.
        
        Args:
            url: YouTube playlist URL
            
        Returns:
            List of dictionaries containing video metadata
        """
        videos = []
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                playlist_info = ydl.extract_info(url, download=False)
                
                if 'entries' in playlist_info:
                    for entry in playlist_info['entries']:
                        if entry:
                            video_url = f"https://www.youtube.com/watch?v={entry.get('id')}"
                            video_data = self.extract_video_data(video_url)
                            if video_data:
                                videos.append(video_data)
                                print(f"Extracted: {video_data['title']}")
        
        except Exception as e:
            print(f"Error extracting playlist data from {url}: {e}")
        
        return videos
    
    def extract_channel_videos(self, url: str, max_videos: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Extract data from videos in a YouTube channel.
        
        Args:
            url: YouTube channel URL
            max_videos: Maximum number of videos to extract (None for all)
            
        Returns:
            List of dictionaries containing video metadata
        """
        videos = []
        
        try:
            ydl_opts = self.ydl_opts.copy()
            if max_videos:
                ydl_opts['playlistend'] = max_videos
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                channel_info = ydl.extract_info(url, download=False)
                
                if 'entries' in channel_info:
                    for entry in channel_info['entries']:
                        if entry:
                            video_url = f"https://www.youtube.com/watch?v={entry.get('id')}"
                            video_data = self.extract_video_data(video_url)
                            if video_data:
                                videos.append(video_data)
                                print(f"Extracted: {video_data['title']}")
                                
                                if max_videos and len(videos) >= max_videos:
                                    break
        
        except Exception as e:
            print(f"Error extracting channel videos from {url}: {e}")
        
        return videos


class AIDatabase:
    """Generate and manage AI database files from scraped YouTube data."""
    
    @staticmethod
    def save_to_json(data: List[Dict[str, Any]], filename: str) -> None:
        """
        Save scraped data to a JSON file.
        
        Args:
            data: List of video data dictionaries
            filename: Output filename
        """
        try:
            output_path = os.path.abspath(filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'metadata': {
                        'generated_at': datetime.now().isoformat(),
                        'total_videos': len(data),
                        'version': '1.0'
                    },
                    'videos': data
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\nJSON database saved to: {output_path}")
            print(f"Total videos: {len(data)}")
        
        except Exception as e:
            print(f"Error saving JSON database: {e}")
    
    @staticmethod
    def save_to_sqlite(data: List[Dict[str, Any]], filename: str) -> None:
        """
        Save scraped data to a SQLite database file.
        
        Args:
            data: List of video data dictionaries
            filename: Output filename
        """
        try:
            output_path = os.path.abspath(filename)
            
            # Remove existing database if it exists
            if os.path.exists(output_path):
                os.remove(output_path)
            
            conn = sqlite3.connect(output_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE videos (
                    video_id TEXT PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    duration INTEGER,
                    upload_date TEXT,
                    uploader TEXT,
                    uploader_id TEXT,
                    channel TEXT,
                    channel_id TEXT,
                    view_count INTEGER,
                    like_count INTEGER,
                    comment_count INTEGER,
                    thumbnail TEXT,
                    url TEXT,
                    scraped_at TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT,
                    tag TEXT,
                    FOREIGN KEY (video_id) REFERENCES videos(video_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT,
                    category TEXT,
                    FOREIGN KEY (video_id) REFERENCES videos(video_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE subtitles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT,
                    language TEXT,
                    url TEXT,
                    ext TEXT,
                    subtitle_type TEXT,
                    FOREIGN KEY (video_id) REFERENCES videos(video_id)
                )
            ''')
            
            # Insert data
            for video in data:
                cursor.execute('''
                    INSERT INTO videos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    video.get('video_id'),
                    video.get('title'),
                    video.get('description'),
                    video.get('duration'),
                    video.get('upload_date'),
                    video.get('uploader'),
                    video.get('uploader_id'),
                    video.get('channel'),
                    video.get('channel_id'),
                    video.get('view_count'),
                    video.get('like_count'),
                    video.get('comment_count'),
                    video.get('thumbnail'),
                    video.get('url'),
                    video.get('scraped_at')
                ))
                
                # Insert tags
                for tag in video.get('tags', []):
                    cursor.execute('INSERT INTO tags (video_id, tag) VALUES (?, ?)',
                                 (video.get('video_id'), tag))
                
                # Insert categories
                for category in video.get('categories', []):
                    cursor.execute('INSERT INTO categories (video_id, category) VALUES (?, ?)',
                                 (video.get('video_id'), category))
                
                # Insert subtitles
                for sub in video.get('subtitles', []):
                    cursor.execute('INSERT INTO subtitles (video_id, language, url, ext, subtitle_type) VALUES (?, ?, ?, ?, ?)',
                                 (video.get('video_id'), sub.get('language'), sub.get('url'), sub.get('ext'), 'manual'))
                
                # Insert automatic captions
                for cap in video.get('automatic_captions', []):
                    cursor.execute('INSERT INTO subtitles (video_id, language, url, ext, subtitle_type) VALUES (?, ?, ?, ?, ?)',
                                 (video.get('video_id'), cap.get('language'), cap.get('url'), cap.get('ext'), 'automatic'))
            
            conn.commit()
            conn.close()
            
            print(f"\nSQLite database saved to: {output_path}")
            print(f"Total videos: {len(data)}")
        
        except Exception as e:
            print(f"Error saving SQLite database: {e}")


def main():
    """Main entry point for the YouTube scraper CLI."""
    parser = argparse.ArgumentParser(
        description='YouTube Tutorial Data Scraper - Extract data from YouTube videos and generate AI database files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Scrape a single video
  python youtube_scraper.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --output tutorial_db.json
  
  # Scrape a playlist
  python youtube_scraper.py --url "https://www.youtube.com/playlist?list=PLAYLIST_ID" --output playlist_db.json
  
  # Scrape a channel (limit to 10 videos)
  python youtube_scraper.py --url "https://www.youtube.com/@channelname" --max-videos 10 --output channel_db.sqlite
  
  # Output to SQLite format
  python youtube_scraper.py --url "VIDEO_URL" --output db.sqlite --format sqlite
        '''
    )
    
    parser.add_argument('--url', '-u', required=True,
                       help='YouTube video, playlist, or channel URL')
    parser.add_argument('--output', '-o', default='youtube_ai_db.json',
                       help='Output database filename (default: youtube_ai_db.json)')
    parser.add_argument('--format', '-f', choices=['json', 'sqlite'], default='json',
                       help='Output format: json or sqlite (default: json)')
    parser.add_argument('--max-videos', '-m', type=int,
                       help='Maximum number of videos to scrape (for playlists/channels)')
    
    args = parser.parse_args()
    
    print("YouTube Tutorial Data Scraper")
    print("=" * 50)
    print(f"URL: {args.url}")
    print(f"Output: {args.output}")
    print(f"Format: {args.format}")
    print("=" * 50)
    print()
    
    scraper = YouTubeScraper()
    videos = []
    
    # Determine URL type and scrape accordingly
    if 'playlist' in args.url:
        print("Detected playlist URL")
        videos = scraper.extract_playlist_data(args.url)
    elif '@' in args.url or '/c/' in args.url or '/channel/' in args.url or '/user/' in args.url:
        print("Detected channel URL")
        videos = scraper.extract_channel_videos(args.url, args.max_videos)
    else:
        print("Detected single video URL")
        video_data = scraper.extract_video_data(args.url)
        if video_data:
            videos = [video_data]
    
    if not videos:
        print("\nNo videos were extracted. Please check the URL and try again.")
        return 1
    
    # Save to database
    db = AIDatabase()
    
    if args.format == 'sqlite':
        db.save_to_sqlite(videos, args.output)
    else:
        db.save_to_json(videos, args.output)
    
    print("\n✓ Scraping complete!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
