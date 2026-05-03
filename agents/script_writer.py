import os
import google.generativeai as genai

def write_script(news_content, genre):
    """
    Generates a sharp, human-sounding video script using Gemini 1.5 Flash.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("[ERROR] GEMINI_API_KEY not found in environment.")
            return None

        genai.configure(api_key=api_key)
        
        system_instruction = """
You are a sharp, witty news writer for short-form video. 
Your job is to take raw news and turn it into a script that 
sounds like a smart, informed human being talking — not a 
news robot, not a press release, not a LinkedIn post.

Rules you never break:
- No cringe openers: never start with "In a world where...", 
  "Imagine if...", "What if I told you...", "Breaking:", 
  or any question as the first line
- No buzzwords: groundbreaking, unprecedented, game-changer, 
  revolutionary, in today's fast-paced world
- No filler: every sentence must carry information
- No emojis in the script
- Short sentences only — max 12 words each
- Write to be SPOKEN, not read
- Sound like a real person who actually finds this interesting
        """

        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=system_instruction
        )

        prompt = f"""
Here are today's top {genre} news stories:

{news_content}

Write a 60-second video script (130-150 words) that:
1. Opens with the single most interesting or surprising fact from these stories — stated directly, no buildup
2. Covers the 3 most important points across the stories
3. Keeps the tone sharp, direct and human
4. Ends with exactly this line: "Stay informed. Follow TrendCast AI."

Do not add any stage directions, labels, or formatting. 
Just the script text, ready to be read aloud.
        """

        response = model.generate_content(prompt)
        script = response.text.strip()
        
        if not script:
            return None
            
        return script

    except Exception as e:
        print(f"[ERROR] script_writer: {e}")
        return None
