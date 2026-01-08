import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)

# -------------------------------------------------
# Validate transcript quality
# -------------------------------------------------
def is_valid_text(text: str) -> bool:
    if not text:
        return False
    if len(text.split()) < 200:
        return False
    bad_markers = ["cnn.com", "ireport", "submit your photos"]
    if any(b in text.lower() for b in bad_markers):
        return False
    return True


# -------------------------------------------------
# MAIN FUNCTION (TRANSCRIPT ONLY)
# -------------------------------------------------
def extract_video_text(video_url: str) -> str:
    """
    Extract YouTube transcript ONLY.
    No audio download.
    No Whisper.
    Ultra-fast.
    """

    try:
        match = re.search(r"(?:v=|youtu.be/)([^&]+)", video_url)
        if not match:
            return "❌ Invalid YouTube URL"

        video_id = match.group(1)

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join(seg["text"] for seg in transcript)

        if not is_valid_text(text):
            return "❌ Transcript too short or low quality"

        return text

    except TranscriptsDisabled:
        return "❌ Transcripts are disabled for this video"
    except NoTranscriptFound:
        return "❌ No transcript available for this video"
    except VideoUnavailable:
        return "❌ Video unavailable"
    except Exception as e:
        return f"❌ Failed to extract transcript: {e}"
