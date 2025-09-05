# game.py

class BowlingGame:
    def __init__(self):
        # Keep track of all rolls
        self.attempts = []

    def roll(self, pins: int):
        """Record a roll. Reject invalid values or rolls after game ends."""
        if not (0 <= pins <= 10):
            raise ValueError("Roll must be between 0 and 10 pins.")
        if self.is_over():
            raise ValueError("No more rolls allowed. Game has ended.")
        self.attempts.append(pins)

    def score(self):
        """Compute the overall game score after 10 frames."""
        total = 0
        roll_pos = 0

        for frame in range(10):
            if self._is_strike(roll_pos):
                total += 10 + self.attempts[roll_pos + 1] + self.attempts[roll_pos + 2]
                roll_pos += 1
            elif self._is_spare(roll_pos):
                total += 10 + self.attempts[roll_pos + 2]
                roll_pos += 2
            else:
                total += self.attempts[roll_pos] + self.attempts[roll_pos + 1]
                roll_pos += 2

        return total

    # ------------------------------
    # Internal helpers
    # ------------------------------

    def _is_strike(self, roll_pos: int) -> bool:
        return self.attempts[roll_pos] == 10

    def _is_spare(self, roll_pos: int) -> bool:
        return self.attempts[roll_pos] + self.attempts[roll_pos + 1] == 10

    def is_over(self) -> bool:
        """Return True if all 10 frames (including bonuses) are done."""
        pos = 0

        # Handle first 9 frames
        for _ in range(9):
            if pos >= len(self.attempts):
                return False
            if self.attempts[pos] == 10:  # strike
                pos += 1
            else:
                pos += 2

        # Now process 10th frame
        if pos >= len(self.attempts):
            return False

        first_throw = self.attempts[pos]
        second_throw = self.attempts[pos + 1] if len(self.attempts) > pos + 1 else None

        # Strike in 10th frame → needs 2 bonus rolls
        if first_throw == 10:
            return len(self.attempts) >= pos + 3

        # Spare in 10th frame → needs 1 bonus roll
        if second_throw is not None and first_throw + second_throw == 10:
            return len(self.attempts) >= pos + 3

        # Open frame → just two throws
        return second_throw is not None
