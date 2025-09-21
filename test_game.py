# test_game.py
import pytest
from game import BowlingGame

# -------------------------------
# Helper functions for rolling
# -------------------------------

def roll_multiple_times(game: BowlingGame, count: int, pins: int):
    """Roll the same number of pins repeatedly."""
    for _ in range(count):
        game.roll(pins)

def roll_spare(game: BowlingGame):
    """Roll a spare (5 pins each roll)."""
    game.roll(5)
    game.roll(5)

def roll_strike(game: BowlingGame):
    """Roll a strike (all 10 pins)."""
    game.roll(10)

# -------------------------------
# Test scenarios
# -------------------------------

def test_gutter_game():
    """All rolls knock down 0 pins → total score 0."""
    game = BowlingGame()
    roll_multiple_times(game, 20, 0)
    assert game.score() == 0

def test_all_ones():
    """All rolls knock down 1 pin → total score 20."""
    game = BowlingGame()
    roll_multiple_times(game, 20, 1)
    assert game.score() == 20

def test_spare_bonus_roll():
    """A spare should add the next roll as a bonus."""
    game = BowlingGame()
    roll_spare(game)      # spare
    game.roll(3)          # bonus roll
    roll_multiple_times(game, 17, 0)
    assert game.score() == 16

def test_strike_bonus_rolls():
    """A strike should add the next two rolls as bonus."""
    game = BowlingGame()
    roll_strike(game)     # strike
    game.roll(3)
    game.roll(4)
    roll_multiple_times(game, 16, 0)
    assert game.score() == 24

def test_perfect_game():
    """12 consecutive strikes → maximum score of 300."""
    game = BowlingGame()
    roll_multiple_times(game, 12, 10)
    assert game.score() == 300

def test_spare_in_last_frame():
    """A spare in the 10th frame grants one extra roll."""
    game = BowlingGame()
    roll_multiple_times(game, 18, 0)
    roll_spare(game)       # 10th frame spare
    game.roll(7)           # bonus roll
    assert game.score() == 17

def test_strike_in_last_frame():
    """A strike in the 10th frame grants two extra rolls."""
    game = BowlingGame()
    roll_multiple_times(game, 18, 0)
    roll_strike(game)      # 10th frame strike
    game.roll(7)
    game.roll(2)
    assert game.score() == 19

def test_no_rolls_after_game_end():
    """Rolling after game completion should raise an error."""
    game = BowlingGame()
    roll_multiple_times(game, 12, 10)  # perfect game
    with pytest.raises(ValueError):
        game.roll(10)

def test_invalid_negative_pins():
    """Rolling a negative number of pins should raise an error."""
    game = BowlingGame()
    with pytest.raises(ValueError):
        game.roll(-1)

def test_invalid_excess_pins():
    """Rolling more than 10 pins in a single roll should raise an error."""
    game = BowlingGame()
    with pytest.raises(ValueError):
        game.roll(11)
