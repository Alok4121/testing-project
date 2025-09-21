# game.py

class BowlingGame:
    def __init__(self):
        # Store the number of pins knocked down for each roll
        self.rolls = []

    def roll(self, pins: int):
        """Add a roll to the game. Reject invalid values or rolls after game completion."""
        if pins < 0 or pins > 10:
            raise ValueError("Pins rolled must be between 0 and 10.")
        if self.is_finished():
            raise ValueError("Game is already complete. No more rolls allowed.")
        self.rolls.append(pins)

    def score(self) -> int:
        """Calculate the total score for the game after 10 frames."""
        total_score = 0
        roll_index = 0

        for frame in range(10):
            if self._is_strike(roll_index):
                total_score += 10 + self.rolls[roll_index + 1] + self.rolls[roll_index + 2]
                roll_index += 1
            elif self._is_spare(roll_index):
                total_score += 10 + self.rolls[roll_index + 2]
                roll_index += 2
            else:
                total_score += self.rolls[roll_index] + self.rolls[roll_index + 1]
                roll_index += 2

        return total_score

    # ------------------------------
    # Helper methods
    # ------------------------------

    def _is_strike(self, index: int) -> bool:
        """Check if the roll at the given index is a strike."""
        return self.rolls[index] == 10

    def _is_spare(self, index: int) -> bool:
        """Check if the two rolls starting at the given index make a spare."""
        return self.rolls[index] + self.rolls[index + 1] == 10

    def is_finished(self) -> bool:
        """Determine if the game has completed all 10 frames, including any bonus rolls."""
        index = 0

        # Process first 9 frames
        for _ in range(9):
            if index >= len(self.rolls):
                return False
            index += 1 if self.rolls[index] == 10 else 2

        # Handle 10th frame
        if index >= len(self.rolls):
            return False

        first = self.rolls[index]
        second = self.rolls[index + 1] if len(self.rolls) > index + 1 else None

        # Strike in 10th frame requires two extra rolls
        if first == 10:
            return len(self.rolls) >= index + 3

        # Spare in 10th frame requires one extra roll
        if second is not None and first + second == 10:
            return len(self.rolls) >= index + 3

        # Open frame in 10th frame is complete with two rolls
        return second is not None


