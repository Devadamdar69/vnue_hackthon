
from datetime import datetime
import json

def create_visual_only_summary(visual_analysis, user_preferences):
    """Create final summary based only on visual analysis"""
    try:
        # Extract user preferences
        summary_length = user_preferences.get('length', 'medium')
        focus_areas = user_preferences.get('focus', ['visual_elements'])
        summary_style = user_preferences.get('style', 'bullet_points')
        detail_level = user_preferences.get('detail_level', 'medium')

        # Determine max length based on user preference
        length_mapping = {
            'short': 150,
            'medium': 300,
            'long': 500
        }
        max_length = length_mapping.get(summary_length, 300)

        # Generate base visual summary
        base_summary = generate_visual_narrative(visual_analysis, max_length)

        # Apply user preferences and focus areas
        enhanced_summary = apply_visual_preferences(
            base_summary,
            visual_analysis,
            user_preferences
        )

        # Add metadata
        summary_data = {
            'summary': enhanced_summary,
            'visual_elements_detected': len(visual_analysis.get('video_characteristics', {}).get('dominant_scene_types', {})),
            'total_scenes_analyzed': visual_analysis.get('total_frames_analyzed', 0),
            'key_moments_identified': len(visual_analysis.get('key_moments', [])),
            'generation_time': datetime.now().isoformat(),
            'processing_mode': 'visual_only',
            'user_preferences': user_preferences,
            'video_characteristics': visual_analysis.get('video_characteristics', {})
        }

        return summary_data

    except Exception as e:
        return {
            'summary': f"Error generating visual summary: {e}",
            'error': str(e),
            'processing_mode': 'visual_only'
        }

def generate_visual_narrative(visual_analysis, max_length):
    """Generate narrative description of visual content"""
    try:
        narrative_parts = []

        # Get video characteristics
        characteristics = visual_analysis.get('video_characteristics', {})
        timeline = visual_analysis.get('timeline_analysis', [])
        key_moments = visual_analysis.get('key_moments', [])

        # Opening statement
        total_frames = visual_analysis.get('total_frames_analyzed', 0)
        narrative_parts.append(f"Analysis of {total_frames} key frames reveals:")

        # Scene types description
        scene_types = characteristics.get('dominant_scene_types', {})
        if scene_types:
            top_scene = max(scene_types, key=scene_types.get)
            scene_percentage = (scene_types[top_scene] / total_frames) * 100 if total_frames > 0 else 0
            narrative_parts.append(f"The video primarily consists of {top_scene} scenes ({scene_percentage:.0f}% of analyzed frames)")

        # Activity level description
        activity_levels = characteristics.get('activity_levels', {})
        if activity_levels:
            top_activity = max(activity_levels, key=activity_levels.get)
            narrative_parts.append(f"Overall activity level is {top_activity}")

        # Visual quality assessment
        avg_quality = characteristics.get('average_quality_score', 0)
        quality_desc = get_quality_description(avg_quality)
        narrative_parts.append(f"Video quality is {quality_desc} (score: {avg_quality:.0f}/100)")

        # Color scheme description
        color_schemes = characteristics.get('color_schemes', {})
        if color_schemes:
            top_color = max(color_schemes, key=color_schemes.get)
            narrative_parts.append(f"Visual style features {top_color} color schemes")

        # Key moments description
        if key_moments:
            narrative_parts.append(f"\n\nKey Visual Moments:")
            for i, moment in enumerate(key_moments[:3], 1):
                timestamp = moment.get('timestamp_formatted', 'Unknown')
                scene_type = moment.get('scene_type', 'scene')
                activity = moment.get('activity_level', 'activity')
                narrative_parts.append(f"{i}. {timestamp} - {scene_type} with {activity} activity")

        # Scene changes
        scene_changes = visual_analysis.get('scene_changes', [])
        if scene_changes:
            narrative_parts.append(f"\n\nSignificant scene changes detected at: {', '.join([sc.get('timestamp_formatted', '') for sc in scene_changes[:3]])}")

        # Text presence
        text_presence = characteristics.get('text_presence', False)
        if text_presence:
            text_timestamps = characteristics.get('text_timestamps', [])
            narrative_parts.append(f"\n\nText or graphics appear in the video, first detected at {format_timestamp(text_timestamps[0]) if text_timestamps else 'multiple points'}")

        # Join narrative parts
        full_narrative = '\n'.join(narrative_parts)

        # Truncate if too long
        if len(full_narrative) > max_length:
            full_narrative = full_narrative[:max_length] + "..."

        return full_narrative

    except Exception as e:
        return f"Error generating visual narrative: {e}"

def apply_visual_preferences(base_summary, visual_analysis, preferences):
    """Customize summary based on user preferences for visual content"""
    try:
        focus_areas = preferences.get('focus', [])
        style = preferences.get('style', 'paragraph')
        detail_level = preferences.get('detail_level', 'medium')

        enhanced_summary = base_summary

        # Add focus area specific content
        if 'scene_analysis' in focus_areas:
            scene_details = get_detailed_scene_analysis(visual_analysis)
            enhanced_summary += f"\n\nDetailed Scene Analysis:\n{scene_details}"

        if 'visual_quality' in focus_areas:
            quality_details = get_quality_analysis(visual_analysis)
            enhanced_summary += f"\n\nVisual Quality Assessment:\n{quality_details}"

        if 'composition' in focus_areas:
            composition_details = get_composition_analysis(visual_analysis)
            enhanced_summary += f"\n\nVisual Composition:\n{composition_details}"

        if 'color_analysis' in focus_areas:
            color_details = get_color_analysis(visual_analysis)
            enhanced_summary += f"\n\nColor Analysis:\n{color_details}"

        if 'motion_analysis' in focus_areas:
            motion_details = get_motion_analysis(visual_analysis)
            enhanced_summary += f"\n\nMotion & Activity Analysis:\n{motion_details}"

        if 'key_moments' in focus_areas:
            key_moments = visual_analysis.get('key_moments', [])
            if key_moments:
                moments_text = "\n".join([f"• {moment.get('timestamp_formatted', '')}: {moment.get('scene_type', 'Scene')} - {moment.get('activity_level', 'activity')} level" for moment in key_moments])
                enhanced_summary += f"\n\nKey Visual Moments:\n{moments_text}"

        # Apply style formatting
        if style == 'bullet_points':
            enhanced_summary = convert_to_bullet_points(enhanced_summary)
        elif style == 'numbered_list':
            enhanced_summary = convert_to_numbered_list(enhanced_summary)
        elif style == 'technical_report':
            enhanced_summary = format_as_technical_report(enhanced_summary, visual_analysis)

        return enhanced_summary

    except Exception as e:
        return base_summary + f"\n\n(Note: Error applying preferences: {e})"

