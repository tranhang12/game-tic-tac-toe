"""A tic-tac-toe game built with Python and Tkinter."""

import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple


class Player(NamedTuple):
    label: str
    color: str


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 10
LINEAR_LEN = 5
DEFAULT_PLAYERS = (
    Player(label="X", color="red"),
    Player(label="O", color="blue"),
)


class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        board = self._current_moves
        row_combo = []
        for i in range(BOARD_SIZE):
            for j in range(0, BOARD_SIZE - LINEAR_LEN + 1):
                single_combo = []
                for k in range(LINEAR_LEN):
                    single_combo.append((board[i][j+k].row, board[i][j+k].col))
                row_combo.append(single_combo)
        
        col_combo = []
        for i in range(0, BOARD_SIZE - LINEAR_LEN + 1):
            for j in range(BOARD_SIZE):
                single_combo = []
                for k in range(LINEAR_LEN):
                    single_combo.append((board[i+k][j].row, board[i+k][j].col))
                col_combo.append(single_combo)
        
        diagonal1_combo = []
        diagonal2_combo = []
        for i in range(0, BOARD_SIZE - LINEAR_LEN + 1):
            for j in range(0, BOARD_SIZE - LINEAR_LEN + 1):
                single_combo1 = []
                single_combo2 = []
                for k in range(LINEAR_LEN):
                    single_combo1.append((board[i+k][j+k].row, board[i+k][j+k].col))
                    single_combo2.append((board[i+k][BOARD_SIZE-1-j-k].row, board[i+k][BOARD_SIZE-1-j-k].col))
                diagonal1_combo.append(single_combo1)
                diagonal2_combo.append(single_combo2)
            
        return row_combo + col_combo + diagonal1_combo + diagonal2_combo

    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col, label = move.row, move.col, move.label
        board = self._current_moves
        board[row][col] = move
        # consecutive = 0
        # block = 0
        # # Check rows
        # for i in range(col+1, BOARD_SIZE):
        #     if board[row][i].label == label:
        #         consecutive += 1
        #         if consecutive >= LINEAR_LEN:
        #             self._has_winner = True
        #             break
        #     elif board[row][i].label == "":
        #         break
        #     else:
        #         block += 1
        #         break

        for combo in self._winning_combos:
            results = set(board[n][m].label for n, m in combo)
            is_unique = (len(results) == 1) and ("" not in results)
            if not is_unique:
                continue
            dir_row = combo[0][0] - combo[1][0]
            dir_col = combo[0][1] - combo[1][1]
            is_win = False
            if (combo[0][0] + dir_row < 0 or 
                combo[0][1] + dir_col < 0 or 
                combo[0][1] + dir_col >= BOARD_SIZE or 
                combo[LINEAR_LEN-1][0] - dir_row >= BOARD_SIZE or
                combo[LINEAR_LEN-1][1] - dir_col >= BOARD_SIZE or 
                combo[LINEAR_LEN-1][1] - dir_col < 0):
                is_win = True
            else:
                label_left = board[combo[0][0] + dir_row][combo[0][1] + dir_col].label
                label_right = board[combo[LINEAR_LEN-1][0] - dir_row][combo[LINEAR_LEN-1][1] - dir_col].label
                if label_left == "" or label_right == "" or label_left == label or label_right == label:
                    is_win = True
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner

    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self._players)

    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []


class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=15)
            self.columnconfigure(row, weight=1, minsize=15)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=18, weight="bold"),
                    fg="black",
                    width=2,
                    height=1,
                    highlightbackground="lightblue",
                    default="active"
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Game draw!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(fg="green", default="active")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")


def main():
    """Create the game's board and run its main loop."""
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()


if __name__ == "__main__":
    main()
