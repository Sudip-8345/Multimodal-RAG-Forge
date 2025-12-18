# Video Processing RAG with LlamaIndex and LanceDB

A simple RAG (Retrieval Augmented Generation) application that processes YouTube videos and allows you to ask questions about the video content using text and images.

## What it does

1. Downloads a YouTube video
2. Extracts frames (images) from the video
3. Extracts audio and converts it to text using Whisper
4. Creates a multimodal vector index using LlamaIndex and LanceDB
5. Allows you to query the video content and get answers from Gemini AI

## Tech Stack

- Python 3.12
- LlamaIndex - for building the RAG pipeline
- LanceDB - vector database for storing embeddings
- FastEmbed - for text embeddings (lightweight alternative to transformers)
- CLIP - for image embeddings
- Google Gemini - for generating answers
- yt-dlp - for downloading YouTube videos
- MoviePy - for video processing (extracting frames and audio)
- Whisper (via SpeechRecognition) - for audio to text conversion

## Project Structure

```
RAG/
├── app.py              # Main application
├── config.py           # Configuration and API keys
├── video_utils.py      # Video download and processing
├── audio_utils.py      # Audio to text conversion
├── index_utils.py      # LlamaIndex and LanceDB setup
├── retrieval_utils.py  # Query and answer generation
├── visualization.py    # Image display utilities
├── transcript_utils.py # YouTube transcript extraction
├── requirements.txt    # Dependencies
└── README.md
```

## Setup

1. Create a virtual environment:
```bash
python -m venv myenv
myenv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install git+https://github.com/openai/CLIP.git
```

3. Set your Google API key in config.py:
```python
GOOGLE_API_KEY = "your-api-key-here"
```

4. Run the application:
```bash
python app.py
```

## Usage

After running app.py, the application will:
- Download and process the video (first run only)
- Build the vector index
- Enter interactive mode where you can ask questions

Example queries:
```
Your query: what is the main topic of this video
Your query: show me the book image show
Your query: quit
```

Add "show" at the end of your query to display relevant images.

## Results

The application successfully:
- Downloads YouTube videos and extracts frames at 0.1 fps
- Converts audio to text using Whisper
- Creates a multimodal index that can search both text and images
- Retrieves relevant content and generates answers using Gemini

Sample output:
```
Query: what is the video about
Found 5 relevant images and 1 text segments.
Generating answer...
Answer: The video is about...
```

## Challenges Faced

1. Gemini API rate limits - The free tier has limited requests per minute. Sometimes the API returns empty responses when the limit is reached. Added error handling to catch these cases.

2. Long processing time - First run takes significant time because:
   - Downloading video from YouTube
   - Extracting frames from video
   - Converting audio to text with Whisper
   - Building the vector index with embeddings
   
   Solution: Added caching so subsequent runs skip already processed data.

3. FFmpeg dependency - yt-dlp requires FFmpeg to merge video and audio streams. Worked around this by downloading pre-muxed formats that dont require merging.

4. Heavy dependencies - The transformers library is very large and takes long to install. Switched to FastEmbed which uses ONNX and is much lighter.

5. CLIP installation - The llama-index-embeddings-clip package requires installing OpenAI CLIP separately from GitHub.

6. Empty Gemini responses - Sometimes Gemini returns empty responses for certain queries. Added try-catch blocks to handle this gracefully.

## Limitations

- Works best with videos that have clear audio
- Image retrieval depends on CLIP embeddings which may not always find the most relevant frames
- Gemini API has rate limits on the free tier
- First run processing can take several minutes depending on video length

## Future Improvements

- Add support for multiple videos
- Implement persistent index storage
- Add support for local LLMs to avoid API limits
- Improve frame extraction with scene detection
- Add video timestamp references in answers
