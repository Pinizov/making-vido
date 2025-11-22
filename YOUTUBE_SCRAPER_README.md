# YouTube Tutorial Data Scraper

A Python-based data scraper that extracts data from YouTube tutorials and generates AI database files in JSON or SQLite format.

## Features

- **Single Video Scraping**: Extract data from individual YouTube videos
- **Playlist Scraping**: Scrape all videos from a YouTube playlist
- **Channel Scraping**: Extract videos from entire YouTube channels
- **Flexible Output**: Save data in JSON or SQLite database format
- **Comprehensive Data**: Extracts video metadata, descriptions, tags, categories, subtitles, and more
- **Auto-Captions**: Captures automatic captions when available

## Installation

1. Install the required dependency:
```bash
pip install yt-dlp>=2024.12.6
```

Or install all project dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Scrape a single YouTube video:
```bash
python youtube_scraper.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --output tutorial_db.json
```

### Scraping Playlists

Extract all videos from a playlist:
```bash
python youtube_scraper.py --url "https://www.youtube.com/playlist?list=PLAYLIST_ID" --output playlist_db.json
```

### Scraping Channels

Extract videos from a channel (with optional limit):
```bash
python youtube_scraper.py --url "https://www.youtube.com/@channelname" --max-videos 10 --output channel_db.json
```

### SQLite Output

Generate a SQLite database instead of JSON:
```bash
python youtube_scraper.py --url "VIDEO_URL" --output db.sqlite --format sqlite
```

## Command Line Options

- `--url`, `-u`: (Required) YouTube video, playlist, or channel URL
- `--output`, `-o`: Output database filename (default: `youtube_ai_db.json`)
- `--format`, `-f`: Output format - `json` or `sqlite` (default: `json`)
- `--max-videos`, `-m`: Maximum number of videos to scrape (for playlists/channels)

## Output Formats

### JSON Format

The JSON output includes:
- **Metadata**: Generation timestamp, total videos, version
- **Videos**: Array of video objects with the following fields:
  - `video_id`: Unique YouTube video ID
  - `title`: Video title
  - `description`: Full video description
  - `duration`: Video duration in seconds
  - `upload_date`: Date the video was uploaded
  - `uploader`: Uploader name
  - `channel`: Channel name
  - `channel_id`: Channel ID
  - `view_count`: Number of views
  - `like_count`: Number of likes
  - `comment_count`: Number of comments
  - `categories`: List of video categories
  - `tags`: List of video tags
  - `thumbnail`: URL to video thumbnail
  - `url`: Original video URL
  - `subtitles`: Available manual subtitles
  - `automatic_captions`: Available auto-generated captions
  - `scraped_at`: Timestamp when the data was scraped

Example JSON structure:
```json
{
  "metadata": {
    "generated_at": "2024-11-22T21:15:00.000000",
    "total_videos": 5,
    "version": "1.0"
  },
  "videos": [
    {
      "video_id": "dQw4w9WgXcQ",
      "title": "Example Tutorial Video",
      "description": "This is a tutorial about...",
      "duration": 300,
      "upload_date": "20240101",
      "uploader": "Channel Name",
      "channel": "Channel Name",
      "view_count": 1000000,
      "like_count": 50000,
      "tags": ["tutorial", "python", "ai"],
      "categories": ["Education"],
      ...
    }
  ]
}
```

### SQLite Format

The SQLite database includes four tables:

1. **videos**: Main video information
2. **tags**: Video tags (one row per tag)
3. **categories**: Video categories (one row per category)
4. **subtitles**: Available subtitles and captions (manual and automatic)

## Use Cases for AI Applications

The scraped data can be used for various AI and machine learning applications:

1. **Training Data**: Use video titles, descriptions, and tags as training data for NLP models
2. **Content Analysis**: Analyze trends, topics, and patterns in tutorial content
3. **Recommendation Systems**: Build recommendation engines based on video metadata
4. **Search Enhancement**: Create enhanced search functionality using comprehensive metadata
5. **Caption Analysis**: Process subtitles and captions for content understanding
6. **Content Generation**: Use as source data for AI-powered video content generation

## Example Workflow

```bash
# 1. Scrape a tutorial playlist
python youtube_scraper.py \
  --url "https://www.youtube.com/playlist?list=PLxxx" \
  --output ai_tutorials.json \
  --format json

# 2. Use the generated database in your AI application
# The JSON file can be loaded and processed by your AI pipeline
```

## Notes

- The scraper respects YouTube's terms of service and only extracts publicly available metadata
- No video files are downloaded; only metadata is extracted
- Large channels or playlists may take time to scrape; use `--max-videos` to limit results
- Requires internet connection to access YouTube data
- Some videos may have restricted access or missing metadata

## Troubleshooting

### yt-dlp Not Installed
If you see the error "yt-dlp is not installed", run:
```bash
pip install yt-dlp
```

### No Videos Extracted
- Verify the URL is correct and publicly accessible
- Check your internet connection
- Some videos may be private or restricted

### Slow Performance
- Use `--max-videos` to limit the number of videos scraped
- Consider scraping in smaller batches for large channels

## License

This tool is part of the making-vido project. See the main LICENSE file for details.
