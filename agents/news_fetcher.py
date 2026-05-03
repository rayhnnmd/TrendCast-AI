import os
import requests

def fetch_top_news(genre):
    """
    Fetches top news headlines from NewsAPI based on the selected genre.
    Returns a formatted string of news stories.
    """
    try:
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            print("[ERROR] NEWS_API_KEY not found in environment.")
            return None

        genre_map = {
            "Technology": "technology",
            "Politics": "general",
            "Business": "business",
            "Sports": "sports",
            "Science": "science",
            "Entertainment": "entertainment",
            "World News": "general"
        }

        category = genre_map.get(genre, "general")
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": api_key,
            "category": category,
            "pageSize": 5,
            "language": "en",
            "country": "us"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200:
            print(f"[ERROR] NewsAPI Error: {data.get('message', 'Unknown error')}")
            return None

        articles = data.get("articles", [])
        formatted_news = []
        count = 1

        for art in articles:
            title = art.get("title")
            desc = art.get("description")
            source = art.get("source", {}).get("name")

            if title and desc:
                formatted_news.append(f"{count}. [{source}] {title}\n   {desc}")
                count += 1

        if not formatted_news:
            return "No relevant news found for this genre."

        return "\n\n".join(formatted_news)

    except Exception as e:
        print(f"[ERROR] news_fetcher: {e}")
        return None
