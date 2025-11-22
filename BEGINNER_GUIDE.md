# YouTube Scraper - Complete Beginner's Guide for Windows

## 📋 What You Need Before Starting

- A Windows computer (Windows 10 or 11 recommended)
- Python 3.7 or higher installed
- Internet connection (for scraping YouTube data)
- PowerShell or Command Prompt

---

## 🖥️ Step-by-Step Instructions for Windows Users

### Part 1: Check if Python is Installed

Open **PowerShell** (search for "PowerShell" in Windows Start menu) and type:

```powershell
python --version
```

**Expected output:** `Python 3.x.x` (where x is any number)

**If you don't have Python:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python for Windows
3. Run the installer
4. ⚠️ **IMPORTANT:** Check the box "Add Python to PATH" during installation
5. Restart PowerShell after installation

---

### Part 2: Download the Code

#### Option A: Using Git (if you have Git installed)
Open **PowerShell** and run:
```powershell
# Clone the repository
git clone https://github.com/Pinizov/making-vido.git

# Go into the folder
cd making-vido
```

#### Option B: Download ZIP (Easier for Beginners)
1. Go to https://github.com/Pinizov/making-vido
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Extract the ZIP file to a folder (e.g., `C:\Users\YourName\making-vido`)
5. Open **PowerShell**
6. Navigate to the folder:
   ```powershell
   cd C:\Users\YourName\making-vido
   ```
   (Replace `YourName` with your actual Windows username)

---

### Part 3: Install Required Software

