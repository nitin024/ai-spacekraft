from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from agent.goal_parser import parse_goal
from mcp.maps_client import fetch_places
from agent.scoring import score_place
from agent.adaptation import adapt_places
from utils.session_manager import create_session, update_rejected, get_session

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.post("/recommend")
def recommend(user_id: str, goal_text: str, location: str):
    session = create_session(user_id)
    goal = parse_goal(goal_text)
    categories = ["cafe", "library", "coworking"]

    places = fetch_places(location, categories)
    if not places:
        return {"error": "No places found"}

    scored = [score_place(p) for p in places]
    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)

    if not ranked:
        return {"error": "No recommendations available"}

    # Save for feedback flow
    session["places"] = ranked
    session["goal"] = goal
    session["last_recommendation"] = ranked[0]["name"]

    return {"recommendation": ranked[0], "top3": ranked[:3]}

@app.post("/feedback")
def feedback(user_id: str, feedback_text: str):
    session = get_session(user_id)
    if not session:
        return {"error": "Session not found"}

    last = session.get("last_recommendation")
    if last:
        update_rejected(user_id, last)

    places = session.get("places", [])
    if not places:
        return {"error": "No previous recommendations available"}

    adapted = adapt_places(places, feedback_text, session)
    if not adapted:
        return {"error": "No adapted recommendations available"}

    session["places"] = adapted
    session["last_recommendation"] = adapted[0]["name"]

    return {"recommendation": adapted[0], "top3": adapted[:3]}