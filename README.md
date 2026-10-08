# Multimedia Analyzer

A command-line tool that analyzes multimedia files (images, audio, and video) and provides detailed metadata reports. It also includes advanced capabilities such as image enhancement, voice cloning, and speech-to-speech conversion.

## Features

- **Image Analysis & Enhancement:** Extracts format, dimensions, color mode, and EXIF metadata. Apply `--enhance` to automatically boost brightness, contrast, color, sharpness, and apply a denoising filter.
- **Audio Analysis:** Extracts channels, sampling rate, bit rate, duration, and ID3 metadata. 
- **Voice Cloning:** Clone a voice using the ElevenLabs API and generate new text-to-speech audio.
- **Speech-to-Speech:** Convert an existing audio voice sample into another voice using the ElevenLabs API.
- **Video Analysis:** Extracts video/audio streams, resolution, frame rate, bit rate, codecs, and metadata.

## Installation

### 1. Python Dependencies
Ensure you have Python 3.7+ installed. Install the required Python packages by running:

```bash
pip install -r requirements.txt
```

### 2. Install FFmpeg (Required for Video Analysis)
The video analyzer relies on `ffprobe` (which is part of the `FFmpeg` suite) to extract video data. 

**Windows (using Winget):**
```bash
winget install -e --id Gyan.FFmpeg
```
*(After installing, you may need to restart your terminal for the PATH variables to update).*

**Mac (using Homebrew):**
```bash
brew install ffmpeg
```

### 3. API Key Configuration (Required for Voice Features)
To use the Voice Cloning or Speech-to-Speech features, you must provide an [ElevenLabs](https://elevenlabs.io/) API key.

1. Create a file named `.env` in the root directory.
2. Add your secret API key (it must start with `sk_`):
```env
ELEVENLABS_API_KEY=sk_your_secret_api_key_here
```

## Usage

The main entry point is `main.py`. It accepts a path to a media file and automatically detects whether it is an image, audio, or video file.

### Basic Analysis
Run the analyzer on any supported file type (.jpg, .mp3, .mp4, etc.):
```bash
python main.py samples/sample.mp3
```
*The analysis report is automatically saved into the `reports/report.json` file.*

### Image Enhancement
Pass the `--enhance` flag alongside an image file path. This will analyze the image and save an enhanced version to your disk:
```bash
python main.py --enhance samples/sample.jpg
```

### Speech-to-Speech Conversion
Pass the `--speech-to-speech` flag alongside an audio file path to transform the voice in the audio file using the ElevenLabs API:
```bash
python main.py --speech-to-speech samples/voice-sample.mp3
```

### Voice Cloning (Text-to-Speech)
Pass the `--clone-voice` flag followed by the text you want to generate. The provided audio file will be used as the voice clone reference:
```bash
python main.py --clone-voice "Wow, my voice is being cloned from a sample!" samples/sample.mp3
```
*Note: This specific feature requires a paid ElevenLabs subscription tier that supports Instant Voice Cloning.*
