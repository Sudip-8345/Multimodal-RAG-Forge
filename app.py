import os
from config import DEFAULT_VIDEO_PATH, DEFAULT_OUTPUT_FOLDER, DEFAULT_AUDIO_PATH
from video_utils import download_video, video_to_images, video_to_audio
from audio_utils import audio_to_text, save_text_to_file
from index_utils import build_index
from retrieval_utils import create_retriever, retrieve, generate_answer
from visualization import plot_images

# Check if video is already downloaded
def is_video_downloaded(video_path):
    video_file = os.path.join(video_path, "input_vid.mp4")
    return os.path.exists(video_file)

# Check if frames are already extracted
def are_frames_extracted(output_folder):
    if not os.path.exists(output_folder):
        return False
    frames = [f for f in os.listdir(output_folder) if f.startswith("frame") and f.endswith(".png")]
    return len(frames) > 0

# Check if text is already extracted
def is_text_extracted(output_folder):
    text_file = os.path.join(output_folder, "output_text.txt")
    return os.path.exists(text_file)

# Process video: download, extract frames, extract audio, convert to text
def process_video(video_url, video_path=None, output_folder=None, audio_path=None, force=False):
    video_path = video_path or DEFAULT_VIDEO_PATH
    output_folder = output_folder or DEFAULT_OUTPUT_FOLDER
    audio_path = audio_path or DEFAULT_AUDIO_PATH
    os.makedirs(video_path, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    
    video_file = os.path.join(video_path, "input_vid.mp4")
    metadata = {}
    
    # Step 1: Download video
    if force or not is_video_downloaded(video_path):
        print("Step 1: Downloading video...")
        metadata = download_video(video_url, video_path)
        print(f"Video metadata: {metadata}")
    else:
        print("Step 1: Video already downloaded. Skipping...")
    
    # Step 2: Extract frames
    if force or not are_frames_extracted(output_folder):
        print("\nStep 2: Extracting frames from video...")
        video_to_images(video_file, output_folder)
    else:
        print("\nStep 2: Frames already extracted. Skipping...")
    
    # Step 3: Extract audio and convert to text
    if force or not is_text_extracted(output_folder):
        print("\nStep 3: Extracting audio from video...")
        video_to_audio(video_file, audio_path)
        
        print("\nStep 4: Converting audio to text...")
        text_data = audio_to_text(audio_path)
        text_file_path = os.path.join(output_folder, "output_text.txt")
        save_text_to_file(text_data, text_file_path)
    else:
        print("\nStep 3-4: Text already extracted. Skipping...")
        text_file_path = os.path.join(output_folder, "output_text.txt")
        with open(text_file_path, 'r', encoding='utf-8') as f:
            text_data = f.read()
    
    return metadata, text_data

# Create multimodal index
def create_video_index(output_folder=None):
    output_folder = output_folder or DEFAULT_OUTPUT_FOLDER
    print("Building multimodal index...")
    index = build_index(output_folder)
    print("Index created successfully!")
    return index

# Query the video
def query_video(index, query, metadata, show_images=True):
    retriever = create_retriever(index)
    print(f"Query: {query}")
    print("\nRetrieving relevant content...")
    images, texts = retrieve(retriever, query)
    print(f"Found {len(images)} relevant images and {len(texts)} text segments.")
    
    if show_images and images:
        print("\nRetrieved images:")
        plot_images(images)
    
    print("\nGenerating answer...")
    answer = generate_answer(query, texts, metadata, images)
    return answer

# Main function
def main():
    video_url = "https://www.youtube.com/watch?v=3dhcmeOTZ_Q"
    
    print("=" * 60)
    print("Video Processing RAG with LlamaIndex & LanceDB")
    print("=" * 60)
    
    print("\n--- PROCESSING VIDEO ---\n")
    metadata, text_data = process_video(video_url)
    
    print("\n--- CREATING INDEX ---\n")
    index = create_video_index()
    
    print("\n--- QUERYING VIDEO ---\n")
    query = "Can you tell me the name of the book shown in the video?"
    answer = query_video(index, query, metadata)
    
    print("\n" + "=" * 60)
    print("ANSWER:")
    print("=" * 60)
    print(answer)
    
    print("\n--- INTERACTIVE MODE ---")
    print("Enter your queries (type 'quit' to exit):")
    print("Add 'show' at end to display images (e.g., 'show me the book show')\n")
    
    while True:
        user_query = input("Your query: ").strip()
        if user_query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        if user_query:
            show_img = user_query.lower().endswith(' show')
            if show_img:
                user_query = user_query[:-5].strip()
            answer = query_video(index, user_query, metadata, show_images=show_img)
            print(f"\nAnswer: {answer}\n")

if __name__ == "__main__":
    main()