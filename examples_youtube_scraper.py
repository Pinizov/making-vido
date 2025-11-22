#!/usr/bin/env python3
"""
Example usage script for YouTube scraper
Demonstrates various use cases with sample URLs
"""

import subprocess
import sys


def run_command(description, command):
    """Run a command and display the result."""
    print(f"\n{'='*70}")
    print(f"Example: {description}")
    print(f"{'='*70}")
    print(f"Command: {' '.join(command)}")
    print(f"\nNote: This example requires internet connection to work.")
    print("In the sandboxed environment, it will fail to connect to YouTube.")
    print("On a real system with internet access, this would work.\n")
    
    # Uncomment the line below to actually run the command
    # subprocess.run(command)


def main():
    """Show various usage examples."""
    print("YouTube Scraper - Usage Examples")
    print("="*70)
    print("These examples demonstrate how to use the scraper in different scenarios.")
    print("Note: Actual execution requires internet connection and access to YouTube.")
    
    # Example 1: Single video
    run_command(
        "Scrape a single YouTube video to JSON",
        [
            "python", "youtube_scraper.py",
            "--url", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "--output", "single_video.json",
            "--format", "json"
        ]
    )
    
    # Example 2: Playlist
    run_command(
        "Scrape an entire playlist",
        [
            "python", "youtube_scraper.py",
            "--url", "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf",
            "--output", "playlist_videos.json"
        ]
    )
    
    # Example 3: Channel (limited)
    run_command(
        "Scrape first 10 videos from a channel",
        [
            "python", "youtube_scraper.py",
            "--url", "https://www.youtube.com/@YourChannelName",
            "--max-videos", "10",
            "--output", "channel_videos.json"
        ]
    )
    
    # Example 4: SQLite output
    run_command(
        "Scrape to SQLite database format",
        [
            "python", "youtube_scraper.py",
            "--url", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "--output", "video_database.sqlite",
            "--format", "sqlite"
        ]
    )
    
    # Example 5: Tutorial playlist
    run_command(
        "Scrape AI/ML tutorial playlist",
        [
            "python", "youtube_scraper.py",
            "--url", "https://www.youtube.com/playlist?list=PLeo1K3hjS3uu7CxAacxVndI4bE_o3BDtO",
            "--output", "ai_tutorials.json"
        ]
    )
    
    print("\n" + "="*70)
    print("Usage Pattern:")
    print("="*70)
    print("\n  python youtube_scraper.py --url <URL> --output <FILE> [OPTIONS]\n")
    print("Options:")
    print("  --url, -u       : YouTube video, playlist, or channel URL (required)")
    print("  --output, -o    : Output filename (default: youtube_ai_db.json)")
    print("  --format, -f    : Output format - json or sqlite (default: json)")
    print("  --max-videos, -m: Limit number of videos (for playlists/channels)")
    print("\nFor more details, run: python youtube_scraper.py --help")
    print("="*70)
    
    # Show how to query the generated database
    print("\n" + "="*70)
    print("Using the Generated Database:")
    print("="*70)
    print("\n1. JSON Format:")
    print("   import json")
    print("   with open('output.json', 'r') as f:")
    print("       data = json.load(f)")
    print("       for video in data['videos']:")
    print("           print(f\"{video['title']} - {video['view_count']} views\")")
    
    print("\n2. SQLite Format:")
    print("   import sqlite3")
    print("   conn = sqlite3.connect('output.sqlite')")
    print("   cursor = conn.cursor()")
    print("   cursor.execute('SELECT title, view_count FROM videos ORDER BY view_count DESC')")
    print("   for row in cursor.fetchall():")
    print("       print(f\"{row[0]} - {row[1]} views\")")
    print("   conn.close()")
    print("="*70)


if __name__ == '__main__':
    main()
