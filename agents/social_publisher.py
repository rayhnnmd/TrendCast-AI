import os
import json
from datetime import datetime
from google import genai
from google.genai import types

def generate_social_caption(script):
    """
    Uses Gemini to generate a catchy social media caption with hashtags based on the video script.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Check out today's top news! #TrendCast #News #AI"

        client = genai.Client(api_key=api_key)
        
        prompt = f"""
Based on this video script, write a viral social media caption for TikTok/Instagram/YouTube Shorts.
Include:
- A catchy hook
- 3-4 bullet points summarizing the key news
- A call to action (like 'Follow for more')
- 5 relevant trending hashtags
- Some emojis to make it look human

SCRIPT:
{script}

Caption:
"""
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"[WARNING] Could not generate AI caption: {e}")
        return "New update from TrendCast AI! #News #AI #Trending"

def schedule_post(video_path, caption, platform="YouTube", schedule_time=None):
    """
    Saves the video and caption to a local scheduler file.
    """
    try:
        os.makedirs("output/scheduler", exist_ok=True)
        scheduler_file = "output/scheduler/pending_posts.json"
        
        posts = []
        if os.path.exists(scheduler_file):
            with open(scheduler_file, "r") as f:
                posts = json.load(f)
        
        new_post = {
            "id": len(posts) + 1,
            "video_path": video_path,
            "caption": caption,
            "platform": platform,
            "schedule_time": schedule_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "scheduled",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        posts.append(new_post)
        
        with open(scheduler_file, "w") as f:
            json.dump(posts, f, indent=4)
            
        return True
    except Exception as e:
        print(f"[ERROR] Scheduling failed: {e}")
        return False

def list_pending_posts():
    """
    Utility to see what's in the queue.
    """
    scheduler_file = "output/scheduler/pending_posts.json"
    if not os.path.exists(scheduler_file):
        return []
    with open(scheduler_file, "r") as f:
        return json.load(f)

# Note: Real YouTube/TikTok upload logic would require OAuth tokens.
# We have provided the foundation for it here.
