"""Updated Tic-Tac-Toe game with replay, scorekeeping, and fair starts."""

from __future__ import annotations

from itertools import cycle
from typing import Dict, Iterator, List, Optional, Tuple

BOARD_TEMPLATE = """
 {0} | {1} | {2}
-----------
 {3} | {4} | {5}
-----------
 {6} | {7} | {8}
"""


def print_board(board: List[str]) -> None:
    """Display the current game board."""
    display = [value if value else str(index + 1) for index, value in enumerate(board)]
    print(BOARD_TEMPLATE.format(*display))


def preview_board_positions() -> None:
    """Show the numbered board layout before play begins."""
    print("Squares are numbered as follows:")
    print(BOARD_TEMPLATE.format(*[str(index + 1) for index in range(9)]))
    print()


def check_winner(board: List[str]) -> Optional[str]:
    """Return the winning mark ('X' or 'O') if present."""
    winning_lines: Tuple[Tuple[int, int, int], ...] = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6),  # diagonals
    )

    for a, b, c in winning_lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board: List[str]) -> bool:
    """Return True if no empty squares remain and there is no winner."""
    return all(board) and check_winner(board) is None


def prompt_player_name(mark: str) -> str:
    """Ask for a player's preferred display name."""
    name = input(f"Enter a name for player {mark} (or leave blank for default): ").strip()
    return name or f"Player {mark}"


def prompt_move(player_label: str, board: List[str]) -> Optional[int]:
    """Prompt the current player for a move; return None to quit the round."""
    while True:
        choice = input(
            f"{player_label}, choose a square (1-9) or 'q' to quit the round: "
        ).strip().lower()

        if choice in {"q", "quit"}:
            return None

        try:
            position = int(choice) - 1
        except ValueError:
            print("Please enter a number between 1 and 9, or 'q' to quit.")
            continue

        if position not in range(9):
            print("That position is out of range. Try again.")
        elif board[position]:
            print("That square is already taken. Try another.")
        else:
            return position


def display_scoreboard(scores: Dict[str, int], players: Dict[str, str]) -> None:
    """Print the current scoreboard."""
    print("\nScoreboard:")
    print(f"{players['X']} (X): {scores['X']}")
    print(f"{players['O']} (O): {scores['O']}")
    print(f"Draws: {scores['draws']}\n")


def alternating_starts() -> Iterator[str]:
    """Generate an infinite sequence alternating 'X' and 'O' for fair starts."""
    return cycle(["X", "O"])


def play_round(players: Dict[str, str], starter: str) -> str:
    """Play a single round and return 'X', 'O', 'draw', or 'quit'."""
    board: List[str] = ["" for _ in range(9)]
    current_player = starter

    while True:
        print_board(board)
        move = prompt_move(players[current_player], board)
        if move is None:
            print(f"{players[current_player]} chose to quit the round.")
            return "quit"

        board[move] = current_player

        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"{players[winner]} wins! Congratulations!")
            return winner

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            return "draw"

        current_player = "O" if current_player == "X" else "X"


def main() -> None:
    """Run the Tic-Tac-Toe game with replay and scorekeeping."""
    print("Updated tic-tac-toe game. Welcome to Tic-Tac-Toe!\n")
    players = {"X": prompt_player_name("X"), "O": prompt_player_name("O")}
    scores = {"X": 0, "O": 0, "draws": 0}
    starters = alternating_starts()

    preview_board_positions()

    while True:
        starter = next(starters)
        print(f"{players[starter]} ({starter}) will start this round.\n")
        result = play_round(players, starter)
        if result in {"X", "O"}:
            scores[result] += 1
        elif result == "draw":
            scores["draws"] += 1
        else:  # quit mid-round
            break

        display_scoreboard(scores, players)

        again = input("Play again? (y/n): ").strip().lower()
        if again not in {"y", "yes"}:
            break

    print("Thanks for playing!")
    display_scoreboard(scores, players)


if __name__ == "__main__":
    main()
