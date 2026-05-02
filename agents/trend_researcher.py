import os
import requests
from typing import Dict, Any

def research_trends(news_topic: str) -> Dict[str, Any]:
    """
    Searches NewsAPI for the given news topic, sorts by popularity, 
    fetches top articles, and returns a simple analysis.
    Falls back gracefully if it fails.
    """
    try:
        print(f" Initializing trend researcher for topic: {news_topic}...")
        api_key = os.environ.get("NEWS_API_KEY")
        if not api_key:
            raise ValueError("NEWS_API_KEY environment variable not set.")
        
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={news_topic}&"
            f"sortBy=popularity&"
            f"pageSize=5&"
            f"apiKey={api_key}"
        )
        
        print(" Searching NewsAPI for trending angles...")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title"),
                "source": article.get("source", {}).get("name"),
                "description": article.get("description")
            })
        
        analysis = "Most covered angle: " + articles[0]["title"] if articles else "Focus on breaking news hook"
        
        print(" Trend analysis complete!")
        return {
            "reddit_posts": articles,
            "analysis": analysis
        }

    except Exception as e:
        print(f" Error during trend research: {e}")
        print(" Falling back gracefully: skipping analysis.")
        return {"reddit_posts": [], "analysis": ""}

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    result = research_trends("AI Breakthrough")
    print(result)
