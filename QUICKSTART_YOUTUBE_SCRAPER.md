# Quick Start Guide: YouTube Scraper

## 🚀 How to Start and Test

### Step 1: Install Dependencies

Install the required library:
```bash
pip install yt-dlp
```

Or install all project dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Run the Test Suite (No Internet Required)

Test the scraper functionality with sample data:
```bash
python test_youtube_scraper.py
```

Expected output:
```
YouTube Scraper Test Suite
============================================================
Testing JSON output generation...
✓ JSON file created successfully!
  Total videos: 3
  
Testing SQLite output generation...
✓ SQLite database created successfully!
  Tables: videos, tags, categories, subtitles
  Total videos: 2
  
✓ All tests passed!
```

### Step 3: View Usage Examples

See various usage patterns:
```bash
python examples_youtube_scraper.py
```

### Step 4: Test with Real YouTube Data (Requires Internet)

#### Single Video Example:
```bash
python youtube_scraper.py \
  --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --output my_video.json
```

#### Playlist Example:
```bash
python youtube_scraper.py \
  --url "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf" \
  --output my_playlist.json
```

#### Channel Example (Limited):
```bash
python youtube_scraper.py \
  --url "https://www.youtube.com/@channelname" \
  --max-videos 5 \
  --output channel_data.json
```

#### SQLite Database Output:
```bash
python youtube_scraper.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --output videos.sqlite \
  --format sqlite
```

### Step 5: View Generated Data

#### For JSON files:
```bash
# View in terminal
cat my_video.json | head -50

# Or open in Python
python -c "import json; data = json.load(open('my_video.json')); print(data['videos'][0]['title'])"
```

#### For SQLite databases:
```bash
# View tables
sqlite3 videos.sqlite ".tables"

# Query data
sqlite3 videos.sqlite "SELECT title, view_count FROM videos;"
```

## 📖 Get Help

View all available options:
```bash
python youtube_scraper.py --help
```

## 🔧 Troubleshooting

### Error: "yt-dlp is not installed"
Solution:
```bash
pip install yt-dlp
```

### Error: "No videos were extracted"
- Check that the URL is correct and publicly accessible
- Verify your internet connection
- Try a different video/playlist URL

### Slow Performance
- Use `--max-videos` to limit the number of videos scraped
- Example: `--max-videos 10`

## 📚 Full Documentation

For complete documentation, see: [YOUTUBE_SCRAPER_README.md](YOUTUBE_SCRAPER_README.md)
