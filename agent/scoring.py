def estimate_quiet(place):
    if place["type"] == "library":
        return 1.0
    elif place["type"] == "coworking":
        return 0.8
    elif place["type"] == "cafe":
        return 0.7
    return 0.5


def estimate_crowd(place, hour=12):
    peak_hours = [12, 13, 17, 18]
    if place["rating"] > 4.5 and hour in peak_hours:
        return 0.5
    return 0.1


PREFERENCE_BOOSTS = {
    "quiet":   {"library": 0.3, "coworking": 0.2, "cafe": -0.1},
    "wifi":    {"coworking": 0.3, "cafe": 0.2, "library": 0.1},
    "cheap":   {"library": 0.3, "cafe": 0.1, "coworking": -0.2},
    "outdoor": {"cafe": 0.2, "park": 0.4, "restaurant": 0.1},
    "food":    {"cafe": 0.3, "restaurant": 0.4, "coworking": -0.1},
    "coffee":  {"cafe": 0.4, "coworking": 0.1, "library": -0.2},
    "24hours": {"coworking": 0.2, "cafe": 0.1},
}


def score_place(place, hour=12, preferences=None):
    rating_score = place["rating"] * 0.4
    distance_score = 1 / (place["distance"] + 0.1) * 0.3
    quiet_score = estimate_quiet(place) * 0.3
    crowd_penalty = estimate_crowd(place, hour)

    base_score = rating_score + distance_score + quiet_score - crowd_penalty

    # Apply preference boosts
    pref_bonus = 0.0
    if preferences:
        for pref in preferences:
            boosts = PREFERENCE_BOOSTS.get(pref, {})
            pref_bonus += boosts.get(place["type"], 0.0)

    place["score"] = round(base_score + pref_bonus, 3)
    return place
