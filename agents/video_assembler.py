import os
from moviepy.editor import (
    AudioFileClip, 
    VideoFileClip, 
    ColorClip, 
    TextClip, 
    CompositeVideoClip
)
from moviepy.config import change_settings

# Configure local TEMP directory to avoid Windows permission issues
TEMP_DIR = os.path.join(os.getcwd(), "output", "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# Update this path to match your Magick.exe location
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

def assemble_video(script, audio_path, background_path=None):
    """
    Assembles the final video using MoviePy with a local TEMP folder.
    """
    try:
        os.makedirs("output/videos", exist_ok=True)
        output_path = os.path.join("output", "videos", "final.mp4")
        
        # Load audio
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # Load background or fallback
        if background_path and os.path.exists(background_path):
            bg = VideoFileClip(background_path).loop(duration=duration).resize((1080, 1920))
        else:
            bg = ColorClip(size=(1080, 1920), color=[10, 10, 20], duration=duration)
            
        # Dark overlay
        overlay = ColorClip(size=(1080, 1920), color=[0, 0, 0]).set_opacity(0.5).set_duration(duration)
        
        # Red banner
        banner = ColorClip(size=(1080, 130), color=[210, 0, 0], duration=duration).set_position(("center", 140))
        
        # Banner text
        banner_text = TextClip(
            "BREAKING NEWS", 
            fontsize=60, 
            color="white", 
            font="Arial"
        ).set_position(("center", 163)).set_duration(duration)
        
        # Captions
        words = script.split()
        chunks = [" ".join(words[i:i+7]) for i in range(0, len(words), 7)]
        time_per_chunk = duration / len(chunks)
        caption_clips = []
        
        for i, chunk in enumerate(chunks):
            txt = TextClip(
                chunk,
                fontsize=58,
                color="white",
                font="Arial",
                size=(980, None),
                method="caption",
                align="center"
            ).set_position(("center", 880))\
             .set_start(i * time_per_chunk)\
             .set_duration(time_per_chunk)
            caption_clips.append(txt)
            
        # Watermark
        watermark = TextClip(
            "TrendCast AI", 
            fontsize=32, 
            color="gray", 
            font="Arial"
        ).set_position(("center", 1820)).set_duration(duration)
        
        # Composite
        final = CompositeVideoClip(
            [bg, overlay, banner, banner_text] + caption_clips + [watermark]
        )
        final = final.set_audio(audio)
        
        print(f"Exporting video using MoviePy (Local Temp)...")
        # Export
        final.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            threads=1, 
            temp_audiofile=os.path.join(TEMP_DIR, "temp-audio.m4a"), # Force local temp audio
        )
        
        return output_path

    except Exception as e:
        print(f"Video assembly error (MoviePy): {e}")
        return None
