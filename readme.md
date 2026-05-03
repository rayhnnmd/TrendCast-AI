# TrendCast-AI

## Overview
TrendCast-AI automates the process of creating short news videos from trending stories. Instead of manually fetching news, sourcing images, recording voiceovers, editing video, and uploading content, this project builds a complete end-to-end pipeline that handles those steps automatically.

## Use Case
Users typically need to:
- Manually fetch trending news and research topics
- Write a video script
- Find and download relevant images or video backgrounds
- Generate or record a voiceover
- Assemble the final video with audio and visuals
- Upload or schedule the video for social platforms

TrendCast-AI solves this by automating the entire workflow:
1. Fetch trending news for a selected genre
2. Generate a 60-second script from the news
3. Collect images for visual storytelling
4. Produce a voiceover automatically
5. Create a background video and assemble the final edit
6. Generate social captions and schedule posts

## What the project does
- Fetches top news by genre using automated agents
- Writes an AI-generated script from the news summary
- Downloads images for the selected topic
- Creates a voiceover from the script using AI audio tools
- Builds a background video and assembles the final video with audio
- Prepares social media captions and saves scheduling data

## Benefits
- Saves time by removing manual video production steps
- Enables creators to publish trend-driven video content faster
- Standardizes the workflow for news-based social media videos
- Integrates voice, visuals, and social publishing preparation

## How to Run
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create and configure your `.env` based on `.env.example`
4. Run the Flask app:
   ```bash
   python app.py
   ```
5. Or run the CLI pipeline directly:
   ```bash
   python main.py
   ```

## Project Structure
- `app.py` - Flask server and asynchronous video pipeline
- `main.py` - CLI-driven pipeline runner
- `agents/` - Modular pipeline components for news, script, images, audio, video, and social publishing
- `output/` - Generated audio, video, and scheduler data

## Demo Video
A demo of this automated workflow is available here:

* Demo video is [here](https://drive.google.com/file/d/1Mug-l0V5OKrRSgI3OzZOQDP9cDGAc57J/view?usp=sharing)


## Notes
- Make sure `ffmpeg` is installed and available on your system path for video processing.
- The app currently provides a YouTube integration placeholder and plans for additional social platforms.
- If you want to use the web UI, navigate to `http://localhost:5000/` after starting `app.py`.

## Summary
TrendCast-AI turns a manual video creation process into a single automated pipeline. It is designed for creators who want to convert trending news into shareable video content quickly and efficiently.
