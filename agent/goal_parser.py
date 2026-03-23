def parse_goal(text):
    # Basic keyword parsing
    goal = {"intent": "work", "duration": 120, "preferences": []}
    if "quiet" in text:
        goal["preferences"].append("quiet")
    if "wifi" in text:
        goal["preferences"].append("wifi")
    return goal
