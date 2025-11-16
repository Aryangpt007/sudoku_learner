"""
Move History Manager for Undo/Redo functionality
"""

from typing import List, Optional, Tuple, Set
from enum import Enum


class MoveType(Enum):
    """Types of moves that can be undone/redone"""
    SET_VALUE = "set_value"
    SET_PENCIL_MARK = "set_pencil_mark"
    AUTO_FILL_PENCIL = "auto_fill_pencil"
    CLEAR_CELL = "clear_cell"


class Move:
    """Represents a single move in the game"""

    def __init__(self, move_type: MoveType, row: int, col: int,
                 old_value=None, new_value=None,
                 old_pencil_marks: Set[int] = None,
                 new_pencil_marks: Set[int] = None):
        self.move_type = move_type
        self.row = row
        self.col = col
        self.old_value = old_value
        self.new_value = new_value
        self.old_pencil_marks = old_pencil_marks.copy() if old_pencil_marks else set()
        self.new_pencil_marks = new_pencil_marks.copy() if new_pencil_marks else set()

    def __repr__(self):
        return f"Move({self.move_type}, ({self.row},{self.col}), {self.old_value}->{self.new_value})"


class HistoryManager:
    """Manages undo/redo history for Sudoku moves"""

    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.undo_stack: List[Move] = []
        self.redo_stack: List[Move] = []

    def add_move(self, move: Move):
        """Add a move to the history"""
        # Add to undo stack
        self.undo_stack.append(move)

        # Limit stack size
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)

        # Clear redo stack when new move is made
        self.redo_stack.clear()

    def can_undo(self) -> bool:
        """Check if undo is available"""
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        """Check if redo is available"""
        return len(self.redo_stack) > 0

    def undo(self) -> Optional[Move]:
        """Get the move to undo"""
        if not self.can_undo():
            return None

        move = self.undo_stack.pop()
        self.redo_stack.append(move)
        return move

    def redo(self) -> Optional[Move]:
        """Get the move to redo"""
        if not self.can_redo():
            return None

        move = self.redo_stack.pop()
        self.undo_stack.append(move)
        return move

    def clear(self):
        """Clear all history"""
        self.undo_stack.clear()
        self.redo_stack.clear()

    def get_undo_count(self) -> int:
        """Get number of available undos"""
        return len(self.undo_stack)

    def get_redo_count(self) -> int:
        """Get number of available redos"""
        return len(self.redo_stack)
