
# test_video_analysis.py - Simple test script

import requests
import os

def test_video_analysis():
    """Test video analysis step by step"""

    print("🧪 Testing Video Analysis System...")

    # Test 1: Check if server is running
    try:
        response = requests.get('http://localhost:5000/health')
        print(f"✅ Server health: {response.json()}")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return

    # Test 2: Upload a video
    if not os.path.exists('test_video.mp4'):
        print("❌ No test video found. Please add a small MP4 file named 'test_video.mp4'")
        return

    try:
        files = {'video': open('test_video.mp4', 'rb')}
        upload_response = requests.post('http://localhost:5000/upload', files=files)
        print(f"📤 Upload response: {upload_response.status_code}")

        if upload_response.status_code == 200:
            upload_data = upload_response.json()
            print(f"✅ Upload successful: {upload_data['filename']}")

            # Test 3: Process video
            process_data = {
                'filepath': upload_data['filepath'],
                'preferences': {
                    'length': 'short',
                    'detail_level': 5,
                    'style': 'bullet_points',
                    'focus': ['visual_elements']
                }
            }

            print("🔄 Starting video processing...")
            process_response = requests.post(
                'http://localhost:5000/process-visual',
                json=process_data,
                timeout=120  # 2 minute timeout
            )

            print(f"📊 Process response: {process_response.status_code}")

            if process_response.status_code == 200:
                result = process_response.json()
                print("✅ Processing successful!")
                print(f"📋 Summary: {result['final_summary']['summary'][:200]}...")
            else:
                print(f"❌ Processing failed: {process_response.text}")

        else:
            print(f"❌ Upload failed: {upload_response.text}")

    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_video_analysis()
