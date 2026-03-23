INTENT_KEYWORDS = {
    "work":   ["work", "working", "focus", "productive", "productivity", "deep work", "coding", "laptop"],
    "study":  ["study", "studying", "revise", "revision", "exam", "homework", "assignment", "research"],
    "relax":  ["relax", "relaxing", "chill", "chilling", "unwind", "hang out", "hangout", "leisure", "break"],
    "meet":   ["meet", "meeting", "client", "interview", "call", "discussion", "team", "catch up"],
    "read":   ["read", "reading", "book", "books", "journal"],
}

PREFERENCE_KEYWORDS = {
    "quiet":   ["quiet", "silent", "peaceful", "no noise", "calm"],
    "wifi":    ["wifi", "wi-fi", "internet", "online"],
    "cheap":   ["cheap", "free", "affordable", "budget", "low cost"],
    "outdoor": ["outdoor", "outside", "open air", "garden", "terrace", "park"],
    "food":    ["food", "eat", "snack", "lunch", "breakfast", "hungry"],
    "coffee":  ["coffee", "espresso", "latte", "cappuccino", "cafe"],
    "24hours": ["24 hours", "24/7", "late night", "night", "open late", "always open"],
}

# Maps intent to best-fit place categories
INTENT_CATEGORIES = {
    "work":   ["coworking", "cafe", "library"],
    "study":  ["library", "cafe", "coworking"],
    "relax":  ["cafe", "park", "restaurant"],
    "meet":   ["cafe", "coworking", "restaurant"],
    "read":   ["library", "cafe"],
}

def parse_goal(text):
    text_lower = text.lower()

    # Detect intent
    intent = "work"  # default
    for key, keywords in INTENT_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            intent = key
            break

    # Detect preferences
    preferences = []
    for pref, keywords in PREFERENCE_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            preferences.append(pref)

    # Detect duration
    duration = 120  # default 2 hours
    if "quick" in text_lower or "short" in text_lower or "30 min" in text_lower:
        duration = 30
    elif "half day" in text_lower or "3 hour" in text_lower:
        duration = 180
    elif "full day" in text_lower or "all day" in text_lower:
        duration = 480

    categories = INTENT_CATEGORIES.get(intent, ["cafe", "library", "coworking"])

    return {
        "intent": intent,
        "duration": duration,
        "preferences": preferences,
        "categories": categories,
    }
