
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import tempfile
import json
from enhanced_visual_analysis import analyze_frames, extract_comprehensive_frames
from visual_only_summarization import create_visual_only_summary
from video_processing import validate_video_file, get_video_info

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file found'}), 400

        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload a video file.'}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Validate video file
        is_valid, message = validate_video_file(filepath)
        if not is_valid:
            os.remove(filepath)  # Clean up invalid file
            return jsonify({'error': f'Invalid video file: {message}'}), 400

        # Get video information
        video_info = get_video_info(filepath)

        # Return file info for processing
        return jsonify({
            'message': 'Video uploaded successfully',
            'filename': filename,
            'filepath': filepath,
            'video_info': video_info
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process-visual', methods=['POST'])
def process_video_visual_only():
    try:
        data = request.json
        filepath = data.get('filepath')
        user_preferences = data.get('preferences', {})

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Video file not found'}), 400

        print("Starting visual-only analysis...")

        # Step 1: Extract comprehensive frames for detailed visual analysis
        print("Step 1: Extracting key frames from video...")
        max_frames = user_preferences.get('detail_level', 15)  # Default 15 frames
        frames_data = extract_comprehensive_frames(filepath, max_frames=max_frames)

        if not frames_data:
            return jsonify({'error': 'Failed to extract frames from video'}), 500

        print(f"Extracted {len(frames_data)} frames for analysis")

        # Step 2: Perform comprehensive visual analysis
        print("Step 2: Analyzing visual content...")
        visual_analysis = analyze_frames(frames_data)

        if 'error' in visual_analysis:
            return jsonify({'error': f'Visual analysis failed: {visual_analysis["error"]}'}), 500

        # Step 3: Create final visual summary based on user preferences
        print("Step 3: Creating visual summary...")
        final_summary = create_visual_only_summary(
            visual_analysis, 
            user_preferences
        )

        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            'visual_analysis': visual_analysis,
            'final_summary': final_summary,
            'processing_mode': 'visual_only',
            'frames_analyzed': len(frames_data),
            'success': True
        }), 200

    except Exception as e:
        print(f"Processing error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/analyze-frame', methods=['POST'])
def analyze_single_frame():
    """Endpoint to analyze a single frame at specific timestamp"""
    try:
        data = request.json
        filepath = data.get('filepath')
        timestamp = data.get('timestamp', 0)

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Video file not found'}), 400

        # Extract frame at specific timestamp
        cap = cv2.VideoCapture(filepath)
        if not cap.isOpened():
            return jsonify({'error': 'Cannot open video file'}), 400

        # Seek to timestamp
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_number = int(timestamp * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        ret, frame = cap.read()
        cap.release()

        if not ret:
            return jsonify({'error': 'Cannot extract frame at specified timestamp'}), 400

        # Analyze this specific frame
        frame_resized = cv2.resize(frame, (800, 600))
        frames_data = [{'frame': frame_resized, 'timestamp': timestamp, 'frame_number': frame_number, 'type': 'user_requested'}]

        analysis = analyze_frames(frames_data)

        return jsonify({
            'frame_analysis': analysis,
            'timestamp': timestamp,
            'success': True
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/video-info', methods=['POST'])
def get_video_information():
    """Get basic information about uploaded video"""
    try:
        data = request.json
        filepath = data.get('filepath')

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Video file not found'}), 400

        video_info = get_video_info(filepath)

        return jsonify({
            'video_info': video_info,
            'success': True
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'mode': 'visual_only'}), 200

if __name__ == '__main__':
    print("🎬 Starting Visual-Only Video Summarizer...")
    print("📊 This version analyzes only visual content (no audio processing)")
    print("🚀 Server starting on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
