
import requests
import tempfile
import os
import subprocess
import json
from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_path):
    """Extract audio from video file"""
    try:
        video = VideoFileClip(video_path)
        audio_path = video_path.replace('.mp4', '.wav').replace('.avi', '.wav').replace('.mov', '.wav')
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        video.close()
        return audio_path
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None

def transcribe_with_assemblyai_free(audio_path):
    """Use AssemblyAI free tier (416 free hours)"""
    try:
        # You need to sign up for AssemblyAI free account and get API key
        # Replace 'your_assemblyai_api_key' with actual key
        API_KEY = "your_assemblyai_api_key"  

        if API_KEY == "your_assemblyai_api_key":
            # Fallback to local Whisper if no API key
            return transcribe_with_local_whisper(audio_path)

        headers = {
            "authorization": API_KEY,
            "content-type": "application/json"
        }

        # Upload audio file
        with open(audio_path, 'rb') as f:
            upload_response = requests.post(
                "https://api.assemblyai.com/v2/upload",
                files={'file': f},
                headers={"authorization": API_KEY}
            )

        audio_url = upload_response.json()['upload_url']

        # Request transcription
        transcript_request = {
            "audio_url": audio_url,
            "language_code": "en"
        }

        response = requests.post(
            "https://api.assemblyai.com/v2/transcript",
            json=transcript_request,
            headers=headers
        )

        transcript_id = response.json()['id']

        # Poll for completion
        while True:
            transcript_response = requests.get(
                f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
                headers=headers
            )

            if transcript_response.json()['status'] == 'completed':
                return transcript_response.json()['text']
            elif transcript_response.json()['status'] == 'error':
                return f"Transcription error: {transcript_response.json()['error']}"

            import time
            time.sleep(3)

    except Exception as e:
        print(f"AssemblyAI error: {e}")
        return transcribe_with_local_whisper(audio_path)

def transcribe_with_local_whisper(audio_path):
    """Fallback to local Whisper model (free)"""
    try:
        import whisper

        # Load the base model (free)
        model = whisper.load_model("base")

        # Transcribe
        result = model.transcribe(audio_path)
        return result["text"]

    except ImportError:
        return "Please install whisper: pip install openai-whisper"
    except Exception as e:
        return f"Local whisper error: {e}"

def transcribe_with_speechrecognition_free(audio_path):
    """Use Google Speech Recognition free tier"""
    try:
        import speech_recognition as sr

        r = sr.Recognizer()

        # Convert to wav if needed
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)

        # Use Google's free service (has daily limits)
        text = r.recognize_google(audio)
        return text

    except ImportError:
        return "Please install: pip install SpeechRecognition"
    except Exception as e:
        return f"Speech recognition error: {e}"

def transcribe_video(video_path):
    """Main transcription function"""
    try:
        # Extract audio from video
        audio_path = extract_audio_from_video(video_path)
        if not audio_path:
            return "Failed to extract audio from video"

        # Try different free transcription services
        transcript = None

        # Method 1: Try AssemblyAI free tier first (most accurate)
        transcript = transcribe_with_assemblyai_free(audio_path)

        # Method 2: Fallback to local Whisper
        if not transcript or "error" in transcript.lower():
            transcript = transcribe_with_local_whisper(audio_path)

        # Method 3: Final fallback to Google Speech Recognition
        if not transcript or "error" in transcript.lower():
            transcript = transcribe_with_speechrecognition_free(audio_path)

        # Clean up audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)

        return transcript or "Failed to transcribe audio"

    except Exception as e:
        return f"Transcription failed: {e}"
