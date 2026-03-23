import requests
import os

MOCK_PLACES = {
    "cafe": [
        {"name": "Café Central", "rating": 4.5, "distance": 0.3, "type": "cafe"},
        {"name": "The Daily Grind", "rating": 4.7, "distance": 0.6, "type": "cafe"},
    ],
    "library": [
        {"name": "City Central Library", "rating": 4.6, "distance": 0.8, "type": "library"},
        {"name": "University Library", "rating": 4.4, "distance": 1.2, "type": "library"},
    ],
    "coworking": [
        {"name": "WeWork City Center", "rating": 4.2, "distance": 0.5, "type": "coworking"},
        {"name": "Spaces Downtown", "rating": 4.3, "distance": 0.9, "type": "coworking"},
    ],
    "park": [
        {"name": "City Park", "rating": 4.5, "distance": 0.4, "type": "park"},
        {"name": "Central Garden", "rating": 4.3, "distance": 0.7, "type": "park"},
    ],
    "restaurant": [
        {"name": "The Corner Bistro", "rating": 4.4, "distance": 0.3, "type": "restaurant"},
        {"name": "Café & Dine", "rating": 4.2, "distance": 0.5, "type": "restaurant"},
    ],
}

def fetch_places(location, categories):
    api_key = os.getenv("MAPS_API_KEY")  # read at call time so load_dotenv() has run

    if not api_key:
        places = []
        for cat in categories:
            for p in MOCK_PLACES.get(cat, []):
                places.append({**p, "name": f"{p['name']} ({location})"})
        return places

    places = []
    for cat in categories:
        try:
            res = requests.post(
                "https://places.googleapis.com/v1/places:searchText",
                json={"textQuery": f"{cat} in {location}"},
                headers={
                    "Content-Type": "application/json",
                    "X-Goog-Api-Key": api_key,
                    "X-Goog-FieldMask": "places.displayName,places.rating",
                },
                timeout=5,
            ).json()

            if "error" in res:
                print(f"Maps API error for {cat}: {res['error'].get('message', '')}")
                continue

            for p in res.get("places", []):
                places.append({
                    "name": p["displayName"]["text"],
                    "rating": p.get("rating", 3.0),
                    "distance": 0,
                    "type": cat,
                })
        except Exception as e:
            print(f"Request failed for {cat}: {e}")
            continue

    return places
