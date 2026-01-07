import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def extract_video_id(url):
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"embed/([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None

def extract_video_text(url):
    video_id = extract_video_id(url)

    if not video_id:
        return "Invalid YouTube URL."

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return "No transcript found for this video."
    except Exception as e:
        return f"Transcript error: {str(e)}"

    return " ".join([item["text"] for item in transcript])
