
import requests
import json
from datetime import datetime

def summarize_with_huggingface_free(text, max_length=150):
    """Use Hugging Face free inference API"""
    try:
        # Hugging Face free inference API
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

        # You can use without API key but with rate limits
        # Or sign up for free account and get API key for better limits
        headers = {}

        # Uncomment and add your HF API key for better performance
        # headers = {"Authorization": "Bearer your_huggingface_api_key"}

        payload = {
            "inputs": text,
            "parameters": {
                "max_length": max_length,
                "min_length": 30,
                "do_sample": False
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('summary_text', text[:max_length])

        # Fallback to local summarization
        return summarize_local_simple(text, max_length)

    except Exception as e:
        print(f"Hugging Face API error: {e}")
        return summarize_local_simple(text, max_length)

def summarize_local_simple(text, max_length=150):
    """Simple local summarization (completely free)"""
    try:
        sentences = text.split('. ')
        if len(sentences) <= 3:
            return text

        # Simple extractive summarization
        # Score sentences by frequency of words
        words = text.lower().split()
        word_freq = {}

        for word in words:
            word = word.strip('.,!?";')
            if len(word) > 3:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1

        # Score sentences
        sentence_scores = []
        for sentence in sentences:
            score = 0
            words_in_sentence = sentence.lower().split()
            for word in words_in_sentence:
                word = word.strip('.,!?";')
                score += word_freq.get(word, 0)

            if len(words_in_sentence) > 0:
                sentence_scores.append((sentence, score / len(words_in_sentence)))

        # Sort by score and take top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = sentence_scores[:3]

        summary = '. '.join([sent[0] for sent in top_sentences])

        # Truncate if too long
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."

        return summary

    except Exception as e:
        return text[:max_length] + "..." if len(text) > max_length else text

def create_final_summary(transcript, visual_analysis, user_preferences):
    """Combine transcript and visual analysis into final summary"""
    try:
        # Extract user preferences
        summary_length = user_preferences.get('length', 'medium')
        focus_areas = user_preferences.get('focus', [])
        summary_style = user_preferences.get('style', 'bullet_points')

        # Determine max length based on user preference
        length_mapping = {
            'short': 100,
            'medium': 200,
            'long': 400
        }
        max_length = length_mapping.get(summary_length, 200)

        # Create combined content for summarization
        combined_content = f"Transcript: {transcript}\n\n"

        if visual_analysis and not visual_analysis.get('error'):
            visual_summary = visual_analysis.get('visual_summary', '')
            top_elements = visual_analysis.get('top_visual_elements', [])

            combined_content += f"Visual Content: {visual_summary}\n"
            if top_elements:
                combined_content += f"Key visual elements: {', '.join(top_elements[:5])}\n\n"

        # Generate base summary
        base_summary = summarize_with_huggingface_free(combined_content, max_length)

        # Apply user preferences
        final_summary = apply_user_preferences(
            base_summary, 
            visual_analysis, 
            transcript,
            user_preferences
        )

        # Add metadata
        summary_data = {
            'summary': final_summary,
            'transcript_length': len(transcript.split()) if transcript else 0,
            'visual_elements_detected': len(visual_analysis.get('top_visual_elements', [])) if visual_analysis else 0,
            'generation_time': datetime.now().isoformat(),
            'user_preferences': user_preferences
        }

        return summary_data

    except Exception as e:
        return {
            'summary': f"Error generating summary: {e}",
            'error': str(e)
        }

def apply_user_preferences(base_summary, visual_analysis, transcript, preferences):
    """Customize summary based on user preferences"""
    try:
        focus_areas = preferences.get('focus', [])
        style = preferences.get('style', 'paragraph')

        enhanced_summary = base_summary

        # Add focus area specific content
        if 'key_points' in focus_areas:
            key_points = extract_key_points(transcript)
            enhanced_summary += f"\n\nKey Points:\n{key_points}"

        if 'visual_elements' in focus_areas and visual_analysis:
            visual_elements = visual_analysis.get('top_visual_elements', [])[:3]
            if visual_elements:
                enhanced_summary += f"\n\nMain Visual Elements: {', '.join(visual_elements)}"

        if 'timestamps' in focus_areas and visual_analysis:
            scene_changes = visual_analysis.get('scene_changes', [])[:3]
            if scene_changes:
                enhanced_summary += "\n\nKey Moments:"
                for scene in scene_changes:
                    timestamp = format_timestamp(scene.get('timestamp', 0))
                    enhanced_summary += f"\n- {timestamp}: Scene change detected"

        # Apply style formatting
        if style == 'bullet_points':
            enhanced_summary = convert_to_bullet_points(enhanced_summary)
        elif style == 'numbered_list':
            enhanced_summary = convert_to_numbered_list(enhanced_summary)

        return enhanced_summary

    except Exception as e:
        return base_summary + f"\n\n(Note: Error applying preferences: {e})"

def extract_key_points(transcript):
    """Extract key points from transcript"""
    try:
        sentences = transcript.split('. ')
        # Simple heuristic: sentences with question words or emphasis
        key_indicators = ['important', 'key', 'main', 'first', 'second', 'finally', 'conclusion']

        key_sentences = []
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in key_indicators):
                key_sentences.append(sentence.strip())

        return '\n'.join([f"• {point}" for point in key_sentences[:5]])

    except Exception as e:
        return "Unable to extract key points"

def format_timestamp(seconds):
    """Format seconds to MM:SS"""
    try:
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    except:
        return "00:00"

def convert_to_bullet_points(text):
    """Convert text to bullet point format"""
    try:
        sentences = text.split('. ')
        bullet_points = []

        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:
                bullet_points.append(f"• {sentence}")

        return '\n'.join(bullet_points)

    except Exception as e:
        return text

def convert_to_numbered_list(text):
    """Convert text to numbered list format"""
    try:
        sentences = text.split('. ')
        numbered_list = []

        for i, sentence in enumerate(sentences, 1):
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:
                numbered_list.append(f"{i}. {sentence}")

        return '\n'.join(numbered_list)

    except Exception as e:
        return text
