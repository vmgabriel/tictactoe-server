"""Tic Tac Toe Module"""

# Libraries
from typing import Tuple
from enum import Enum


class PlayStatus(str, Enum):
    WIN = "win"
    DRAW = "draw"
    INGAME = "in game"


class Player:
    figure: str = ""
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class TicTacToe:
    def __init__(self, player1: Player, player2: Player):
        self.figures = ["x", "o"]
        self.player1 = player1
        self.player1.figure = self.figures[0]
        self.player2 = player2
        self.player2.figure = self.figures[1]
        self.status = PlayStatus.INGAME
        self.board = {
            "1": None, "2": None, "3": None,
            "4": None, "5": None, "6": None,
            "7": None, "8": None, "9": None
        }
        self.to_win = [
            ("1", "4", "7"),
            ("2", "5", "8"),
            ("3", "6", "9"),
            ("4", "5", "6"),
            ("7", "8", "9"),
            ("1", "5", "9"),
            ("3", "5", "7"),
        ]

    def _is_draw(self) -> bool:
        """Draw"""
        draw = True
        for board in self.board.values():
            draw = bool(board) and draw
        return draw

    def _winner(self) -> Player or None:
        """Match Winner"""
        for player in [self.player1, self.player2]:
            figure = player.figure
            for condition in self.to_win:
                cond = True
                for space in condition:
                    sp = self.board[space] == figure
                    cond = sp and cond
                if cond:
                    return player
        return None

    def play(self, move: str, player: Player) -> Tuple[PlayStatus, Player or None]:
        """Play game with move and player"""
        if not self.board[move] and self.status == PlayStatus.INGAME:
            self.board[move] = player.figure
            player = self._winner()
            if player:
                self.status = PlayStatus.WIN
            elif self._is_draw():
                self.status = PlayStatus.DRAW
            return self.status, player
        else:
            raise Exception("Error: Move Invalid")
