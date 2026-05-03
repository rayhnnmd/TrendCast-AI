import os
import requests

def fetch_images(genre):
    """
    Fetches 6 relevant portrait images from Pexels based on the news genre.
    Returns a list of local file paths.
    """
    try:
        api_key = os.getenv("PEXELS_API_KEY")
        if not api_key:
            print("[ERROR] PEXELS_API_KEY not found in environment.")
            return []

        query_map = {
            "Technology": "technology futuristic city neon",
            "Politics": "government parliament building dramatic",
            "Business": "business finance city skyline",
            "Sports": "sports stadium crowd action",
            "Science": "space science laboratory cosmos",
            "Entertainment": "concert stage spotlight crowd",
            "World News": "earth globe aerial world"
        }

        query = query_map.get(genre, "world news aerial")
        url = "https://api.pexels.com/v1/search"
        headers = {"Authorization": api_key}
        params = {
            "query": query,
            "per_page": 6,
            "orientation": "portrait"
        }

        os.makedirs("output/images", exist_ok=True)
        
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        photos = data.get("photos", [])
        image_paths = []

        for i, photo in enumerate(photos):
            image_url = photo.get("src", {}).get("large")
            if not image_url:
                continue
                
            try:
                img_data = requests.get(image_url).content
                path = os.path.join("output/images", f"img_{i+1}.jpg")
                with open(path, "wb") as f:
                    f.write(img_data)
                image_paths.append(path)
            except:
                print(f"[WARNING] Failed to download image {i+1}")
                continue

        return image_paths

    except Exception as e:
        print(f"[ERROR] image_fetcher: {e}")
        return []
