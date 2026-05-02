import edge_tts
import asyncio
import os

async def _generate(script, output_path):
    communicate = edge_tts.Communicate(
        script,
        voice="en-US-ChristopherNeural",
        rate="+10%",
        volume="+0%"
    )
    await communicate.save(output_path)

def generate_voiceover(script, output_path="output/audio/voiceover.mp3"):
    """
    Generates natural sounding voiceover using Microsoft Edge TTS.
    Takes script (string), returns output_path on success, None on failure.
    """
    try:
        os.makedirs("output/audio", exist_ok=True)
        print("🎙️ Generating voiceover with Edge TTS...")
        asyncio.run(_generate(script, output_path))
        print(f"✅ Voiceover saved to {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Voiceover failed: {e}")
        return None
