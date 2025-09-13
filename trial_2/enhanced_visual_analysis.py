
import cv2
import requests
import base64
import json
import numpy as np
from io import BytesIO
import time

def extract_comprehensive_frames(video_path, max_frames=20):
    """Extract more frames for detailed visual analysis"""
    try:
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            return []

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps

        # Extract frames at regular intervals + scene changes
        frames_data = []

        # Method 1: Regular intervals
        interval = max(1, total_frames // max_frames)

        frame_count = 0
        prev_frame = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Resize frame for analysis
            frame_resized = cv2.resize(frame, (800, 600))
            timestamp = frame_count / fps if fps > 0 else 0

            # Add regular interval frames
            if frame_count % interval == 0 and len(frames_data) < max_frames:
                frames_data.append({
                    'frame': frame_resized,
                    'timestamp': timestamp,
                    'frame_number': frame_count,
                    'type': 'regular'
                })

            # Detect scene changes (significant visual differences)
            if prev_frame is not None and len(frames_data) < max_frames:
                # Calculate frame difference
                diff = cv2.absdiff(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY), 
                                 cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY))
                change_percentage = np.sum(diff > 30) / (diff.shape[0] * diff.shape[1])

                # If significant change detected, add as scene change frame
                if change_percentage > 0.3:  # 30% of pixels changed significantly
                    frames_data.append({
                        'frame': frame_resized,
                        'timestamp': timestamp,
                        'frame_number': frame_count,
                        'type': 'scene_change',
                        'change_percentage': change_percentage
                    })

            prev_frame = cv2.resize(frame, (800, 600))
            frame_count += 1

        cap.release()
        return frames_data

    except Exception as e:
        print(f"Error extracting comprehensive frames: {e}")
        return []

def analyze_frame_with_gemini_free(frame_base64, timestamp):
    """Use Google Gemini free tier for frame analysis"""
    try:
        # This is a placeholder - you'd need actual Gemini API implementation
        # For now, we'll use local analysis as fallback
        return analyze_frame_with_opencv_advanced(frame_base64, timestamp)

    except Exception as e:
        return analyze_frame_with_opencv_advanced(frame_base64, timestamp)

def analyze_frame_with_opencv_advanced(frame_base64, timestamp):
    """Enhanced local OpenCV analysis for visual-only mode"""
    try:
        # Decode base64 back to image
        img_data = base64.b64decode(frame_base64)
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Enhanced visual analysis
        analysis = {}

        # 1. Color Analysis
        analysis['colors'] = analyze_colors(frame)

        # 2. Object Detection (basic shapes)
        analysis['shapes'] = detect_basic_shapes(frame)

        # 3. Text Detection
        analysis['text'] = detect_text_in_frame(frame)

        # 4. Motion/Activity Analysis
        analysis['activity'] = analyze_activity_level(frame)

        # 5. Scene Classification
        analysis['scene_type'] = classify_scene_advanced(frame)

        # 6. Composition Analysis
        analysis['composition'] = analyze_composition(frame)

        # 7. Quality Assessment
        analysis['quality'] = assess_frame_quality(frame)

        return {
            'timestamp': timestamp,
            'visual_elements': analysis,
            'confidence': 0.8,
            'analysis_method': 'opencv_advanced'
        }

    except Exception as e:
        return {
            'timestamp': timestamp,
            'error': str(e),
            'visual_elements': {},
            'confidence': 0.0
        }

