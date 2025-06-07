# 🎥 YTD - YouTube Downloader (Video & Audio)

**YTD** is a user-friendly desktop application built with Python and PyQt5 that enables easy downloading of YouTube videos and audio. Leveraging the powerful yt-dlp library, it supports multiple video resolutions (720p, 1080p, 2160p) and high-quality MP3 audio extraction. Users can input multiple YouTube links, choose download folders, and monitor real-time progress within a sleek, dark-themed interface. The app also allows setting a default download directory for convenience and handles video-audio merging via ffmpeg. It is designed to simplify media downloading while providing clear feedback and a smooth user experience.

---

## 🚀 Features

- ✅ Download YouTube **videos** in 720p, 1080p, or 2160p.
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
git clone https://github.com/yourusername/YTD.git
cd YTD

2. Create and Activate Virtual Environment (Optional but Recommended)

python -m venv buildenv
source buildenv/bin/activate  # On Windows use: buildenv\Scripts\activate

3. Install Dependencies
Create a requirements.txt file with the following contents:
PyQt5
yt-dlp

Then install:
pip install -r requirements.txt

🖥️ Run the Application
python3 YTD.py

📦 Build Executable (Optional)
To create a Windows executable using PyInstaller:
pyinstaller --noconfirm --onefile --windowed --add-data "<path_to_platforms>:platforms" YTD.py

Replace <path_to_platforms> with the actual path to the PyQt5 platforms directory, e.g.:
./buildenv/lib/python3.12/site-packages/PyQt5/Qt5/plugins/platforms

📁 Folder Structure
YTD/
├── YTD.py                  # Main application file
├── downloads/              # Default folder for downloaded content
├── dist/                   # Output directory for built executable
├── buildenv/               # Virtual environment (excluded from Git)
├── .gitignore
└── README.md

📃 License
MIT License - Use freely for personal or educational purposes.

🙋‍♂️ Author
Jude Adolfo
https://github.com/JuD990
