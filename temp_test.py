print("✅ Script started")

from core.video_processor import extract_video_text

print("✅ Function imported")

result = extract_video_text("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

print("✅ Function executed")
print("OUTPUT:")
print(result)
