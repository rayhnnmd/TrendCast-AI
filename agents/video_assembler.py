import os
# Configure ImageMagick path for MoviePy on Windows
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

from moviepy.editor import *

def assemble_video(script, audio_path, 
                   background_path=None,
                   category="Global",
                   output_path="output/videos/final.mp4"):
    """
    Assembles final video with background footage, captions, banner and audio.
    Returns output_path on success.
    """
    try:
        os.makedirs("output/videos", exist_ok=True)
        
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # Background — use video if available, else dark color
        if background_path and os.path.exists(background_path):
            bg = VideoFileClip(background_path)\
                .resize((1080, 1920))\
                .loop(duration=duration)\
                .set_duration(duration)
            # Darken background for text readability
            bg = bg.fl_image(lambda frame: (frame * 0.5).astype('uint8'))
        else:
            bg = ColorClip(
                size=(1080, 1920),
                color=[10, 10, 20],
                duration=duration
            )
        
        # Category badge at top
        badge = TextClip(
            f"⚡ {category.upper()}",
            fontsize=50,
            color="white",
            font="Arial-Bold",
            bg_color="red",
            size=(1080, 100)
        ).set_position(("center", 120)).set_duration(duration)
        
        # Split script into caption chunks
        words = script.split()
        chunks = [
            " ".join(words[i:i+6])
            for i in range(0, len(words), 6)
        ]
        
        time_per_chunk = duration / len(chunks)
        caption_clips = []
        
        for i, chunk in enumerate(chunks):
            # Shadow effect for readability
            shadow = TextClip(
                chunk,
                fontsize=62,
                color="black",
                font="Arial-Bold",
                size=(984, None),
                method="caption",
                align="center"
            ).set_position((3, 853))\
             .set_start(i * time_per_chunk)\
             .set_duration(time_per_chunk)
            
            cap = TextClip(
                chunk,
                fontsize=62,
                color="white",
                font="Arial-Bold",
                size=(980, None),
                method="caption",
                align="center"
            ).set_position(("center", 850))\
             .set_start(i * time_per_chunk)\
             .set_duration(time_per_chunk)\
             .crossfadein(0.15)
            
            caption_clips.append(shadow)
            caption_clips.append(cap)
        
        # Watermark
        watermark = TextClip(
            "TrendForge AI",
            fontsize=35,
            color="white",
            font="Arial",
            bg_color="black"
        ).set_position(("center", 1820)).set_duration(duration)
        
        # Composite everything
        final = CompositeVideoClip(
            [bg, badge] + caption_clips + [watermark]
        )
        final = final.set_audio(audio)
        
        final.write_videofile(
            output_path,
            fps=30,
            codec="libx264",
            audio_codec="aac",
            threads=4
        )
        
        print(f"✅ Video saved to {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Video assembly failed: {e}")
        return None
