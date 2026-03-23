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


def score_place(place, hour=12):
    rating_score = place["rating"] * 0.4
    distance_score = 1 / (place["distance"] + 0.1) * 0.3
    quiet_score = estimate_quiet(place) * 0.3
    crowd_penalty = estimate_crowd(place, hour)
    place["score"] = rating_score + distance_score + quiet_score - crowd_penalty
    return place
