from transformers import pipeline

# Load once (important for performance)
summarizer = pipeline(
    "summarization",
    model="t5-small",
    tokenizer="t5-small"
)

def generate_summary(text, max_len=150, min_len=50):
    summary = summarizer(
        text,
        max_length=max_len,
        min_length=min_len,
        do_sample=False
    )
    return summary[0]['summary_text']
