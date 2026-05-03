import os
from moviepy.editor import ImageClip, concatenate_videoclips

def generate_background_video(image_paths, audio_duration):
    """
    Creates a background video from a list of images using MoviePy.
    """
    try:
        if not image_paths:
            return None
            
        os.makedirs("output/backgrounds", exist_ok=True)
        output_path = os.path.join("output", "backgrounds", "background.mp4")
        
        duration_per_image = audio_duration / len(image_paths)
        clips = []
        
        for path in image_paths:
            if os.path.exists(path):
                # Create a clip for each image, resized to 1080x1920
                clip = ImageClip(path).set_duration(duration_per_image).resize(height=1920)
                # Ensure it's exactly 1080x1920 by cropping or centering
                if clip.w > 1080:
                    clip = clip.crop(x_center=clip.w/2, width=1080)
                clips.append(clip)
        
        if not clips:
            return None
            
        # Concatenate all clips
        final_bg = concatenate_videoclips(clips, method="compose")
        
        print("Exporting background video using MoviePy...")
        # Write to file
        final_bg.write_videofile(
            output_path, 
            fps=24, 
            codec="libx264", 
            audio=False, 
            threads=1, 
        )
        
        return output_path

    except Exception as e:
        print(f"Background generation error (MoviePy): {e}")
        return None
