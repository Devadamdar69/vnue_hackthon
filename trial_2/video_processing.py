
import cv2
import os
import numpy as np
from moviepy import (
    VideoFileClip,
    ImageClip,
    TextClip,
    CompositeVideoClip,
    AudioFileClip,
    concatenate_videoclips
)
import tempfile

def get_video_info(video_path):
    """Get basic video information"""
    try:
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            return None

        fps = cap.get(cv2.CAV_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0

        cap.release()

        return {
            'duration': duration,
            'fps': fps,
            'frame_count': frame_count,
            'width': width,
            'height': height,
            'file_size': os.path.getsize(video_path) if os.path.exists(video_path) else 0
        }

    except Exception as e:
        print(f"Error getting video info: {e}")
        return None

def extract_frames(video_path, max_frames=10):
    """Extract frames from video for analysis"""
    try:
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            return []

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Calculate interval to get evenly spaced frames
        interval = max(1, total_frames // max_frames)

        frames_with_times = []
        frame_count = 0

        while cap.isOpened() and len(frames_with_times) < max_frames:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % interval == 0:
                timestamp = frame_count / fps if fps > 0 else 0
                # Resize frame to manageable size
                frame_resized = cv2.resize(frame, (640, 480))
                frames_with_times.append((frame_resized, timestamp))

            frame_count += 1

        cap.release()
        return frames_with_times

    except Exception as e:
        print(f"Error extracting frames: {e}")
        return []

def validate_video_file(video_path):
    """Validate if file is a proper video file"""
    try:
        if not os.path.exists(video_path):
            return False, "File does not exist"

        # Check file extension
        valid_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv']
        file_ext = os.path.splitext(video_path)[1].lower()

        if file_ext not in valid_extensions:
            return False, f"Unsupported file format: {file_ext}"

        # Try to open with OpenCV
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            cap.release()
            return False, "Cannot open video file"

        # Check if video has frames
        ret, frame = cap.read()
        cap.release()

        if not ret:
            return False, "Video file appears to be corrupted"

        # Check file size (limit to 100MB for free processing)
        file_size = os.path.getsize(video_path)
        max_size = 100 * 1024 * 1024  # 100MB

        if file_size > max_size:
            return False, f"File too large: {file_size / (1024*1024):.1f}MB (max: 100MB)"

        return True, "Valid video file"

    except Exception as e:
        return False, f"Validation error: {e}"

def compress_video_if_needed(video_path, max_size_mb=50):
    """Compress video if it's too large for processing"""
    try:
        file_size_mb = os.path.getsize(video_path) / (1024 * 1024)

        if file_size_mb <= max_size_mb:
            return video_path  # No compression needed

        # Create compressed version
        base_name = os.path.splitext(video_path)[0]
        compressed_path = f"{base_name}_compressed.mp4"

        # Use moviepy to compress
        video = VideoFileClip(video_path)

        # Calculate target resolution to achieve size limit
        compression_ratio = max_size_mb / file_size_mb
        new_width = int(video.w * (compression_ratio ** 0.5))
        new_height = int(video.h * (compression_ratio ** 0.5))

        # Ensure dimensions are even (required for some codecs)
        new_width = new_width - (new_width % 2)
        new_height = new_height - (new_height % 2)

        video_resized = video.resize((new_width, new_height))
        video_resized.write_videofile(
            compressed_path,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )

        video.close()
        video_resized.close()

        return compressed_path

    except Exception as e:
        print(f"Compression error: {e}")
        return video_path  # Return original if compression fails

def cleanup_temp_files(*file_paths):
    """Clean up temporary files"""
    for file_path in file_paths:
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                print(f"Cleaned up: {file_path}")
        except Exception as e:
            print(f"Error cleaning up {file_path}: {e}")

def create_video_thumbnail(video_path, timestamp=None):
    """Create thumbnail from video at specified timestamp"""
    try:
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            return None

        # If timestamp not specified, use middle of video
        if timestamp is None:
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            timestamp = (total_frames / fps) / 2 if fps > 0 else 0

        # Seek to timestamp
        cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)

        ret, frame = cap.read()
        cap.release()

        if ret:
            # Resize to thumbnail size
            thumbnail = cv2.resize(frame, (320, 240))

            # Save thumbnail
            thumbnail_path = video_path.replace('.mp4', '_thumb.jpg')
            cv2.imwrite(thumbnail_path, thumbnail)

            return thumbnail_path

        return None

    except Exception as e:
        print(f"Thumbnail creation error: {e}")
        return None
