# Simple in-memory session store
sessions = {}

def create_session(user_id):
    sessions[user_id] = {"last_recommendation": None, "rejected": []}
    return sessions[user_id]

def update_rejected(user_id, place_name):
    sessions[user_id]["rejected"].append(place_name)

def get_session(user_id):
    return sessions.get(user_id)