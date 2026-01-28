# Text to Video Generator with Google Veo

This application allows you to generate videos from text prompts using Google's Veo 3.1 model via the Gemini API.

## Features
- **Google Veo Integration:** Generate high-quality AI videos using Gemini API.
- **Local Fallback:** Automatically falls back to basic FFmpeg-based video generation if no API key is provided.
- **Web Interface:** Easy-to-use Flask-based web interface with loading indicators.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **System Dependencies:**
   Ensure `ffmpeg` is installed on your system.

3. **Configuration:**
   Create a `.env` file in the root directory and add your Google API Key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

1. **Start the server:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   Navigate to `http://localhost:3000`

3. **Generate:**
   Enter your prompt and click "Generate Video".

## Unlimited & Free Usage
- The **Google Veo** service is subject to Google's API pricing and rate limits.
- The **Local Fallback** (used when no API key is set) is free and unlimited as it runs locally on your machine.
