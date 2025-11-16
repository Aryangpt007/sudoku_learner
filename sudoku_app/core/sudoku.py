"""
Core Sudoku class for managing puzzle state and validation
"""

import copy
from typing import List, Set, Tuple, Optional


class Sudoku:
    """Represents a Sudoku puzzle with validation and helper methods"""

    def __init__(self, grid: Optional[List[List[int]]] = None, track_history: bool = True):
        """
        Initialize a Sudoku puzzle

        Args:
            grid: 9x9 grid where 0 represents empty cells
            track_history: Whether to track move history for undo/redo
        """
        if grid is None:
            self.grid = [[0 for _ in range(9)] for _ in range(9)]
        else:
            self.grid = [row[:] for row in grid]  # Deep copy

        # Track which cells are initial (given) vs user-filled
        self.initial_cells = set()
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] != 0:
                    self.initial_cells.add((r, c))

        # Pencil marks for each cell (candidates)
        self.pencil_marks = [[set(range(1, 10)) if self.grid[r][c] == 0 else set()
                              for c in range(9)] for r in range(9)]

        # History tracking for undo/redo
        self.track_history = track_history
        self.history_manager = None  # Will be set by GUI if needed

    def is_valid_move(self, row: int, col: int, num: int) -> bool:
        """Check if placing num at (row, col) is valid"""
        if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
            return False

        # Check row
        for c in range(9):
            if c != col and self.grid[row][c] == num:
                return False

        # Check column
        for r in range(9):
            if r != row and self.grid[r][col] == num:
                return False

        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) != (row, col) and self.grid[r][c] == num:
                    return False

        return True

    def set_cell(self, row: int, col: int, num: int) -> bool:
        """
        Set a cell value if valid

        Returns:
            True if successful, False otherwise
        """
        if (row, col) in self.initial_cells:
            return False  # Can't modify initial cells

        if num == 0 or self.is_valid_move(row, col, num):
            self.grid[row][col] = num
            if num != 0:
                self.pencil_marks[row][col] = set()
            else:
                self.update_pencil_marks()
            return True
        return False

    def get_cell(self, row: int, col: int) -> int:
        """Get the value at a cell"""
        return self.grid[row][col]

    def is_initial_cell(self, row: int, col: int) -> bool:
        """Check if a cell was part of the initial puzzle"""
        return (row, col) in self.initial_cells

    def get_candidates(self, row: int, col: int) -> Set[int]:
        """Get possible values for a cell"""
        if self.grid[row][col] != 0:
            return set()

        candidates = set(range(1, 10))

        # Remove numbers in same row
        for c in range(9):
            if self.grid[row][c] in candidates:
                candidates.discard(self.grid[row][c])

        # Remove numbers in same column
        for r in range(9):
            if self.grid[r][col] in candidates:
                candidates.discard(self.grid[r][col])

        # Remove numbers in same box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if self.grid[r][c] in candidates:
                    candidates.discard(self.grid[r][c])

        return candidates

    def update_pencil_marks(self):
        """Update all pencil marks based on current grid state"""
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    self.pencil_marks[r][c] = self.get_candidates(r, c)
                else:
                    self.pencil_marks[r][c] = set()

    def set_pencil_mark(self, row: int, col: int, num: int, enabled: bool):
        """Manually set or unset a pencil mark"""
        if self.grid[row][col] == 0:
            if enabled:
                self.pencil_marks[row][col].add(num)
            else:
                self.pencil_marks[row][col].discard(num)

    def get_pencil_marks(self, row: int, col: int) -> Set[int]:
        """Get pencil marks for a cell"""
        return self.pencil_marks[row][col].copy()

    def is_complete(self) -> bool:
        """Check if the puzzle is completely filled"""
        for row in self.grid:
            if 0 in row:
                return False
        return True

    def is_solved(self) -> bool:
        """Check if the puzzle is correctly solved"""
        if not self.is_complete():
            return False

        # Check all rows, columns, and boxes
        for i in range(9):
            if not self._is_valid_group(self.get_row(i)):
                return False
            if not self._is_valid_group(self.get_column(i)):
                return False
            if not self._is_valid_group(self.get_box(i)):
                return False

        return True

    def _is_valid_group(self, group: List[int]) -> bool:
        """Check if a group (row/column/box) contains all digits 1-9"""
        return set(group) == set(range(1, 10))

    def get_row(self, row: int) -> List[int]:
        """Get all values in a row"""
        return self.grid[row][:]

    def get_column(self, col: int) -> List[int]:
        """Get all values in a column"""
        return [self.grid[r][col] for r in range(9)]

    def get_box(self, box_idx: int) -> List[int]:
        """Get all values in a box (0-8, left-to-right, top-to-bottom)"""
        box_row = 3 * (box_idx // 3)
        box_col = 3 * (box_idx % 3)
        values = []
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                values.append(self.grid[r][c])
        return values

    def get_box_coords(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all coordinates in the same box as (row, col)"""
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        coords = []
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                coords.append((r, c))
        return coords

    def clone(self) -> 'Sudoku':
        """Create a deep copy of this Sudoku"""
        new_sudoku = Sudoku(self.grid)
        new_sudoku.initial_cells = self.initial_cells.copy()
        new_sudoku.pencil_marks = [row[:] for row in self.pencil_marks]
        return new_sudoku

    def clear_non_initial(self):
        """Clear all non-initial cells"""
        for r in range(9):
            for c in range(9):
                if (r, c) not in self.initial_cells:
                    self.grid[r][c] = 0
        self.update_pencil_marks()

    def to_string(self) -> str:
        """Convert grid to string representation (81 characters)"""
        return ''.join(str(self.grid[r][c]) for r in range(9) for c in range(9))

    @classmethod
    def from_string(cls, s: str) -> 'Sudoku':
        """Create Sudoku from string representation"""
        if len(s) != 81:
            raise ValueError("String must be exactly 81 characters")

        grid = []
        for i in range(9):
            row = [int(c) if c.isdigit() else 0 for c in s[i*9:(i+1)*9]]
            grid.append(row)

        return cls(grid)

    def __str__(self) -> str:
        """String representation of the grid"""
        lines = []
        for i, row in enumerate(self.grid):
            if i % 3 == 0 and i != 0:
                lines.append("------+-------+------")
            row_str = ""
            for j, val in enumerate(row):
                if j % 3 == 0 and j != 0:
                    row_str += "| "
                row_str += str(val) if val != 0 else "."
                row_str += " "
            lines.append(row_str.rstrip())
        return "\n".join(lines)