In **PowerShell** (make sure you're in the `making-vido` folder):

```powershell
# Install the YouTube scraper library
pip install yt-dlp
```

**Alternative:** Install all project dependencies:
```powershell
pip install -r requirements.txt
```

**What you'll see:**
```
Collecting yt-dlp
  Downloading yt-dlp-2024.12.6...
Installing collected packages: yt-dlp
Successfully installed yt-dlp-2024.12.6
```

**Wait for installation to complete** - you'll see "Successfully installed..." when done

**If you get an error:** Try running PowerShell as Administrator (right-click PowerShell → "Run as administrator")

---

### Part 4: Test the Scraper (No Internet Needed)

This tests if everything works without needing to connect to YouTube.

In **PowerShell**:
```powershell
python test_youtube_scraper.py
```

**What you should see:**
```
YouTube Scraper Test Suite
============================================================
Testing JSON output generation...
✓ JSON file created successfully!
  Total videos: 3
  File size: 3530 bytes
  
Testing SQLite output generation...
✓ SQLite database created successfully!
  Tables: videos, tags, categories, subtitles
  Total videos: 2
  
✓ All tests passed!
```

**If you see "✓ All tests passed!" - Congratulations! Everything works!** 🎉

---

### Part 5: Use the Scraper with Real YouTube Videos

Now let's scrape actual YouTube data! Open **PowerShell** and make sure you're in the `making-vido` folder.

#### Example 1: Scrape a Single Video

```powershell
python youtube_scraper.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --output my_first_video.json
```

**What happens:** 
- The scraper downloads video information (NOT the video file itself)
- Creates a file called `my_first_video.json` in the current folder
- You can open this file with **Notepad** to see the data

**What you'll see:**
```
YouTube Tutorial Data Scraper
==================================================
URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Output: my_first_video.json
Format: json
==================================================

Detected single video URL

JSON database saved to: C:\Users\...\my_first_video.json
Total videos: 1

✓ Scraping complete!
```

---

#### Example 2: Scrape a YouTube Playlist

```powershell
python youtube_scraper.py --url "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf" --output my_playlist.json
```

**What happens:**
- Scrapes ALL videos in the playlist
- This may take a few minutes depending on playlist size
- Shows progress as each video is extracted
- Creates a JSON file with data from all videos

---

#### Example 3: Scrape a Channel (Limited to 5 Videos)

```powershell
python youtube_scraper.py --url "https://www.youtube.com/@TechWithTim" --max-videos 5 --output channel_videos.json
```

**What happens:**
- Scrapes only the first 5 videos from the channel
- Use `--max-videos` to control how many videos to scrape
- Good for testing before scraping entire channels

---

#### Example 4: Save to SQLite Database Instead of JSON

```powershell
python youtube_scraper.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --output my_database.sqlite --format sqlite
```

**What's the difference?**
- **JSON format:** Easy to read in Notepad, good for simple use
- **SQLite format:** Database format, can be queried with SQL, good for data analysis

---

### Part 6: View Your Scraped Data

#### To View JSON Files:

**Open in Notepad:**
```powershell
notepad my_first_video.json
```

**Or view in PowerShell:**
```powershell
# View first 30 lines
Get-Content my_first_video.json | Select-Object -First 30

# View the entire file
Get-Content my_first_video.json
```

**Or open with Windows File Explorer:**
1. Press `Windows Key + E` to open File Explorer
2. Navigate to your `making-vido` folder
3. Double-click `my_first_video.json`
4. Choose Notepad or your favorite text editor

#### To View SQLite Database:

**Option 1: Download DB Browser (Recommended for Beginners)**
1. Download from: https://sqlitebrowser.org/dl/
2. Install DB Browser for SQLite
3. Open the program
4. Click "Open Database"
5. Select your `.sqlite` file
6. Click "Browse Data" tab to view tables

**Option 2: Using SQLite Command Line**
```powershell
# Download sqlite3 tools from sqlite.org if not installed
# Then run:
sqlite3 my_database.sqlite

# Inside sqlite3, run these commands:
.tables                                 # Show all tables
SELECT * FROM videos;                   # View all video data
SELECT title, view_count FROM videos;  # View specific columns
.quit                                   # Exit sqlite3
```

---

### Part 7: Understanding the Output Files

#### JSON File Structure:
```json
{
  "metadata": {
    "generated_at": "2024-11-22T...",
    "total_videos": 3
  },
  "videos": [
    {
      "video_id": "abc123",
      "title": "Video Title",
      "description": "Video description...",
      "duration": 300,
      "view_count": 10000,
      "like_count": 500,
      "tags": ["tag1", "tag2"],
      ...
    }
  ]
}
```

#### SQLite Database Tables:
- **videos** - Main video information (title, views, duration, etc.)
- **tags** - All video tags
- **categories** - Video categories
- **subtitles** - Available subtitles and captions

---

### Part 8: Common Commands Reference for Windows

#### Get Help:
```powershell
python youtube_scraper.py --help
```

#### Basic Single Video:
```powershell
python youtube_scraper.py --url "YOUTUBE_URL" --output filename.json
```

#### With All Options (One Line):
```powershell
python youtube_scraper.py --url "YOUTUBE_URL" --output filename.json --format json --max-videos 10
```

**Options Explained:**
- `--url` or `-u`: The YouTube video/playlist/channel URL (REQUIRED)
- `--output` or `-o`: Name of the file to save data to (default: youtube_ai_db.json)
- `--format` or `-f`: Choose `json` or `sqlite` (default: json)
- `--max-videos` or `-m`: Maximum number of videos to scrape (optional, for playlists/channels)

---

## 🆘 Troubleshooting for Windows Users

### Problem: "python is not recognized as an internal or external command"

**Solution:**
1. Python is not installed or not in PATH
2. Reinstall Python from python.org
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Restart PowerShell after installation
5. If still not working, search for "Environment Variables" in Windows and add Python to PATH manually

### Problem: "yt-dlp is not installed"

**Solution:**
```powershell
pip install yt-dlp
```

If that doesn't work, try:
```powershell
python -m pip install yt-dlp
```

### Problem: "No videos were extracted"

**Possible reasons:**
1. **Wrong URL** - Make sure you copied the full YouTube URL (right-click video → Copy URL)
2. **Private video** - The video must be publicly accessible
3. **No internet connection** - Check your internet connection
4. **Video doesn't exist** - Try a different URL
5. **Age-restricted** - Some videos can't be scraped

### Problem: "Access is denied" or "Permission Error"

**Solution:**
1. Run PowerShell as Administrator:
   - Search for "PowerShell" in Start menu
   - Right-click → "Run as administrator"
2. Or save files to a folder where you have permissions (like Documents)

### Problem: Script is very slow or takes forever

**Solution:**
```powershell
# Limit the number of videos when scraping playlists/channels
python youtube_scraper.py --url "URL" --max-videos 5 --output data.json
```

### Problem: "SSL Certificate Error"

**Solution:**
```powershell
# Update pip and yt-dlp
python -m pip install --upgrade pip
pip install --upgrade yt-dlp
```

---

## 💡 Tips for Windows Beginners

1. **Start Small:** Try scraping just one video first before attempting playlists
2. **Check the Output:** Open the JSON file in Notepad to see what data was extracted
3. **Use max-videos:** When testing, use `--max-videos 5` to limit results and save time
4. **Save Your Commands:** Create a `.txt` file with commands you use often - you can copy/paste from it
5. **Read Error Messages:** They usually tell you exactly what's wrong
6. **Use Tab Completion:** In PowerShell, type part of a filename and press TAB to auto-complete
7. **Keep PowerShell Open:** You don't need to close and reopen it between commands

---

## 📂 Where Are the Output Files Saved?

The output files are saved in the **same folder** where you run the command (the `making-vido` folder).

**To find them in PowerShell:**

```powershell
# Show current directory path
pwd

# List all files
dir

# List only JSON files
dir *.json

# List only SQLite files
dir *.sqlite
```

**To find them in Windows:**
1. Open File Explorer (`Windows Key + E`)
2. Navigate to your `making-vido` folder
3. Look for files with names like `my_first_video.json` or `my_database.sqlite`

**Quick Tip:** In PowerShell, type `explorer .` to open the current folder in File Explorer:
```powershell
explorer .
```

---

## 🎯 Quick Reference: What Command Should I Use on Windows?

| What I Want to Do | PowerShell Command |
|-------------------|-------------------|
| **Test if it works** | `python test_youtube_scraper.py` |
| **Scrape one video** | `python youtube_scraper.py --url "VIDEO_URL" --output video.json` |
| **Scrape a playlist** | `python youtube_scraper.py --url "PLAYLIST_URL" --output playlist.json` |
| **Scrape channel (5 videos)** | `python youtube_scraper.py --url "CHANNEL_URL" --max-videos 5 --output channel.json` |
| **Save as SQLite database** | `python youtube_scraper.py --url "VIDEO_URL" --output data.sqlite --format sqlite` |
| **Limit number of videos** | Add `--max-videos 10` to any command |
| **Get help** | `python youtube_scraper.py --help` |
| **See example commands** | `python examples_youtube_scraper.py` |
| **Open current folder** | `explorer .` |
| **List output files** | `dir *.json` or `dir *.sqlite` |

---

## 📚 Next Steps After Mastering the Basics

After you're comfortable with the basic commands:

1. **Read the detailed docs:** [YOUTUBE_SCRAPER_README.md](YOUTUBE_SCRAPER_README.md)
2. **See more examples:** Run `python examples_youtube_scraper.py`
3. **Try different sources:** Scrape various YouTube channels and playlists
4. **Learn to analyze data:** Open the JSON/SQLite files and explore the data
5. **Use in your projects:** Import the data into Excel, Python scripts, or other tools

---

## 🎓 Copy-Paste Ready Commands for Windows

Here are complete, ready-to-use commands. Just copy and paste into PowerShell:

**Install and Test:**
```powershell
# Install
pip install yt-dlp

# Test
python test_youtube_scraper.py
```

**Quick Examples (Replace VIDEO_URL with actual URL):**
```powershell
# Single video to JSON
python youtube_scraper.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --output my_video.json

# Playlist (first 10 videos)
python youtube_scraper.py --url "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID" --max-videos 10 --output playlist.json

# Channel (first 5 videos) to SQLite
python youtube_scraper.py --url "https://www.youtube.com/@channelname" --max-videos 5 --output channel.sqlite --format sqlite

# Open output folder in File Explorer
explorer .
```

---

## ❓ Still Need Help?

If you're stuck after reading this guide:

1. **Read the error message carefully** - it often tells you exactly what's wrong
2. **Check the troubleshooting section** above for your specific error
3. **Make sure you followed all steps in order** - don't skip steps!
4. **Try the test command first** - `python test_youtube_scraper.py` should work without internet
5. **Ask for help:** Create an issue on GitHub with:
   - What command you ran
   - What error you got
   - What step you're on

**Remember:** Everyone was a beginner once! Take it one step at a time, and don't be afraid to ask questions. 🚀

---

## ✅ Quick Checklist Before Asking for Help

Before asking for help, verify:

- [ ] Python is installed (`python --version` works)
- [ ] yt-dlp is installed (`pip list | findstr yt-dlp` shows it)
- [ ] You're in the correct folder (`dir` shows `youtube_scraper.py`)
- [ ] Test script passes (`python test_youtube_scraper.py` shows ✓)
- [ ] You have internet connection (for real YouTube scraping)
- [ ] You copied the FULL YouTube URL
- [ ] You read the error message completely

If all checked and still having issues, then it's time to ask for help!
