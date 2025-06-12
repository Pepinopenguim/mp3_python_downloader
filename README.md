# MP3 Python Downloader

A simple Python script using `pytube`/`pytubefix` to download songs from YouTube by searching their names.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyTube](https://img.shields.io/badge/PyTube-Fork-lightgrey)

## Features

- 🎵 Downloads MP3s from YouTube using search queries
- 📝 Supports custom file naming (with/without artist names)
- 📁 Organizes downloads into designated folders
- 💡 Ignores comments (lines starting with `#`) in song lists
- ⚙️ Configurable through simple JSON settings

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mp3_python_downloader.git
   cd mp3_python_downloader
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate environment**
   - Windows:
     ```cmd
     call venv\Scripts\activate
     ```
   - Linux/MacOS:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### songs.txt
Create a text file with your song list. Example:
```plaintext
# Format: Artist - Song Name (recommended for best results)
# Lines starting with # are ignored

Kevin MacLeod - Monkeys Spinning Monkeys
The Green Orbs - A Little Trip
Jingle Punks - Back to the 80s
```

### config.json
Modify the configuration file:
```json
{
    "custom download path": null,
    "folder name": "My Music",
    "songs text file": "songs.txt",
    "song name only": false,
    "index names": true,
    "index digits": 3
}
```

| Setting | Description | Values |
|---------|-------------|--------|
| `custom download path` | Absolute path for downloads | `null` for script directory |
| `folder name` | Subfolder for downloads | Any valid folder name, `null` for script folder name |
| `songs text file` | Name of song list file | `.txt` filename |
| `song name only` | Include artist name in saved song | `true` for "Song.mp3", `false` for "Artist - Song.mp3" |
| `index names` | Add numbering prefix | `true`/`false` |
| `index digits` | Number of digits in index | e.g. `3` → "001_Song.mp3" |

## Usage

```bash
python main.py
```

The script will:
1. Read your song list from `songs.txt`
2. Search YouTube for each track
3. Download the best audio match
4. Save files in your specified folder


## Legal warning

Although possible you should definitely not use it for piracy haha
wink wink nudge nudge blinks at you subtly
Not that I would know

## License

MIT License - See [LICENSE](LICENSE) for details.

## to do
- edit tags to include artist name and album name
- add compatibility with other file types, not only mp3
- import song list directly from spotify link
