import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents.news_fetcher import fetch_top_news
from agents.script_writer import write_script
from agents.image_fetcher import fetch_images
from agents.background_generator import generate_background_video
from agents.voiceover import generate_voiceover
from agents.video_assembler import assemble_video
from agents.social_publisher import generate_social_caption, schedule_post

def print_banner():
    banner = r"""
===================================================
  _______                 _  _____           _   
 |__   __|               | |/ ____|         | |  
    | | ___ _ __   __ _  | | |     __ _ ___| |_ 
    | |/ _ \ '_ \ / _` | | | |    / _` / __| __|
    | |  __/ | | | (_| | | | |___| (_| \__ \ |_ 
    |_|\___|_| |_|\__,_| |_|\_____\__,_|___/\__|
                                                 
               TrendCast AI Pipeline
===================================================
    """
    print(banner)

def main():
    print_banner()
    
    print("Select your news genre:\n")
    print("1. Technology")
    print("2. Politics")
    print("3. Business")
    print("4. Sports")
    print("5. Science")
    print("6. Entertainment")
    print("7. World News")
    
    choice = input("\nEnter number (1-7): ").strip()
    print(f"DEBUG: You entered '{choice}'")
    
    genre_map = {
        "1": "Technology",
        "2": "Politics",
        "3": "Business",
        "4": "Sports",
        "5": "Science",
        "6": "Entertainment",
        "7": "World News"
    }
    
    genre = genre_map.get(choice)
    if not genre:
        print("[ERROR] Invalid selection. Exiting.")
        sys.exit(1)
        
    print(f"\nStarting pipeline for: {genre}")
    
    # Step 1: Fetch News
    print("\n[STEP 1] Fetching top news...")
    news_content = fetch_top_news(genre)
    if not news_content:
        print("[ERROR] Pipeline failed at Step 1.")
        sys.exit(1)
    print("News Content:\n")
    print(news_content)
    
    # Step 2: Write Script
    print("\n[STEP 2] Writing script...")
    script = write_script(news_content, genre)
    if not script:
        print("[ERROR] Pipeline failed at Step 2.")
        sys.exit(1)
    print("Script:\n")
    print(script)
    
    # Step 3: Fetch Images
    print("\n[STEP 3] Fetching images...")
    image_paths = fetch_images(genre)
    if not image_paths:
        print("[ERROR] Pipeline failed at Step 3 (No images found).")
        sys.exit(1)
    print(f"Downloaded {len(image_paths)} images.")
    
    # Step 4: Generating Voiceover
    print("\n[STEP 4] Generating voiceover...")
    audio_path = generate_voiceover(script)
    if not audio_path:
        print("[ERROR] Pipeline failed at Step 4.")
        sys.exit(1)
    
    # Get audio duration
    from moviepy.editor import AudioFileClip
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    print(f"Voiceover generated: {audio_path} (Duration: {audio_duration:.2f}s)")
    
    # Step 5: Generating Background Video
    print("\n[STEP 5] Generating background video...")
    background_path = generate_background_video(image_paths, audio_duration)
    if not background_path:
        print("[WARNING] Background generation failed, using fallback.")
    else:
        print(f"Background video generated: {background_path}")
        
    # Step 6: Assembling Final Video
    print("\n[STEP 6] Assembling final video...")
    final_video_path = assemble_video(script, audio_path, background_path)
    if not final_video_path:
        print("[ERROR] Pipeline failed at Step 6.")
        sys.exit(1)
        
    print(f"\n[DONE] Video saved to: {final_video_path}")

    # Step 7: Social Publishing & Scheduling
    print("\n[STEP 7] Preparing for social media...")
    caption = generate_social_caption(script)
    print("\nGenerated AI Caption for social media:\n")
    print("-" * 30)
    try:
        print(caption)
    except UnicodeEncodeError:
        print(caption.encode('ascii', 'ignore').decode('ascii'))
    print("-" * 30)
    
    choice = input("\nWould you like to schedule this post? (y/n): ").strip().lower()
    if choice == 'y':
        platform = input("Enter platform (YouTube/TikTok/Instagram) [default: YouTube]: ").strip() or "YouTube"
        sched_time = input("Enter schedule time (YYYY-MM-DD HH:MM) [leave blank for now]: ").strip()
        
        success = schedule_post(final_video_path, caption, platform, sched_time)
        if success:
            print(f"\n[SUCCESS] Post scheduled for {platform}!")
            print(f"Details saved to: output/scheduler/pending_posts.json")
        else:
            print("\n[ERROR] Failed to schedule post.")
    else:
        print("\nSkipping social media scheduling.")

if __name__ == "__main__":
    main()
