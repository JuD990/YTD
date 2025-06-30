# 🎥 YTD - YouTube Downloader (Video & Audio)

**YTD** is a user-friendly desktop application built with Python and PyQt5 that enables easy downloading of YouTube videos and audio. Leveraging the powerful yt-dlp library, it supports multiple video resolutions (720p, 1080p, 2160p) and high-quality MP3 audio extraction. Users can input multiple YouTube links, choose download folders, and monitor real-time progress within a sleek, dark-themed interface. The app also allows setting a default download directory for convenience and handles video-audio merging via ffmpeg. It is designed to simplify media downloading while providing clear feedback and a smooth user experience.

---

## 🚀 Features

- ✅ Download YouTube **videos** in 720p, 1080p, or 2160p(4k).
- ✅ Extract and download **audio** in high-quality MP3 format.
- ✅ Select and save a **default download folder**.
- ✅ Progress tracking and live download logs.
- ✅ Modern dark-themed **PyQt5 interface**.
- ✅ Multi-link support: paste multiple YouTube URLs at once.

---

## 🛠 Requirements

- Python 3.8+
- PyQt5
- yt-dlp
- ffmpeg (required for video merging and audio conversion)

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/JuD990/YTD.git
cd YTD
```
### 2. Operating System
#### 2.1 Using Linux:
```bash
./dist/YTD
```
#### 2.2 Using Windows:
  ##### 2.2.1 Using CMD:
  ```bash
  buildenv\Scripts\activate
  ```
  ##### 2.2.2 Using PowerShell:
  ```bash
  .\buildenv\Scripts\Activate.ps1
  ```
#### 2.3 Using macOS:
```bash
source buildenv/bin/activate
```

### 3. Install Dependencies
Create a requirements.txt file with the following contents:
```bash
PyQt5
yt-dlp
```

Then install:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python3 YTD.py
```

📦 Build Executable (Optional)
To create a Windows executable using PyInstaller:
```bash
pyinstaller --noconfirm --onefile --windowed --add-data "<path_to_platforms>:platforms" YTD.py
```

Replace <path_to_platforms> with the actual path to the PyQt5 platforms directory, e.g.:
```bash
./buildenv/lib/python3.12/site-packages/PyQt5/Qt5/plugins/platforms
```

📁 Folder Structure
```bash
YTD/
├── YTD.py                  # Main application file
├── downloads/              # Default folder for downloaded content
├── dist/                   # Output directory for built executable
├── buildenv/               # Virtual environment (excluded from Git)
├── .gitignore
└── README.md
```

## 📃 License
MIT License - Use freely for personal or educational purposes.

🙋‍♂️ Author
Jude Adolfo
```bash
https://github.com/JuD990
```
