import requests
import os

CATEGORY_KEYWORDS = {
    "global world news": "world city aerial",
    "war conflict military news": "military army soldiers",
    "gaming video games news": "gaming setup controller",
    "finance markets stocks economy news": "stock market trading",
    "technology AI tech news": "technology digital futuristic",
    "sports news": "sports stadium crowd",
    "entertainment celebrity movies news": "entertainment lights stage",
    "science space discovery news": "science space laboratory",
    "politics government news": "government capitol building",
    "climate environment nature news": "nature environment earth"
}

def fetch_background_video(category, output_path="output/background.mp4"):
    """
    Fetches relevant stock video from Pexels based on news category.
    Returns output_path on success, None on failure.
    """
    try:
        api_key = os.getenv("PEXELS_API_KEY")
        keyword = CATEGORY_KEYWORDS.get(category, "world news city")
        
        headers = {"Authorization": api_key}
        url = f"https://api.pexels.com/videos/search?query={keyword}&per_page=5&orientation=portrait"
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        videos = data.get("videos", [])
        if not videos:
            print("⚠️ No background video found, using color background")
            return None
        
        # Get the best quality video file
        video = videos[0]
        video_files = sorted(
            video["video_files"],
            key=lambda x: x.get("height", 0),
            reverse=True
        )
        
        video_url = video_files[0]["link"]
        
        print(f"🎥 Downloading background video...")
        video_response = requests.get(video_url, stream=True)
        
        os.makedirs("output", exist_ok=True)
        with open(output_path, "wb") as f:
            for chunk in video_response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Background video saved")
        return output_path
        
    except Exception as e:
        print(f"❌ Background fetch failed: {e}")
        return None
