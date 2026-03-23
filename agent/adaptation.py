def adapt_places(places, feedback, session):
    rejected = session["rejected"]
    if feedback == "too crowded" or feedback == "too noisy":
        # Penalize rejected place
        for p in places:
            if p["name"] in rejected:
                p["score"] -= 0.5
    # Return ranked places
    return sorted([p for p in places if p["name"] not in rejected], key=lambda x: x["score"], reverse=True)