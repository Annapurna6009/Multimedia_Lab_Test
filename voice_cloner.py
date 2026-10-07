import os
from io import BytesIO

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs


load_dotenv()


def get_client():
    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not api_key:
        raise RuntimeError(
            "ELEVENLABS_API_KEY is not configured. "
            "Add it to your .env file."
        )

    return ElevenLabs(api_key=api_key)


def clone_voice(
    audio_path,
    voice_name="Multimedia Analyzer Voice"
):
    """
    Create an Instant Voice Clone using an audio sample.

    The audio should belong to the person whose voice is being cloned
    or be used with that person's permission.

    Returns:
        voice_id
    """

    if not os.path.exists(audio_path):
        raise FileNotFoundError(
            f"Voice sample not found: {audio_path}"
        )

    client = get_client()

    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()

    voice = client.voices.ivc.create(
        name=voice_name,
        files=[
            BytesIO(audio_data)
        ]
    )

    return voice.voice_id


def generate_speech(
    text,
    voice_id,
    output_path="outputs/cloned_voice.mp3",
    model_id="eleven_multilingual_v2"
):
    """
    Generate speech using the cloned voice.
    """

    if not text.strip():
        raise ValueError("Text cannot be empty.")

    client = get_client()

    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128"
    )

    os.makedirs(
        os.path.dirname(output_path) or ".",
        exist_ok=True
    )

    with open(output_path, "wb") as output_file:
        for chunk in audio:
            output_file.write(chunk)

    return output_path


def clone_and_generate(
    audio_path,
    text,
    voice_name="Multimedia Analyzer Voice",
    output_path="outputs/cloned_voice.mp3"
):
    """
    Complete pipeline:

    reference audio
        ↓
    voice cloning
        ↓
    cloned voice ID
        ↓
    text-to-speech
        ↓
    MP3
    """

    voice_id = clone_voice(
        audio_path=audio_path,
        voice_name=voice_name
    )

    generated_audio = generate_speech(
        text=text,
        voice_id=voice_id,
        output_path=output_path
    )

    return {
        "voice_id": voice_id,
        "output_file": generated_audio
    }
