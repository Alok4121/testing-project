# test_game.py
import pytest
from game import BowlingGame

# -------------------------------
# Utility functions for rolls
# -------------------------------

def roll_repeated(game: BowlingGame, times: int, pins: int):
    """Roll the same number of pins multiple times."""
    for _ in range(times):
        game.roll(pins)

def make_spare(game: BowlingGame):
    """Roll a spare (5 + 5)."""
    game.roll(5)
    game.roll(5)

def make_strike(game: BowlingGame):
    """Roll a strike (10 pins)."""
    game.roll(10)

# -------------------------------
# TEST CASES
# -------------------------------

def test_all_zeros():
    """Game of 20 gutter balls should score 0."""
    g = BowlingGame()
    roll_repeated(g, 20, 0)
    assert g.score() == 0

def test_all_ones_game():
    """Game of 20 rolls knocking 1 pin each = 20."""
    g = BowlingGame()
    roll_repeated(g, 20, 1)
    assert g.score() == 20

def test_single_spare_bonus():
    """Check spare adds next roll as bonus."""
    g = BowlingGame()
    make_spare(g)   # 5 + 5
    g.roll(3)       # bonus roll
    roll_repeated(g, 17, 0)
    assert g.score() == 16

def test_single_strike_bonus():
    """Check strike adds next two rolls as bonus."""
    g = BowlingGame()
    make_strike(g)  # 10
    g.roll(3)
    g.roll(4)
    roll_repeated(g, 16, 0)
    assert g.score() == 24

def test_flawless_perfect_game():
    """12 strikes in a row → maximum 300 points."""
    g = BowlingGame()
    roll_repeated(g, 12, 10)
    assert g.score() == 300

def test_spare_in_final_frame():
    """10th frame spare gives one extra roll."""
    g = BowlingGame()
    roll_repeated(g, 18, 0)
    make_spare(g)   # 10th frame spare
    g.roll(7)       # bonus roll
    assert g.score() == 17

def test_strike_in_final_frame():
    """10th frame strike gives two extra rolls."""
    g = BowlingGame()
    roll_repeated(g, 18, 0)
    make_strike(g)  # 10th frame strike
    g.roll(7)
    g.roll(2)
    assert g.score() == 19

def test_disallow_roll_after_game_over():
    """Rolling after the game is complete should raise error."""
    g = BowlingGame()
    roll_repeated(g, 12, 10)  # perfect game
    with pytest.raises(ValueError):
        g.roll(10)

def test_negative_pins_invalid():
    """Rolling a negative number of pins should be invalid."""
    g = BowlingGame()
    with pytest.raises(ValueError):
        g.roll(-1)

def test_too_many_pins_invalid():
    """Rolling more than 10 pins in one roll should be invalid."""
    g = BowlingGame()
    with pytest.raises(ValueError):
        g.roll(11)
