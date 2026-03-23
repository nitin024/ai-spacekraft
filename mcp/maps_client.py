import requests
import os

API_KEY = os.getenv("MAPS_API_KEY")

MOCK_PLACES = {
    "cafe": [
        {"name": "Café de Jaren", "rating": 4.5, "distance": 0, "type": "cafe"},
        {"name": "Lot Sixty One Coffee", "rating": 4.7, "distance": 0, "type": "cafe"},
    ],
    "library": [
        {"name": "OBA Central Library", "rating": 4.6, "distance": 0, "type": "library"},
        {"name": "University of Amsterdam Library", "rating": 4.4, "distance": 0, "type": "library"},
    ],
    "coworking": [
        {"name": "WeWork Amsterdam", "rating": 4.2, "distance": 0, "type": "coworking"},
        {"name": "Spaces Vijzelstraat", "rating": 4.3, "distance": 0, "type": "coworking"},
    ],
}

def fetch_places(location, categories):
    if not API_KEY:
        places = []
        for cat in categories:
            places.extend(MOCK_PLACES.get(cat, []))
        return places

    places = []
    for cat in categories:
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={cat}+in+{location}&key={API_KEY}"
        res = requests.get(url).json()
        for p in res.get("results", []):
            places.append({
                "name": p["name"],
                "rating": p.get("rating", 0),
                "distance": 0,
                "type": cat
            })
    return places