from youtube_transcript_api import YouTubeTranscriptApi

# Extract transcript from YouTube video
def extract_transcript_details(yt_video_url):
    try:
        ytt_api = YouTubeTranscriptApi()
        video_id = yt_video_url.split("=")[1]
        transcript_text = ytt_api.fetch(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i.text
        return transcript
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
