import os
import requests
from gtts import gTTS

def generate_voiceover(script):
    """
    Synthesizes speech using ElevenLabs with a fallback to gTTS if ElevenLabs fails (e.g. quota exceeded).
    """
    os.makedirs("output/audio", exist_ok=True)
    output_path = os.path.join("output", "audio", "voiceover.mp3")
    
    # Try ElevenLabs first
    try:
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if api_key:
            voice_id = "XrExE9yKIg1WjnnlVkGX" # Matilda
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            }
            
            body = {
                "text": script,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.4,
                    "similarity_boost": 0.8,
                    "style": 0.5,
                    "use_speaker_boost": True
                }
            }
            
            response = requests.post(url, headers=headers, json=body)
            
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print("[INFO] Voiceover generated using ElevenLabs.")
                return output_path
            else:
                print(f"[WARNING] ElevenLabs error ({response.status_code}): {response.text}")
                print("[INFO] Falling back to gTTS...")
        else:
            print("[WARNING] ELEVENLABS_API_KEY not found. Using gTTS fallback.")

    except Exception as e:
        print(f"[WARNING] ElevenLabs attempt failed: {e}. Falling back to gTTS...")

    # Fallback to gTTS
    try:
        tts = gTTS(text=script, lang='en', slow=False)
        tts.save(output_path)
        print("[INFO] Voiceover generated using gTTS (Fallback).")
        return output_path
    except Exception as e:
        print(f"[ERROR] gTTS fallback failed: {e}")
        return None
