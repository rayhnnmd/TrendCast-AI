import os
import sys

# Force UTF-8 encoding for printing emojis on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv

# Load dotenv at the very top before any imports
load_dotenv()

from agents.news_fetcher import fetch_trending_news
from agents.trend_researcher import research_trends
from agents.script_writer import write_script
from agents.voiceover import generate_voiceover
from agents.video_assembler import assemble_video
from agents.background_fetcher import fetch_background_video

def run_pipeline():
    """
    Orchestrates the entire TrendForge AI pipeline: fetching news, researching trends,
    writing a script, generating voiceover, and assembling the video.
    """
    print("Starting TrendForge AI Pipeline...")
    
    # Step 1
    print("\n Step 1: fetch news")
    news_content = fetch_trending_news()
    print("Result:")
    print(news_content)
    if not news_content:
        print(" Failed to fetch news. Exiting pipeline.")
        sys.exit(1)
        
    # Step 2
    print("\n Step 2: extract first 6 words as topic, get trends")
    # Extract first 6 words safely
    words = news_content.split()
    topic = " ".join(words[:6]) if len(words) >= 6 else " ".join(words)
    print(f"Topic identified: {topic}")
    
    trend_data = research_trends(topic)
    print("Analysis:")
    print(trend_data.get('analysis', 'No analysis available'))
    
    # Step 3
    print("\n Step 3: write script")
    script = write_script(news_content, trend_data)
    print("Full Script:")
    print(script)
    if not script:
        print(" Failed to write script. Exiting pipeline.")
        sys.exit(1)
        
    category = topic

    print("\n🎥 Step 3.5: Fetching background video...")
    background_path = fetch_background_video(category)

    # Step 4
    print("\n Step 4: generate voiceover")
    audio_path = generate_voiceover(script)
    if not audio_path:
        print(" Voiceover generation failed. Exiting gracefully.")
        sys.exit(1)
        
    # Step 5
    print("\n Step 5: assemble video")
    video_path = assemble_video(
        script, 
        audio_path, 
        background_path=background_path,
        category=category
    )
    if not video_path:
        print(" Video assembly failed. Exiting pipeline.")
        sys.exit(1)
        
    print(f"Final Path: {video_path}")
    print("\n BIG SUCCESS! The AI news video has been fully generated! ")

if __name__ == "__main__":
    run_pipeline()
