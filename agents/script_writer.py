import os
from google import genai
from typing import Dict, Any

def write_script(news_content: str, trend_data: Dict[str, Any]) -> str:
    """
    Takes news content and trend analysis data to generate a short-form video script
    using Gemini. The script will be optimized for viral potential and spoken delivery.
    """
    try:
        print(" Initializing script writer...")
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
            
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are a viral short-form news content creator on TikTok and YouTube Shorts.
        Write a highly engaging video script based on the following news and trend data.
        
        News Content:
        {news_content}
        
        Trend Analysis Data:
        {trend_data.get('analysis', 'No trend analysis available')}
        
        Hard rules:
        - Max 150 words.
        - Short punchy sentences.
        - No filler words.
        - Written to be SPOKEN not read.
        - Feel urgent.
        
        Structure Requirements:
        1. Shocking hook in the first 3 seconds.
        2. 3 key facts delivered clearly.
        3. Viral angle taken from Reddit trend analysis (if available).
        4. CTA at the end exactly as: "Follow for daily news drops"
        """
        
        print(" Generating viral script...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        print(" Script generated successfully!")
        
        return response.text
        
    except Exception as e:
        print(f" Error generating script: {e}")
        return ""

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    test_news = "AI models are becoming more agentic and capable of reasoning."
    test_trend = {"analysis": "People are excited but also anxious about AI safety. Use a dramatic hook."}
    print(write_script(test_news, test_trend))
