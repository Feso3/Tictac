import io
import unittest
from contextlib import redirect_stdout

import main


class TestTicTacToeHelpers(unittest.TestCase):
    def test_check_winner_detects_all_lines(self):
        winning_boards = {
            "row": ["X", "X", "X", "", "", "", "", "", ""],
            "column": ["O", "", "", "O", "", "", "O", "", ""],
            "diag_left": ["X", "", "", "", "X", "", "", "", "X"],
            "diag_right": ["", "", "O", "", "O", "", "O", "", ""],
        }

        for name, board in winning_boards.items():
            with self.subTest(name=name):
                self.assertEqual(main.check_winner(board), board[[i for i, v in enumerate(board) if v][0]])

    def test_is_draw_true_when_board_full_without_winner(self):
        full_board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        self.assertTrue(main.is_draw(full_board))

    def test_is_draw_false_when_spaces_remain(self):
        in_progress_board = ["X", "O", "", "", "O", "X", "", "", ""]
        self.assertFalse(main.is_draw(in_progress_board))

    def test_is_draw_false_when_winner_exists(self):
        winning_board = ["X", "X", "X", "O", "O", "", "", "", ""]
        self.assertFalse(main.is_draw(winning_board))

    def test_alternating_starts_cycles_between_marks(self):
        generator = main.alternating_starts()
        sequence = [next(generator) for _ in range(6)]
        self.assertEqual(sequence, ["X", "O", "X", "O", "X", "O"])

    def test_print_board_shows_numbers_for_empty_squares(self):
        board = ["", "O", "", "X", "", "", "", "", "X"]
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            main.print_board(board)
        output_lines = [line for line in buffer.getvalue().splitlines() if line.strip()]
        self.assertEqual(output_lines[0], " 1 | O | 3")
        self.assertEqual(output_lines[-1], " 7 | 8 | X")

    def test_display_scoreboard_includes_player_names(self):
        players = {"X": "Alice", "O": "Bob"}
        scores = {"X": 2, "O": 1, "draws": 3}
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            main.display_scoreboard(scores, players)
        output = buffer.getvalue()
        self.assertIn("Alice (X): 2", output)
        self.assertIn("Bob (O): 1", output)
        self.assertIn("Draws: 3", output)


if __name__ == "__main__":
    unittest.main()
