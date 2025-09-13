
import cv2
import requests
import base64
import json
import numpy as np
from io import BytesIO
import time

def extract_key_frames(video_path, max_frames=10):
    """Extract key frames from video for analysis"""
    try:
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            return []

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps

        # Extract frames at regular intervals
        interval = max(1, total_frames // max_frames)
        frames = []
        frame_times = []

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % interval == 0 and len(frames) < max_frames:
                # Resize frame to reduce API payload
                frame_resized = cv2.resize(frame, (640, 480))
                frames.append(frame_resized)
                frame_times.append(frame_count / fps)

            frame_count += 1

        cap.release()
        return list(zip(frames, frame_times))

    except Exception as e:
        print(f"Error extracting frames: {e}")
        return []

def frame_to_base64(frame):
    """Convert frame to base64 for API calls"""
    try:
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        return frame_base64
    except Exception as e:
        print(f"Error converting frame to base64: {e}")
        return None

def analyze_with_imagga_free(frame_base64):
    """Use Imagga free tier (1000 requests/month)"""
    try:
        # You need to sign up for Imagga and get API credentials
        API_KEY = "your_imagga_api_key"
        API_SECRET = "your_imagga_api_secret"

        if API_KEY == "your_imagga_api_key":
            return analyze_with_opencv_local(frame_base64)

        url = "https://api.imagga.com/v2/tags"

        response = requests.post(
            url,
            auth=(API_KEY, API_SECRET),
            files={'image': base64.b64decode(frame_base64)}
        )

        if response.status_code == 200:
            data = response.json()
            tags = [tag['tag']['en'] for tag in data['result']['tags'][:10]]
            return {
                'objects': tags,
                'confidence': [tag['confidence'] for tag in data['result']['tags'][:10]]
            }
        else:
            return analyze_with_opencv_local(frame_base64)

    except Exception as e:
        print(f"Imagga API error: {e}")
        return analyze_with_opencv_local(frame_base64)

def analyze_with_google_vision_free(frame_base64):
    """Use Google Cloud Vision free tier (1000 requests/month)"""
    try:
        # You need Google Cloud credentials
        # This is a simplified example - you'd need proper auth setup
        API_KEY = "your_google_vision_api_key"

        if API_KEY == "your_google_vision_api_key":
            return analyze_with_opencv_local(frame_base64)

        url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"

        payload = {
            "requests": [{
                "image": {"content": frame_base64},
                "features": [
                    {"type": "LABEL_DETECTION", "maxResults": 10},
                    {"type": "OBJECT_LOCALIZATION", "maxResults": 10}
                ]
            }]
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            if 'responses' in data and len(data['responses']) > 0:
                labels = data['responses'][0].get('labelAnnotations', [])
                objects = data['responses'][0].get('localizedObjectAnnotations', [])

                return {
                    'labels': [label['description'] for label in labels],
                    'objects': [obj['name'] for obj in objects],
                    'confidence': [label['score'] for label in labels]
                }

        return analyze_with_opencv_local(frame_base64)

    except Exception as e:
        print(f"Google Vision API error: {e}")
        return analyze_with_opencv_local(frame_base64)

def analyze_with_opencv_local(frame_base64):
    """Fallback local analysis using OpenCV (completely free)"""
    try:
        # Decode base64 back to image
        img_data = base64.b64decode(frame_base64)
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Simple color analysis
        avg_color = np.mean(frame, axis=(0, 1))
        dominant_color = get_dominant_color_name(avg_color)

        # Edge detection for complexity
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])

        # Brightness analysis
        brightness = np.mean(gray)

        # Simple motion detection could be added here
        scene_type = classify_scene_simple(brightness, edge_density)

        return {
            'dominant_color': dominant_color,
            'brightness_level': 'bright' if brightness > 127 else 'dark',
            'complexity': 'complex' if edge_density > 0.1 else 'simple',
            'scene_type': scene_type,
            'confidence': [0.7]  # Default confidence for local analysis
        }

    except Exception as e:
        print(f"Local OpenCV analysis error: {e}")
        return {
            'objects': ['unknown'],
            'confidence': [0.5],
            'error': str(e)
        }

def get_dominant_color_name(bgr_color):
    """Convert BGR color to color name"""
    b, g, r = bgr_color

    if r > g and r > b:
        return 'red-dominant'
    elif g > r and g > b:
        return 'green-dominant'
    elif b > r and b > g:
        return 'blue-dominant'
    elif r > 200 and g > 200 and b > 200:
        return 'bright'
    elif r < 50 and g < 50 and b < 50:
        return 'dark'
    else:
        return 'neutral'

def classify_scene_simple(brightness, edge_density):
    """Simple scene classification"""
    if brightness > 180 and edge_density < 0.05:
        return 'outdoor/bright'
    elif brightness < 80:
        return 'indoor/dark'
    elif edge_density > 0.15:
        return 'complex/detailed'
    else:
        return 'standard'

def analyze_frames(frames_with_times):
    """Main function to analyze all extracted frames"""
    try:
        if not frames_with_times:
            return {"error": "No frames to analyze"}

        frame_analysis = []

        for i, (frame, timestamp) in enumerate(frames_with_times):
            print(f"Analyzing frame {i+1}/{len(frames_with_times)}...")

            # Convert frame to base64
            frame_base64 = frame_to_base64(frame)
            if not frame_base64:
                continue

            # Try different free APIs in order of preference
            analysis = None

            # Method 1: Try Imagga free tier
            analysis = analyze_with_imagga_free(frame_base64)

            # Method 2: Try Google Vision free tier  
            if not analysis or 'error' in analysis:
                analysis = analyze_with_google_vision_free(frame_base64)

            # Method 3: Fallback to local OpenCV
            if not analysis or 'error' in analysis:
                analysis = analyze_with_opencv_local(frame_base64)

            frame_analysis.append({
                'timestamp': timestamp,
                'frame_number': i + 1,
                'analysis': analysis
            })

            # Rate limiting for free APIs
            time.sleep(0.5)

        # Aggregate analysis across all frames
        return aggregate_frame_analysis(frame_analysis)

    except Exception as e:
        return {"error": f"Frame analysis failed: {e}"}

def aggregate_frame_analysis(frame_analysis):
    """Combine analysis from all frames into summary"""
    try:
        all_objects = []
        all_labels = []
        scene_changes = []

        for frame_data in frame_analysis:
            analysis = frame_data['analysis']

            # Collect all detected objects/labels
            if 'objects' in analysis:
                all_objects.extend(analysis['objects'])
            if 'labels' in analysis:
                all_labels.extend(analysis['labels'])

            # Track scene information
            scene_changes.append({
                'timestamp': frame_data['timestamp'],
                'scene_info': analysis
            })

        # Count frequency of detected items
        from collections import Counter
        object_counts = Counter(all_objects + all_labels)
        top_objects = object_counts.most_common(10)

        return {
            'total_frames_analyzed': len(frame_analysis),
            'top_visual_elements': [item[0] for item in top_objects],
            'element_frequencies': dict(top_objects),
            'scene_changes': scene_changes,
            'visual_summary': f"Video contains primarily: {', '.join([item[0] for item in top_objects[:5]])}"
        }

    except Exception as e:
        return {"error": f"Analysis aggregation failed: {e}"}
