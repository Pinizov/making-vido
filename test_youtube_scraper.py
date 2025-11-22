#!/usr/bin/env python3
"""
Test script for YouTube scraper - demonstrates functionality without internet
"""

import json
import os
import sys
from datetime import datetime

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from youtube_scraper import AIDatabase


def test_json_output():
    """Test JSON database generation with sample data."""
    print("Testing JSON output generation...")
    
    # Sample scraped data
    sample_data = [
        {
            'video_id': 'dQw4w9WgXcQ',
            'title': 'ComfyUI Tutorial: Getting Started with AI Video Generation',
            'description': 'Learn how to use ComfyUI for creating AI-generated videos. This tutorial covers setup, workflow creation, and best practices.',
            'duration': 1200,
            'upload_date': '20240115',
            'uploader': 'AI Video Channel',
            'uploader_id': 'UCxxxxx',
            'channel': 'AI Video Channel',
            'channel_id': 'UCxxxxx',
            'view_count': 50000,
            'like_count': 2500,
            'comment_count': 300,
            'categories': ['Education', 'Science & Technology'],
            'tags': ['comfyui', 'ai video', 'tutorial', 'machine learning', 'stable diffusion'],
            'thumbnail': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
            'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'scraped_at': datetime.now().isoformat(),
            'subtitles': [
                {'language': 'en', 'url': 'https://example.com/sub.en.vtt', 'ext': 'vtt'}
            ],
            'automatic_captions': [
                {'language': 'en', 'url': 'https://example.com/cap.en.srv3', 'ext': 'srv3'}
            ]
        },
        {
            'video_id': 'abc123XYZ',
            'title': 'Advanced AI Filmmaking Techniques',
            'description': 'Deep dive into advanced techniques for AI-powered filmmaking using ComfyUI and various AI models.',
            'duration': 1800,
            'upload_date': '20240201',
            'uploader': 'AI Video Channel',
            'uploader_id': 'UCxxxxx',
            'channel': 'AI Video Channel',
            'channel_id': 'UCxxxxx',
            'view_count': 75000,
            'like_count': 3800,
            'comment_count': 450,
            'categories': ['Education'],
            'tags': ['ai', 'filmmaking', 'video generation', 'comfyui', 'workflows'],
            'thumbnail': 'https://i.ytimg.com/vi/abc123XYZ/maxresdefault.jpg',
            'url': 'https://www.youtube.com/watch?v=abc123XYZ',
            'scraped_at': datetime.now().isoformat(),
            'subtitles': [],
            'automatic_captions': [
                {'language': 'en', 'url': 'https://example.com/cap2.en.srv3', 'ext': 'srv3'}
            ]
        },
        {
            'video_id': 'xyz789ABC',
            'title': 'Creating Character Consistency in AI Videos',
            'description': 'Tutorial on maintaining character consistency across AI-generated video frames using LoRA models.',
            'duration': 900,
            'upload_date': '20240210',
            'uploader': 'AI Video Channel',
            'uploader_id': 'UCxxxxx',
            'channel': 'AI Video Channel',
            'channel_id': 'UCxxxxx',
            'view_count': 60000,
            'like_count': 3000,
            'comment_count': 250,
            'categories': ['Education', 'Howto & Style'],
            'tags': ['character consistency', 'ai video', 'lora', 'stable diffusion', 'tutorial'],
            'thumbnail': 'https://i.ytimg.com/vi/xyz789ABC/maxresdefault.jpg',
            'url': 'https://www.youtube.com/watch?v=xyz789ABC',
            'scraped_at': datetime.now().isoformat(),
            'subtitles': [
                {'language': 'en', 'url': 'https://example.com/sub3.en.vtt', 'ext': 'vtt'}
            ],
            'automatic_captions': []
        }
    ]
    
    # Test JSON output
    db = AIDatabase()
    output_file = '/tmp/test_youtube_ai_db.json'
    db.save_to_json(sample_data, output_file)
    
    # Verify the output
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            loaded_data = json.load(f)
        
        print(f"\n✓ JSON file created successfully!")
        print(f"  Total videos: {loaded_data['metadata']['total_videos']}")
        print(f"  File size: {os.path.getsize(output_file)} bytes")
        print(f"  Location: {output_file}")
        
        # Display sample content
        print("\nSample video data:")
        for i, video in enumerate(loaded_data['videos'][:2], 1):
            print(f"\n  Video {i}:")
            print(f"    Title: {video['title']}")
            print(f"    Duration: {video['duration']}s")
            print(f"    Views: {video['view_count']:,}")
            print(f"    Tags: {', '.join(video['tags'][:3])}...")
        
        return True
    else:
        print("✗ Failed to create JSON file")
        return False


