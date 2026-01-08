import os
from openai import OpenAI, RateLimitError, APIError, AuthenticationError
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_video_summary_and_flashcards(video_url: str) -> tuple[str, list]:
    prompt = f"""
You are given a YouTube video URL.

URL:
{video_url}

Task:
1. Generate a high-level summary of what this video is likely about.
2. Generate 5–7 educational flashcards (question and answer format).
3. Do NOT claim you watched or accessed the video.
4. Be clear that this is an inferred summary.

Return output in this format:

SUMMARY:
<summary>

FLASHCARDS:
Q: ...
A: ...
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        content = response.choices[0].message.content.strip()

        if "FLASHCARDS:" not in content:
            raise ValueError("Unexpected response format")

        summary_part, flashcard_part = content.split("FLASHCARDS:")

        summary = summary_part.replace("SUMMARY:", "").strip()

        flashcards = []
        for line in flashcard_part.strip().split("\n"):
            if line.startswith("Q:"):
                flashcards.append(
                    {"question": line.replace("Q:", "").strip(), "answer": ""}
                )
            elif line.startswith("A:") and flashcards:
                flashcards[-1]["answer"] = line.replace("A:", "").strip()

        return summary, flashcards

    # 🔴 QUOTA / BILLING
    except RateLimitError:
        return (
            "⚠️ OpenAI API quota exceeded.\n\n"
            "Please check your billing or try again later.",
            []
        )

    # 🔴 AUTH / KEY ISSUES
    except AuthenticationError:
        return (
            "❌ Invalid OpenAI API key.\n\n"
            "Please check your .env configuration.",
            []
        )

    # 🔴 OPENAI SERVER ISSUES
    except APIError:
        return (
            "⚠️ OpenAI service is temporarily unavailable.\n\n"
            "Please try again later.",
            []
        )

    # 🔴 FORMAT / UNEXPECTED
    except Exception as e:
        return (
            f"❌ Failed to generate video output.\n\nError: {str(e)}",
            []
        )
