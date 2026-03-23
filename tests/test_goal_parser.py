from agent.goal_parser import parse_goal


def test_default_intent_and_duration():
    result = parse_goal("somewhere to work")
    assert result["intent"] == "work"
    assert result["duration"] == 120
    assert result["preferences"] == []


def test_detects_quiet():
    result = parse_goal("I need a quiet place")
    assert "quiet" in result["preferences"]


def test_detects_wifi():
    result = parse_goal("needs wifi")
    assert "wifi" in result["preferences"]


def test_detects_both():
    result = parse_goal("quiet spot with wifi")
    assert "quiet" in result["preferences"]
    assert "wifi" in result["preferences"]


def test_no_false_positives():
    result = parse_goal("loud coffee shop")
    assert "quiet" not in result["preferences"]
    assert "wifi" not in result["preferences"]
