import os
import requests
from dotenv import load_dotenv

def convert_speech_to_speech(input_path, output_path=None, voice_id="CwhRBWXzGAHq8TQ4Fs17"):
    """
    Converts speech in the given audio file to another voice using ElevenLabs Speech-to-Speech API.
    """
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is not configured in .env file.")
        
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Audio file not found: {input_path}")
        
    if output_path is None:
        filename, extension = os.path.splitext(input_path)
        output_path = f"{filename}_sts{extension}"

    url = f"https://api.elevenlabs.io/v1/speech-to-speech/{voice_id}"
    headers = {"xi-api-key": api_key}

    with open(input_path, 'rb') as audio_file:
        files = {'audio': (input_path, audio_file, 'audio/mpeg')}
        data = {"model_id": "eleven_english_sts_v2"}
        response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code == 200:
        with open(output_path, 'wb') as output_file:
            output_file.write(response.content)
        return output_path
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")
