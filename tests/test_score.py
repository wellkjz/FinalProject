import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from systems.scoring import ScoreSystem


def test_gold_adds_points():
    s = ScoreSystem()
    s.collect_coin("gold")
    assert s.score == 1000


def test_blue_deducts_points():
    s = ScoreSystem()
    s.collect_coin("gold")
    s.collect_coin("blue")
    assert s.score == 800


def test_score_never_negative():
    s = ScoreSystem()
    s.collect_coin("blue")
    assert s.score == 0


def test_scroll_increases_score():
    s = ScoreSystem()
    s.add_scroll(200)
    assert s.score == 200


def test_reset_clears_score():
    s = ScoreSystem()
    s.collect_coin("gold")
    s.reset()
    assert s.score == 0