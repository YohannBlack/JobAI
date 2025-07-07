from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_profile_summary(extracted_text):
    max_input_length = 1024
    if len(extracted_text) > max_input_length:
        extracted_text = extracted_text[:max_input_length]

    summary = summarizer(
        extracted_text,
        max_length=150,
        min_length=40,
        do_sample=False
    )

    return summary[0]["summary_text"]
