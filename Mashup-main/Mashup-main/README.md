# 🎵 YouTube Mashup Generator

A Python-based multimedia automation tool that creates audio mashups by downloading songs from YouTube, converting them to MP3 format, trimming each track to a fixed duration, and merging them into a single output file. The project provides both a command-line interface for batch processing and a Flask web interface for interactive mashup generation with direct ZIP downloads.

## ✨ Features
- Automated YouTube song downloading using **yt-dlp**
- Audio conversion, trimming, and merging with **pydub** and **FFmpeg**
- Configurable number of tracks and clip duration
- Command-line interface for scripted mashup generation
- Flask web interface for interactive mashup creation
- Direct ZIP file download of generated mashups

## 🛠️ Tech Stack
**Python 3.11** · yt-dlp · pydub · FFmpeg · Flask · yagmail

## 📁 Project Structure
- **program1/mashup_generator.py** – Core logic for downloading, processing, and merging audio  
- **program2/app.py** – Flask web application for mashup generation

## 🚀 How to Run

### Command-Line Interface (CLI)
```bash
cd program1
python mashup_generator.py "Singer Name" <number_of_videos> <duration_in_seconds> output.mp3
```
Example:
```bash
python mashup_generator.py "The Weeknd" 5 30 mashup.mp3
```

### Flask Web Interface
```bash
cd program2
python app.py
```
Open your browser and navigate to `http://localhost:5000` to access the web interface.

**Features:**
- Input singer name, number of videos, duration, and email ID
- Generates mashup using Program 1
- Creates a ZIP file containing the mashup
- Sends the ZIP file via email using **yagmail**
- Validates email format before sending

**Environment Variables:**
Set the following environment variables to enable email delivery:
```
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

## 👤 Author
**Harshit Kansal**  
**Roll No: 102303554**