def test_sqlite_output():
    """Test SQLite database generation with sample data."""
    print("\n" + "="*60)
    print("Testing SQLite output generation...")
    
    # Sample scraped data
    sample_data = [
        {
            'video_id': 'test001',
            'title': 'AI Video Tutorial Part 1',
            'description': 'Introduction to AI video generation',
            'duration': 600,
            'upload_date': '20240101',
            'uploader': 'Tutorial Channel',
            'uploader_id': 'UC12345',
            'channel': 'Tutorial Channel',
            'channel_id': 'UC12345',
            'view_count': 10000,
            'like_count': 500,
            'comment_count': 50,
            'categories': ['Education'],
            'tags': ['ai', 'video', 'tutorial'],
            'thumbnail': 'https://example.com/thumb1.jpg',
            'url': 'https://www.youtube.com/watch?v=test001',
            'scraped_at': datetime.now().isoformat(),
            'subtitles': [
                {'language': 'en', 'url': 'https://example.com/sub1.vtt', 'ext': 'vtt'}
            ],
            'automatic_captions': []
        },
        {
            'video_id': 'test002',
            'title': 'AI Video Tutorial Part 2',
            'description': 'Advanced techniques for AI video',
            'duration': 720,
            'upload_date': '20240105',
            'uploader': 'Tutorial Channel',
            'uploader_id': 'UC12345',
            'channel': 'Tutorial Channel',
            'channel_id': 'UC12345',
            'view_count': 8000,
            'like_count': 400,
            'comment_count': 40,
            'categories': ['Education'],
            'tags': ['ai', 'advanced', 'video'],
            'thumbnail': 'https://example.com/thumb2.jpg',
            'url': 'https://www.youtube.com/watch?v=test002',
            'scraped_at': datetime.now().isoformat(),
            'subtitles': [],
            'automatic_captions': [
                {'language': 'en', 'url': 'https://example.com/cap2.srv3', 'ext': 'srv3'}
            ]
        }
    ]
    
    # Test SQLite output
    db = AIDatabase()
    output_file = '/tmp/test_youtube_ai_db.sqlite'
    db.save_to_sqlite(sample_data, output_file)
    
    # Verify the output
    if os.path.exists(output_file):
        import sqlite3
        
        conn = sqlite3.connect(output_file)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        # Check video count
        cursor.execute("SELECT COUNT(*) FROM videos")
        video_count = cursor.fetchone()[0]
        
        # Check tag count
        cursor.execute("SELECT COUNT(*) FROM tags")
        tag_count = cursor.fetchone()[0]
        
        # Sample query
        cursor.execute("SELECT title, view_count FROM videos ORDER BY view_count DESC LIMIT 1")
        top_video = cursor.fetchone()
        
        conn.close()
        
        print(f"\n✓ SQLite database created successfully!")
        print(f"  Tables: {', '.join([t[0] for t in tables])}")
        print(f"  Total videos: {video_count}")
        print(f"  Total tags: {tag_count}")
        print(f"  File size: {os.path.getsize(output_file)} bytes")
        print(f"  Location: {output_file}")
        print(f"\n  Most viewed video: '{top_video[0]}' ({top_video[1]:,} views)")
        
        return True
    else:
        print("✗ Failed to create SQLite database")
        return False


def main():
    """Run all tests."""
    print("YouTube Scraper Test Suite")
    print("="*60)
    
    success = True
    
    # Test JSON output
    if not test_json_output():
        success = False
    
    # Test SQLite output
    if not test_sqlite_output():
        success = False
    
    print("\n" + "="*60)
    if success:
        print("✓ All tests passed!")
        print("\nThe scraper is ready to use. Example usage:")
        print("  python youtube_scraper.py --url 'VIDEO_URL' --output db.json")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
