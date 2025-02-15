# YouTube Downloader with Animated Progress Bar

This is a Python program that downloads YouTube videos using a graphical interface built with `tkinter` and the `yt_dlp` library. It features an animated green progress bar that updates in real-time to show the overall download progress and displays a final message (in both English and Arabic) when all downloads are complete.

---

## Features

- **Graphical User Interface (GUI):**  
  - A text area for entering multiple YouTube video links (one link per line).
  - An animated progress bar that updates as videos are being downloaded.
  - A "Download Videos" button to start the download process.
  - A "GITHUB" button that opens the developer's GitHub page.
  - A "Created by: Abdelrhaman" label.

- **Animated Progress Bar:**  
  The progress bar moves continuously to reflect the download progress of each video, showing the current overall percentage.

- **Multi-threaded Downloads:**  
  Downloads run in a separate thread to keep the interface responsive.

- **Real-time Progress Updates:**  
  Utilizes `yt_dlp`'s progress hook to update the progress bar with the current video's download percentage.

---

## Prerequisites

Before running the program, ensure you have the following installed:

1. **Python 3.x**

2. **FFmpeg**  
   Required for processing audio and video streams. Follow these steps to install:

   - **Download and Install FFmpeg:**
     1. Download the latest Windows build from [FFmpeg Release Essentials](https://www.gyan.dev/ffmpeg/builds/).
     2. Extract the ZIP file to a folder (e.g., `C:\ffmpeg`).

   - **Add FFmpeg to System PATH:**
     1. Navigate to the `bin` folder inside your extracted FFmpeg directory (contains `ffmpeg.exe`).
     2. Add this path to your system environment variables:
        - Press `Win + S` and search for "Edit the system environment variables".
        - Click **Environment Variables**.
        - Under "System Variables", select **Path** → **Edit**.
        - Click **New** and add the path to your FFmpeg `bin` folder (e.g., `C:\ffmpeg\bin`).
     3. Restart your Command Prompt/PowerShell to apply changes.

3. **yt_dlp Library**  
   Install via pip:
   ```bash
   pip install yt-dlp