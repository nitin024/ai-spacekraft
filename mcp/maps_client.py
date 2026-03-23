import requests
import os
import math


def _haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 2)


def _geocode(location, api_key):
    try:
        res = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": location, "key": api_key},
            timeout=5,
        ).json()
        if res.get("status") == "OK":
            loc = res["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]
    except Exception:
        pass
    return None, None

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

    user_lat, user_lon = _geocode(location, api_key)

    places = []
    for cat in categories:
        try:
            res = requests.post(
                "https://places.googleapis.com/v1/places:searchText",
                json={"textQuery": f"{cat} in {location}"},
                headers={
                    "Content-Type": "application/json",
                    "X-Goog-Api-Key": api_key,
                    "X-Goog-FieldMask": "places.displayName,places.rating,places.location",
                },
                timeout=5,
            ).json()

            if "error" in res:
                print(f"Maps API error for {cat}: {res['error'].get('message', '')}")
                continue

            for p in res.get("places", []):
                loc = p.get("location", {})
                if user_lat is not None and loc.get("latitude") is not None:
                    distance = _haversine_km(user_lat, user_lon, loc["latitude"], loc["longitude"])
                else:
                    distance = 1.0  # neutral fallback when coordinates unavailable
                places.append({
                    "name": p["displayName"]["text"],
                    "rating": p.get("rating", 3.0),
                    "distance": distance,
                    "type": cat,
                })
        except Exception as e:
            print(f"Request failed for {cat}: {e}")
            continue

    return places
