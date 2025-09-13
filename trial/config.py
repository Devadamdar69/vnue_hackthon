
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    UPLOAD_FOLDER = 'uploads'

    # API Keys (sign up for free accounts to get these)
    ASSEMBLYAI_API_KEY = os.environ.get('ASSEMBLYAI_API_KEY') or 'your_assemblyai_api_key'
    HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY') or 'your_huggingface_api_key'
    IMAGGA_API_KEY = os.environ.get('IMAGGA_API_KEY') or 'your_imagga_api_key'
    IMAGGA_API_SECRET = os.environ.get('IMAGGA_API_SECRET') or 'your_imagga_api_secret'
    GOOGLE_VISION_API_KEY = os.environ.get('GOOGLE_VISION_API_KEY') or 'your_google_vision_api_key'

    # Processing Configuration
    MAX_FRAMES_TO_ANALYZE = 10
    MAX_VIDEO_DURATION = 600  # 10 minutes max
    SUPPORTED_FORMATS = ['mp4', 'avi', 'mov', 'mkv', 'webm']

    # Free API Limits (adjust based on your accounts)
    ASSEMBLYAI_FREE_HOURS = 416  # Free tier limit
    IMAGGA_FREE_REQUESTS = 1000  # Free tier limit per month
    GOOGLE_VISION_FREE_REQUESTS = 1000  # Free tier limit per month
