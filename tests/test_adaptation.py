from agent.adaptation import adapt_places


def make_session(rejected=None):
    return {"rejected": rejected or []}


def make_places():
    return [
        {"name": "Cafe A", "score": 1.0},
        {"name": "Cafe B", "score": 0.8},
        {"name": "Cafe C", "score": 0.6},
    ]


def test_rejected_places_excluded():
    places = make_places()
    session = make_session(rejected=["Cafe B"])
    result = adapt_places(places, "too crowded", session)
    names = [p["name"] for p in result]
    assert "Cafe B" not in names


def test_result_sorted_by_score_descending():
    places = make_places()
    result = adapt_places(places, "too crowded", make_session())
    scores = [p["score"] for p in result]
    assert scores == sorted(scores, reverse=True)


def test_penalty_applied_to_rejected_place_scores():
    places = make_places()
    session = make_session(rejected=["Cafe A"])
    # Cafe A is in rejected — it gets penalized then filtered out
    result = adapt_places(places, "too crowded", session)
    assert all(p["name"] != "Cafe A" for p in result)


def test_no_feedback_match_no_penalty():
    places = make_places()
    original_scores = {p["name"]: p["score"] for p in places}
    result = adapt_places(places, "too far", make_session())
    for p in result:
        assert p["score"] == original_scores[p["name"]]


def test_empty_places():
    result = adapt_places([], "too crowded", make_session())
    assert result == []


def test_all_rejected():
    places = make_places()
    session = make_session(rejected=["Cafe A", "Cafe B", "Cafe C"])
    result = adapt_places(places, "too crowded", session)
    assert result == []


def test_noisy_feedback_also_penalizes():
    places = make_places()
    session = make_session(rejected=["Cafe A"])
    result = adapt_places(places, "too noisy", session)
    assert all(p["name"] != "Cafe A" for p in result)
