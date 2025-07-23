import os
import re
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from together import Together

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
client = Together(api_key=TOGETHER_API_KEY)

# Helper to extract video ID
def get_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# Chunk text into ~1000 words each
def chunk_text(text, max_words=1000):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])

# Main summarization function
def summarize_transcript(video_url):
    video_id = get_video_id(video_url)
    if not video_id:
        return "Invalid YouTube URL."

    try:
        # Initialize API
        ytt_api = YouTubeTranscriptApi()

        # Fetch transcript prioritizing English then Hindi
        transcript = None
        try:
            # Try English first
            fetched_transcript = ytt_api.fetch(video_id, languages=['en'])
            language_used = "English"
        except Exception as e_en:
            print("English transcript not available, trying Hindi...")
            try:
                # Try Hindi
                fetched_transcript = ytt_api.fetch(video_id, languages=['hi'])
                language_used = "Hindi"
            except Exception as e_hi:
                print("Neither English nor Hindi transcript available.")
                return f"Error fetching transcript: {e_hi}"

        # Convert fetched_transcript to text
        full_text = " ".join([snippet.text for snippet in fetched_transcript])

        # Split text into manageable chunks (each chunk ~1000 words)
        chunks = list(chunk_text(full_text, max_words=1000))

        summaries = []
        for idx, chunk in enumerate(chunks):
            response = client.chat.completions.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                messages=[
                    {"role": "system", "content": "You are a helpful summarizer."},
                    {"role": "user", "content": f"Summarize the following YouTube {language_used} transcript chunk clearly:\n\n{chunk}"}
                ],
                temperature=0.6
            )
            summary_chunk = response.choices[0].message.content
            summaries.append(summary_chunk)

        # Combine all chunk summaries into one text
        combined_summary = " ".join(summaries)

        # Perform final summarization if combined summary is still large
        if len(combined_summary.split()) > 1000:
            response = client.chat.completions.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                messages=[
                    {"role": "system", "content": "You are a helpful summarizer."},
                    {"role": "user", "content": f"Provide a concise summary of the following combined summaries:\n\n{combined_summary}"}
                ],
                temperature=0.6
            )
            combined_summary = response.choices[0].message.content

        return combined_summary

    except Exception as e:
        return f"Error summarizing transcript: {str(e)}"