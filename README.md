# 🎙️ Danish Radio Transcriber

## Overview  
A Python app that records live Danish radio, transcribes it with Whisper, translates into Spanish & English and displays everything in your terminal.

## Prerequisites  
- Python 3.8+  
- ffmpeg (incl. ffplay)  
  ```bash
  brew install ffmpeg   # macOS/Homebrew 

Installation & Setup
1 Clone this repo and cd terminal-version/.
Create & activate a venv:

python3 -m venv .venv
source .venv/bin/activate

Install Python dependencies:

pip install openai python-dotenv rich 


Copy .env.example → .env and add your key:

OPENAI_API_KEY= (YOUR KEY) 



Usage
Verify ffmpeg & ffplay are on your $PATH.
Make the script executable & run it:
chmod +x transcribe_ver_3.py
./transcribe_ver_3.py

The app will:
Record 60 s blocks from the default URL
Transcribe Danish → text via Whisper
Translate text → Spanish & English
Show panels in terminal (Rich)
Optionally play back the clip
Append logs to transcripcion_YYYY-MM-DD.txt
Configuration

RADIO_URL: change to any Icecast/SHOUTcast MP3 stream
BLOCK_DURATION: seconds per segment
LANGUAGE: any ISO-639 code (da, es, en, fr, de, it, pt, ru, zh, etc.)
How It Works
Capture with ffmpeg → WAV.
Transcribe via openai.audio.transcriptions.create(…).
Translate via openai.chat.completions.create(…).
Render panels in terminal (Rich).
Log audio & text to disk.
Tech Stack
Python 3
ffmpeg / ffplay
OpenAI Whisper & GPT-3.5-turbo
rich for console UI
python-dotenv

Contributing & License
Feel free to open issues or PRs. Please keep your API key out of commits—use .env.

This README is generated for the “Danish Radio Transcriber” project.





Prerequisites
Python 3.8+
ffmpeg (includes ffplay)
macOS (Homebrew): brew install ffmpeg
Git (optional, for cloning and version control)
Installation & Setup
Clone your repo and cd into the terminal-version folder.
Create & activate a virtual environment:
Install Python dependencies:
Create a .env file in the same directory with your key:
Usage
Ensure ffmpeg and ffplay are on your $PATH.
Give the script execute permission and run it:
The app will record 60-second audio blocks, transcribe Danish → text (Whisper), translate into Spanish & English, display panels, play back audio, and append to a daily log file.



The Danish Radio Transcriber is a Python-based application that captures live Danish(Or other languages)  radio streams, transcribes the audio into text in real-time (or with a slight delay), and translates the transcriptions into Spanish and English. It leverages modern AI technologies to provide accurate transcriptions and translations, making it easier for non-Danish speakers to understand live radio broadcasts.

Purpose
The primary goal of this project is to enable users to listen to Danish radio stations while simultaneously accessing transcriptions and translations of the content in multiple languages. This is particularly useful for:

Language learners who want to practice Danish while seeing translations.
International listeners interested in Danish culture, news, or music.

Developers exploring real-time audio processing and AI-driven transcription/translation.
How It Works

The application operates by:

Capturing Audio: Uses ffmpeg to record 60-second audio blocks from a live Danish radio stream (default: DR P3 at https://live-icy.dr.dk/A/A03H.mp3).
Transcribing Audio: Processes the audio using OpenAI's Whisper model (whisper-1) to transcribe Danish speech into text.

Translating Text: Translates the transcribed text into Spanish and English using OpenAI's GPT-3.5-turbo model.

Displaying Results: Shows transcriptions and translations in a visually appealing console interface using the rich library.

Saving Outputs: Saves audio blocks in the audio_blocks/ folder and transcriptions/translations in a daily text file (transcription_YYYY-MM-DD.txt).
Playback: Allows optional replay of recorded audio blocks.
Technologies Used

Python: Core programming language for the application.
ffmpeg: Handles audio capture and playback.
OpenAI Whisper: Performs real-time audio transcription.
OpenAI GPT-3.5-turbo: Provides high-quality translations.
rich: Enhances console output with formatted text and panels.
python-dotenv: Manages API keys securely.

Potential Use Cases
Educational Tool: Helps Danish language learners by providing real-time transcriptions and translations.
Accessibility: Makes Danish radio content accessible to non-Danish speakers.
Research: Useful for analyzing live radio broadcasts in multiple languages.

Open Source Contribution: A starting point for developers interested in audio processing, AI, or real-time applications.

Limitations

Requires an active internet connection for streaming and API calls.
Depends on a valid OpenAI API key, which may incur costs.

Performance may vary depending on the quality of the radio stream and system resources.
Currently configured for Danish radio; adapting to other languages requires code modifications.
Future Improvements
Support for additional radio stations and languages.
Real-time streaming without fixed block durations.
A graphical user interface (GUI) for easier interaction.
Integration with other transcription/translation APIs for cost optimization.
Enhanced error handling and logging for debugging.
Get Involved

This is an open-source project, and contributions are welcome! Check the README.md for instructions on how to set up and contribute to the project. Feel free to open issues or submit pull requests on GitHub.
