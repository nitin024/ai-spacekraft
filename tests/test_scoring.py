import pytest
from agent.scoring import estimate_quiet, estimate_crowd, score_place


# --- estimate_quiet ---

def test_quiet_library():
    assert estimate_quiet({"type": "library"}) == 1.0


def test_quiet_coworking():
    assert estimate_quiet({"type": "coworking"}) == 0.8


def test_quiet_default():
    assert estimate_quiet({"type": "cafe"}) == 0.5


# --- estimate_crowd ---

def test_crowd_peak_hour_high_rating():
    place = {"rating": 4.8}
    assert estimate_crowd(place, hour=12) == 0.5
    assert estimate_crowd(place, hour=17) == 0.5


def test_crowd_off_peak_high_rating():
    place = {"rating": 4.8}
    assert estimate_crowd(place, hour=10) == 0.1


def test_crowd_low_rating_peak_hour():
    place = {"rating": 3.0}
    assert estimate_crowd(place, hour=12) == 0.1


# --- score_place ---

@pytest.fixture
def library():
    return {"name": "City Library", "type": "library", "rating": 4.8, "distance": 1.0}


def test_score_place_returns_place(library):
    result = score_place(library)
    assert result is library


def test_score_place_adds_score_key(library):
    score_place(library)
    assert "score" in library


def test_score_place_higher_score_off_peak(library):
    off_peak = score_place(dict(library), hour=10)
    peak = score_place(dict(library), hour=12)
    assert off_peak["score"] > peak["score"]


def test_score_place_closer_scores_higher():
    near = {"type": "cafe", "rating": 4.0, "distance": 0.1}
    far = {"type": "cafe", "rating": 4.0, "distance": 5.0}
    score_place(near, hour=10)
    score_place(far, hour=10)
    assert near["score"] > far["score"]