def analyze_colors(frame):
    """Analyze color distribution and dominant colors"""
    try:
        # Convert to different color spaces
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

        # Calculate color histograms
        hist_b = cv2.calcHist([frame], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([frame], [1], None, [256], [0, 256])
        hist_r = cv2.calcHist([frame], [2], None, [256], [0, 256])

        # Dominant colors
        avg_b, avg_g, avg_r = np.mean(frame, axis=(0, 1))

        # Color temperature estimation
        color_temp = estimate_color_temperature(avg_r, avg_g, avg_b)

        # Saturation analysis
        saturation = np.mean(hsv[:, :, 1])

        return {
            'dominant_rgb': [int(avg_r), int(avg_g), int(avg_b)],
            'color_temperature': color_temp,
            'saturation_level': float(saturation),
            'color_scheme': classify_color_scheme(avg_r, avg_g, avg_b)
        }

    except Exception as e:
        return {'error': str(e)}

def detect_basic_shapes(frame):
    """Detect basic geometric shapes and patterns"""
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Edge detection
        edges = cv2.Canny(gray, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        shapes = {
            'rectangles': 0,
            'circles': 0,
            'triangles': 0,
            'total_objects': len(contours),
            'edge_density': np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        }

        # Classify shapes
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Only consider significant shapes
                # Approximate contour
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                if len(approx) == 3:
                    shapes['triangles'] += 1
                elif len(approx) == 4:
                    shapes['rectangles'] += 1
                else:
                    # Check if it's roughly circular
                    perimeter = cv2.arcLength(contour, True)
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    if circularity > 0.7:
                        shapes['circles'] += 1

        return shapes

    except Exception as e:
        return {'error': str(e)}

def detect_text_in_frame(frame):
    """Detect text using basic image processing"""
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Simple text detection using morphological operations
        # Detect horizontal text regions
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 2))
        morph = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

        # Find text regions
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Filter based on aspect ratio (typical for text)
            aspect_ratio = w / float(h)
            if 2 < aspect_ratio < 10 and w > 50 and h > 10:
                text_regions.append({
                    'x': int(x), 'y': int(y), 
                    'width': int(w), 'height': int(h),
                    'aspect_ratio': aspect_ratio
                })

        return {
            'text_regions_detected': len(text_regions),
            'regions': text_regions[:5],  # Top 5 regions
            'likely_contains_text': len(text_regions) > 0
        }

    except Exception as e:
        return {'error': str(e)}

def analyze_activity_level(frame):
    """Analyze the activity/motion level in the frame"""
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate image gradients to detect motion/activity
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        # Calculate gradient magnitude
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        activity_score = np.mean(magnitude)

        # Classify activity level
        if activity_score > 50:
            activity_level = 'high'
        elif activity_score > 25:
            activity_level = 'medium'
        else:
            activity_level = 'low'

        return {
            'activity_score': float(activity_score),
            'activity_level': activity_level,
            'motion_detected': activity_score > 30
        }

    except Exception as e:
        return {'error': str(e)}

def classify_scene_advanced(frame):
    """Advanced scene classification"""
    try:
        # Analyze various visual features
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Brightness analysis
        brightness = np.mean(gray)

        # Contrast analysis
        contrast = np.std(gray)

        # Edge density
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])

        # Color diversity
        colors = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color_diversity = np.std(colors[:, :, 1])  # Saturation std

        # Scene classification logic
        scene_features = {
            'brightness_level': 'bright' if brightness > 127 else 'dark',
            'contrast_level': 'high' if contrast > 50 else 'low',
            'complexity': 'complex' if edge_density > 0.1 else 'simple',
            'color_richness': 'colorful' if color_diversity > 30 else 'monochrome'
        }

        # Infer scene type
        if brightness > 180 and color_diversity > 40:
            scene_type = 'outdoor/nature'
        elif brightness < 80 and edge_density > 0.15:
            scene_type = 'indoor/complex'
        elif edge_density < 0.05 and contrast < 30:
            scene_type = 'static/presentation'
        elif edge_density > 0.2:
            scene_type = 'dynamic/action'
        else:
            scene_type = 'standard'

        return {
            'scene_type': scene_type,
            'features': scene_features,
            'brightness': float(brightness),
            'contrast': float(contrast),
            'edge_density': float(edge_density)
        }

    except Exception as e:
        return {'error': str(e)}

