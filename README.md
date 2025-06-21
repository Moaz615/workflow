# Moaz-Video-Downloader-V.1.0
A universal, multi-language, GUI-based video downloader for Windows, powered by Python, yt-dlp, and ffmpeg.

## Features
- Download videos and playlists from hundreds of sites
- Batch downloads with parallelism
- Audio-only (MP3) and custom format support
- Multi-language GUI (English, Arabic, French, etc.)
- Drag-and-drop URLs or batch files
- Download history, recent URLs, and settings persistence
- Modern light/dark themes
- Built-in ffmpeg integration (auto-download or bundled)
- Auto-update for yt-dlp

## Installation

1.  **Download the Installer**: Go to the [latest release](<YOUR_RELEASE_LINK_HERE>) and download the `MoazVideoDownloaderSetup.exe` file.
2.  **Run the Installer**: Double-click the downloaded `.exe` file and follow the on-screen instructions. The installer will handle everything, including placing `ffmpeg.exe` where it needs to be.
3.  **Launch the App**: Once installed, you can launch Moaz Video Downloader from the Start Menu or the desktop shortcut.

That's it! You are ready to start downloading.

## For Developers

If you want to run the downloader from the source code, follow these steps:

1.  **Clone the Repository**:
    ```sh
    git clone https://github.com/your-username/Moaz-Video-Downloader-V.1.0.git
    cd Moaz-Video-Downloader-V.1.0
    ```

2.  **Install Dependencies**:
    It is recommended to use a virtual environment.
   ```sh
    python -m venv venv
    venv\Scripts\activate
   pip install -r requirements.txt
   ```

3.  **Download FFmpeg**:
    You will need `ffmpeg.exe` for merging video and audio files.
    - Download the latest "essentials" build from [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
    - Extract the `.zip` file.
    - Copy `ffmpeg.exe` from the `bin` folder into the root directory of this project.

4.  **Run the App**:
   ```sh
    python "Moaz Downloader.py"
   ```

## Packaging for Windows

- The `installer.iss` script is used with [Inno Setup](https://jrsoftware.org/isinfo.php) to create the final Windows installer.
- The `Moaz Downloader.spec` file is used with [PyInstaller](https://pyinstaller.org/en/stable/) to bundle the Python script into a single executable.

## Adding/Editing Languages

- Edit or add JSON files in `downloader/languages/`.

## Troubleshooting
- If you see errors about ffmpeg, ensure `ffmpeg.exe` is in the app folder or use the auto-download button in settings.
- For yt-dlp issues, use the "Check for Updates" button in settings.

## License
MIT

---
How to Use:

- Single Video: Paste or drag a video URL into the app and click Download.
- Batch Download: Paste multiple URLs (one per line) and click Batch Download.
- Settings: Change language, theme, output folder, and more in the Settings tab.
-**Please, choose another download directory than the default (Downloads)**.
- Ignore the error of (download failed), I am working on it. You will find your files in the directory.
- For some audio-only files, you may need to download ffmpeg. (https://ffmpeg.org/download.html)
- The app will notify you when downloads finish.
---

For help, click the Help menu inside the app.
If you have a problem, contact me (mazmhmd493@gmail.com).