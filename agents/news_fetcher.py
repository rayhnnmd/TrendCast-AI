import os
from google import genai

def fetch_trending_news() -> str:
    """
    Fetches the top 5 trending news stories of the day using Gemini's Google Search Retrieval tool.
    Returns the result as a string containing punchy titles, key facts, and why people care.
    """
    try:
        print(" Initializing news fetcher...")
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        
        client = genai.Client(api_key=api_key)
        
        prompt = (
            "Fetch the top 5 trending news stories of the day. "
            "For each story, provide:\n"
            "- A punchy title\n"
            "- Three key facts\n"
            "- Why people care\n"
            "Format the output clearly."
        )
        
        print(" Searching for trending news...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        print(" News fetched successfully!")
        
        return response.text
        
    except Exception as e:
        print(f" Error fetching news: {e}")
        return ""

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    print(fetch_trending_news())
