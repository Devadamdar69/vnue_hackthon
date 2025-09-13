
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import tempfile
import json
from utils.transcription import transcribe_video
from utils.visual_analysis import analyze_frames
from utils.summarization import create_final_summary
from utils.video_processing import extract_frames

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

        # Return file info for processing
        return jsonify({
            'message': 'Video uploaded successfully',
            'filename': filename,
            'filepath': filepath
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process', methods=['POST'])
def process_video():
    try:
        data = request.json
        filepath = data.get('filepath')
        user_preferences = data.get('preferences', {})

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Video file not found'}), 400

        # Step 1: Extract transcript using free transcription API
        print("Step 1: Extracting transcript...")
        transcript = transcribe_video(filepath)

        # Step 2: Extract and analyze frames using free computer vision API
        print("Step 2: Analyzing video frames...")
        frames_data = extract_frames(filepath)
        visual_analysis = analyze_frames(frames_data)

        # Step 3: Combine both analyses and create final summary
        print("Step 3: Creating final summary...")
        final_summary = create_final_summary(
            transcript, 
            visual_analysis, 
            user_preferences
        )

        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)
 
        return jsonify({
            'transcript': transcript,
            'visual_analysis': visual_analysis,
            'final_summary': final_summary,
            'success': True
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