def analyze_composition(frame):
    """Analyze visual composition of the frame"""
    try:
        h, w = frame.shape[:2]

        # Rule of thirds analysis
        third_w, third_h = w // 3, h // 3

        # Analyze brightness in different regions
        regions = {
            'top_left': np.mean(frame[:third_h, :third_w]),
            'top_center': np.mean(frame[:third_h, third_w:2*third_w]),
            'top_right': np.mean(frame[:third_h, 2*third_w:]),
            'center_left': np.mean(frame[third_h:2*third_h, :third_w]),
            'center': np.mean(frame[third_h:2*third_h, third_w:2*third_w]),
            'center_right': np.mean(frame[third_h:2*third_h, 2*third_w:]),
            'bottom_left': np.mean(frame[2*third_h:, :third_w]),
            'bottom_center': np.mean(frame[2*third_h:, third_w:2*third_w]),
            'bottom_right': np.mean(frame[2*third_h:, 2*third_w:])
        }

        # Find the brightest region (likely focus area)
        brightest_region = max(regions, key=regions.get)

        # Calculate symmetry
        left_half = frame[:, :w//2]
        right_half = cv2.flip(frame[:, w//2:], 1)

        # Resize to match if needed
        if left_half.shape != right_half.shape:
            min_w = min(left_half.shape[1], right_half.shape[1])
            left_half = left_half[:, :min_w]
            right_half = right_half[:, :min_w]

        symmetry_score = 1.0 - (np.mean(np.abs(left_half.astype(float) - right_half.astype(float))) / 255.0)

        return {
            'focus_area': brightest_region,
            'symmetry_score': float(symmetry_score),
            'composition_balance': 'balanced' if 0.4 < symmetry_score < 0.6 else 'asymmetric',
            'region_brightness': {k: float(v) for k, v in regions.items()}
        }

    except Exception as e:
        return {'error': str(e)}

def assess_frame_quality(frame):
    """Assess technical quality of the frame"""
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Sharpness (using Laplacian variance)
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()

        # Noise estimation
        noise_level = np.std(gray - cv2.GaussianBlur(gray, (5, 5), 0))

        # Exposure assessment
        brightness = np.mean(gray)
        overexposed_pixels = np.sum(gray > 250) / gray.size
        underexposed_pixels = np.sum(gray < 5) / gray.size

        # Overall quality score
        quality_score = min(100, max(0, 
            (sharpness / 1000) * 30 + 
            (1 - noise_level / 50) * 30 +
            (1 - overexposed_pixels) * 20 +
            (1 - underexposed_pixels) * 20
        ))

        return {
            'sharpness_score': float(sharpness),
            'noise_level': float(noise_level),
            'brightness': float(brightness),
            'overexposed_percentage': float(overexposed_pixels * 100),
            'underexposed_percentage': float(underexposed_pixels * 100),
            'overall_quality': float(quality_score),
            'quality_rating': 'excellent' if quality_score > 80 else 
                           'good' if quality_score > 60 else 
                           'fair' if quality_score > 40 else 'poor'
        }

    except Exception as e:
        return {'error': str(e)}

def frame_to_base64(frame):
    """Convert frame to base64 for API calls"""
    try:
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        return frame_base64
    except Exception as e:
        print(f"Error converting frame to base64: {e}")
        return None

def analyze_frames(frames_data):
    """Main function to analyze all extracted frames for visual-only mode"""
    try:
        if not frames_data:
            return {"error": "No frames to analyze"}

        frame_analyses = []

        for i, frame_info in enumerate(frames_data):
            print(f"Analyzing frame {i+1}/{len(frames_data)} at {frame_info['timestamp']:.2f}s...")

            frame = frame_info['frame']
            timestamp = frame_info['timestamp']

            # Convert frame to base64
            frame_base64 = frame_to_base64(frame)
            if not frame_base64:
                continue

            # Perform comprehensive visual analysis
            analysis = analyze_frame_with_opencv_advanced(frame_base64, timestamp)

            # Add frame metadata
            analysis['frame_metadata'] = {
                'frame_number': frame_info['frame_number'],
                'type': frame_info['type'],
                'timestamp_formatted': format_timestamp(timestamp)
            }

            if 'change_percentage' in frame_info:
                analysis['frame_metadata']['scene_change_intensity'] = frame_info['change_percentage']

            frame_analyses.append(analysis)

            # Small delay to prevent overwhelming the system
            time.sleep(0.1)

        # Aggregate analysis across all frames
        return aggregate_visual_analysis(frame_analyses)

    except Exception as e:
        return {"error": f"Frame analysis failed: {e}"}

def aggregate_visual_analysis(frame_analyses):
    """Combine analysis from all frames into comprehensive visual summary"""
    try:
        # Collect data from all frames
        all_scene_types = []
        all_colors = []
        activity_levels = []
        quality_scores = []
        composition_data = []
        text_detections = []

        timeline_events = []

        for analysis in frame_analyses:
            if 'error' not in analysis and 'visual_elements' in analysis:
                elements = analysis['visual_elements']
                timestamp = analysis['timestamp']

                # Collect scene types
                scene_info = elements.get('scene_type', {})
                if 'scene_type' in scene_info:
                    all_scene_types.append(scene_info['scene_type'])

                # Collect color information
                color_info = elements.get('colors', {})
                if 'dominant_rgb' in color_info:
                    all_colors.append(color_info['color_scheme'])

                # Collect activity levels
                activity_info = elements.get('activity', {})
                if 'activity_level' in activity_info:
                    activity_levels.append(activity_info['activity_level'])

                # Collect quality scores
                quality_info = elements.get('quality', {})
                if 'overall_quality' in quality_info:
                    quality_scores.append(quality_info['overall_quality'])

                # Collect text detection
                text_info = elements.get('text', {})
                if text_info.get('likely_contains_text', False):
                    text_detections.append(timestamp)

                # Create timeline events
                timeline_events.append({
                    'timestamp': timestamp,
                    'timestamp_formatted': format_timestamp(timestamp),
                    'scene_type': scene_info.get('scene_type', 'unknown'),
                    'activity_level': activity_info.get('activity_level', 'unknown'),
                    'quality_rating': quality_info.get('quality_rating', 'unknown'),
                    'has_text': text_info.get('likely_contains_text', False),
                    'frame_type': analysis.get('frame_metadata', {}).get('type', 'regular')
                })

        # Calculate statistics
        from collections import Counter
        scene_distribution = Counter(all_scene_types)
        color_distribution = Counter(all_colors)
        activity_distribution = Counter(activity_levels)

        avg_quality = np.mean(quality_scores) if quality_scores else 0

        # Create comprehensive summary
        summary = {
            'total_frames_analyzed': len(frame_analyses),
            'video_characteristics': {
                'dominant_scene_types': dict(scene_distribution.most_common(3)),
                'color_schemes': dict(color_distribution.most_common(3)),
                'activity_levels': dict(activity_distribution.most_common()),
                'average_quality_score': float(avg_quality),
                'text_presence': len(text_detections) > 0,
                'text_timestamps': text_detections[:5]  # First 5 text occurrences
            },
            'timeline_analysis': timeline_events,
            'scene_changes': [event for event in timeline_events if event['frame_type'] == 'scene_change'],
            'visual_summary': create_visual_narrative(scene_distribution, activity_distribution, color_distribution, avg_quality),
            'key_moments': identify_key_visual_moments(timeline_events)
        }

        return summary

    except Exception as e:
        return {"error": f"Analysis aggregation failed: {e}"}

def create_visual_narrative(scenes, activities, colors, quality):
    """Create a narrative description of the visual content"""
    try:
        narrative_parts = []

        # Scene description
        if scenes:
            top_scene = scenes.most_common(1)[0][0]
            narrative_parts.append(f"The video primarily shows {top_scene} scenes")

        # Activity description  
        if activities:
            top_activity = activities.most_common(1)[0][0]
            narrative_parts.append(f"with {top_activity} activity levels")

        # Color description
        if colors:
            top_color = colors.most_common(1)[0][0]
            narrative_parts.append(f"featuring {top_color} color schemes")

        # Quality description
        quality_desc = 'excellent' if quality > 80 else 'good' if quality > 60 else 'fair' if quality > 40 else 'poor'
        narrative_parts.append(f"Video quality appears {quality_desc}")

        return '. '.join(narrative_parts) + '.'

    except Exception as e:
        return "Unable to generate visual narrative."

def identify_key_visual_moments(timeline_events):
    """Identify the most important visual moments"""
    try:
        key_moments = []

        # Scene changes are always key moments
        scene_changes = [event for event in timeline_events if event['frame_type'] == 'scene_change']
        key_moments.extend(scene_changes[:3])  # Top 3 scene changes

        # High activity moments
        high_activity = [event for event in timeline_events if event['activity_level'] == 'high']
        key_moments.extend(high_activity[:2])  # Top 2 high activity moments

        # Text appearance moments
        text_moments = [event for event in timeline_events if event['has_text']]
        key_moments.extend(text_moments[:2])  # Top 2 text moments

        # Remove duplicates and sort by timestamp
        unique_moments = []
        seen_timestamps = set()

        for moment in key_moments:
            if moment['timestamp'] not in seen_timestamps:
                unique_moments.append(moment)
                seen_timestamps.add(moment['timestamp'])

        return sorted(unique_moments, key=lambda x: x['timestamp'])[:5]  # Top 5 key moments

    except Exception as e:
        return []

# Helper functions
def estimate_color_temperature(r, g, b):
    """Estimate color temperature from RGB values"""
    if r > g and r > b:
        return 'warm'
    elif b > r and b > g:
        return 'cool'
    else:
        return 'neutral'

def classify_color_scheme(r, g, b):
    """Classify the color scheme"""
    if abs(r - g) < 20 and abs(g - b) < 20:
        return 'monochromatic'
    elif max(r, g, b) - min(r, g, b) > 100:
        return 'high_contrast'
    else:
        return 'balanced'

def format_timestamp(seconds):
    """Format seconds to MM:SS"""
    try:
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    except:
        return "00:00"