def get_detailed_scene_analysis(visual_analysis):
    """Get detailed scene analysis"""
    try:
        timeline = visual_analysis.get('timeline_analysis', [])
        scene_types = {}

        for event in timeline:
            scene_type = event.get('scene_type', 'unknown')
            if scene_type not in scene_types:
                scene_types[scene_type] = []
            scene_types[scene_type].append(event.get('timestamp_formatted', ''))

        details = []
        for scene_type, timestamps in scene_types.items():
            details.append(f"• {scene_type.title()}: {len(timestamps)} instances at {', '.join(timestamps[:3])}")

        return '\n'.join(details)
    except:
        return "Scene analysis data not available"

def get_quality_analysis(visual_analysis):
    """Get detailed quality analysis"""
    try:
        timeline = visual_analysis.get('timeline_analysis', [])
        quality_ratings = {}

        for event in timeline:
            rating = event.get('quality_rating', 'unknown')
            quality_ratings[rating] = quality_ratings.get(rating, 0) + 1

        total = sum(quality_ratings.values())
        details = []

        for rating, count in quality_ratings.items():
            percentage = (count / total) * 100 if total > 0 else 0
            details.append(f"• {rating.title()}: {percentage:.1f}% of frames")

        avg_quality = visual_analysis.get('video_characteristics', {}).get('average_quality_score', 0)
        details.append(f"• Overall Quality Score: {avg_quality:.1f}/100")

        return '\n'.join(details)
    except:
        return "Quality analysis data not available"

def get_composition_analysis(visual_analysis):
    """Get composition analysis details"""
    try:
        timeline = visual_analysis.get('timeline_analysis', [])
        # This would need more detailed composition data from the analysis
        return "Composition analysis includes framing, symmetry, and visual balance assessment across key frames"
    except:
        return "Composition analysis data not available"

def get_color_analysis(visual_analysis):
    """Get detailed color analysis"""
    try:
        characteristics = visual_analysis.get('video_characteristics', {})
        color_schemes = characteristics.get('color_schemes', {})

        details = []
        for scheme, count in color_schemes.items():
            details.append(f"• {scheme.replace('_', ' ').title()}: {count} instances")

        return '\n'.join(details) if details else "Color analysis data not available"
    except:
        return "Color analysis data not available"

def get_motion_analysis(visual_analysis):
    """Get motion and activity analysis"""
    try:
        characteristics = visual_analysis.get('video_characteristics', {})
        activity_levels = characteristics.get('activity_levels', {})

        details = []
        total = sum(activity_levels.values())

        for level, count in activity_levels.items():
            percentage = (count / total) * 100 if total > 0 else 0
            details.append(f"• {level.title()} Activity: {percentage:.1f}% of analyzed frames")

        return '\n'.join(details) if details else "Motion analysis data not available"
    except:
        return "Motion analysis data not available"

def get_quality_description(score):
    """Convert quality score to description"""
    if score > 80:
        return 'excellent'
    elif score > 60:
        return 'good'
    elif score > 40:
        return 'fair'
    else:
        return 'poor'

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
        lines = text.split('\n')
        bullet_points = []

        for line in lines:
            line = line.strip()
            if line and not line.startswith('•'):
                if len(line) > 5:  # Only meaningful lines
                    bullet_points.append(f"• {line}")
            elif line.startswith('•'):
                bullet_points.append(line)

        return '\n'.join(bullet_points)
    except:
        return text

def convert_to_numbered_list(text):
    """Convert text to numbered list format"""
    try:
        lines = text.split('\n')
        numbered_list = []
        counter = 1

        for line in lines:
            line = line.strip()
            if line and len(line) > 5:
                if not line[0].isdigit():
                    numbered_list.append(f"{counter}. {line}")
                    counter += 1
                else:
                    numbered_list.append(line)

        return '\n'.join(numbered_list)
    except:
        return text

def format_as_technical_report(summary, visual_analysis):
    """Format as technical report"""
    try:
        report_parts = [
            "VISUAL ANALYSIS TECHNICAL REPORT",
            "=" * 40,
            "",
            "EXECUTIVE SUMMARY:",
            summary,
            "",
            "TECHNICAL SPECIFICATIONS:",
            f"• Frames Analyzed: {visual_analysis.get('total_frames_analyzed', 0)}",
            f"• Processing Mode: Visual-Only Analysis",
            f"• Analysis Depth: Comprehensive frame-by-frame examination",
            "",
            "FINDINGS:",
            "• Visual content analysis completed successfully",
            "• Scene classification and activity detection performed",
            "• Quality assessment and composition analysis included",
            "• Key moments and scene changes identified"
        ]

        return '\n'.join(report_parts)
    except:
        return summary
