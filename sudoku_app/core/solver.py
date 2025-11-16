"""
Advanced Sudoku Solver with multiple techniques
"""

import copy
from typing import List, Set, Tuple, Optional, Dict
from .sudoku import Sudoku


class SolveStep:
    """Represents a single solving step"""

    def __init__(self, technique: str, description: str, cells: List[Tuple[int, int]],
                 values: List[int], eliminations: List[Tuple[int, int, Set[int]]] = None):
        self.technique = technique
        self.description = description
        self.cells = cells  # Cells involved
        self.values = values  # Values placed or involved
        self.eliminations = eliminations or []  # (row, col, eliminated_candidates)

    def __str__(self):
        return f"{self.technique}: {self.description}"


class SudokuSolver:
    """Advanced Sudoku solver with multiple techniques"""

    # Technique difficulty levels
    TECHNIQUE_LEVELS = {
        'naked_single': 1,
        'hidden_single': 1,
        'naked_pair': 2,
        'naked_triple': 3,
        'hidden_pair': 2,
        'hidden_triple': 3,
        'pointing_pair': 2,
        'box_line_reduction': 2,
        'naked_quad': 4,
        'hidden_quad': 4,
        'x_wing': 4,
        'swordfish': 5,
        'xy_wing': 5,
    }

    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku.clone()
        self.steps: List[SolveStep] = []
        self.max_technique_used = 0

    def solve(self, step_by_step: bool = False) -> bool:
        """
        Solve the Sudoku puzzle

        Args:
            step_by_step: If True, record each solving step

        Returns:
            True if solved, False otherwise
        """
        self.steps = []
        self.max_technique_used = 0

        if step_by_step:
            return self._solve_logical()
        else:
            return self._solve_backtrack()

    def _solve_logical(self) -> bool:
        """Solve using logical techniques, recording steps"""
        self.sudoku.update_pencil_marks()

        progress = True
        iterations = 0
        max_iterations = 1000

        while progress and iterations < max_iterations:
            progress = False
            iterations += 1

            # Try techniques in order of difficulty
            if self._apply_naked_singles():
                progress = True
                continue

            if self._apply_hidden_singles():
                progress = True
                continue

            if self._apply_pointing_pairs():
                progress = True
                continue

            if self._apply_box_line_reduction():
                progress = True
                continue

            if self._apply_naked_pairs():
                progress = True
                continue

            if self._apply_naked_triples():
                progress = True
                continue

            if self._apply_hidden_pairs():
                progress = True
                continue

            if self._apply_hidden_triples():
                progress = True
                continue

            if self._apply_x_wing():
                progress = True
                continue

            # If no logical technique works, try backtracking
            if not progress and not self.sudoku.is_complete():
                return self._solve_backtrack()

        return self.sudoku.is_solved()

    def _apply_naked_singles(self) -> bool:
        """Find and apply naked singles (cells with only one candidate)"""
        found = False
        for r in range(9):
            for c in range(9):
                if self.sudoku.grid[r][c] == 0:
                    candidates = self.sudoku.get_candidates(r, c)
                    if len(candidates) == 1:
                        value = list(candidates)[0]
                        self.sudoku.grid[r][c] = value
                        self.sudoku.update_pencil_marks()

                        step = SolveStep(
                            'naked_single',
                            f"Cell ({r+1},{c+1}) can only be {value}",
                            [(r, c)],
                            [value]
                        )
                        self.steps.append(step)
                        self._update_max_technique(1)
                        found = True

        return found

    def _apply_hidden_singles(self) -> bool:
        """Find hidden singles in rows, columns, and boxes"""
        found = False

        # Check rows
        for r in range(9):
            for num in range(1, 10):
                possible_cols = [c for c in range(9)
                                 if self.sudoku.grid[r][c] == 0 and
                                 num in self.sudoku.get_candidates(r, c)]
                if len(possible_cols) == 1:
                    c = possible_cols[0]
                    self.sudoku.grid[r][c] = num
                    self.sudoku.update_pencil_marks()

                    step = SolveStep(
                        'hidden_single',
                        f"In row {r+1}, {num} can only go in cell ({r+1},{c+1})",
                        [(r, c)],
                        [num]
                    )
                    self.steps.append(step)
                    self._update_max_technique(1)
                    found = True

        # Check columns
        for c in range(9):
            for num in range(1, 10):
                possible_rows = [r for r in range(9)
                                 if self.sudoku.grid[r][c] == 0 and
                                 num in self.sudoku.get_candidates(r, c)]
                if len(possible_rows) == 1:
                    r = possible_rows[0]
                    self.sudoku.grid[r][c] = num
                    self.sudoku.update_pencil_marks()

                    step = SolveStep(
                        'hidden_single',
                        f"In column {c+1}, {num} can only go in cell ({r+1},{c+1})",
                        [(r, c)],
                        [num]
                    )
                    self.steps.append(step)
                    self._update_max_technique(1)
                    found = True

        # Check boxes
        for box_idx in range(9):
            box_row, box_col = 3 * (box_idx // 3), 3 * (box_idx % 3)
            for num in range(1, 10):
                possible_cells = []
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        if self.sudoku.grid[r][c] == 0 and \
                           num in self.sudoku.get_candidates(r, c):
                            possible_cells.append((r, c))

                if len(possible_cells) == 1:
                    r, c = possible_cells[0]
                    self.sudoku.grid[r][c] = num
                    self.sudoku.update_pencil_marks()

                    step = SolveStep(
                        'hidden_single',
                        f"In box {box_idx+1}, {num} can only go in cell ({r+1},{c+1})",
                        [(r, c)],
                        [num]
                    )
                    self.steps.append(step)
                    self._update_max_technique(1)
                    found = True

        return found

    def _apply_pointing_pairs(self) -> bool:
        """Apply pointing pairs/triples technique"""
        found = False

        for box_idx in range(9):
            box_row, box_col = 3 * (box_idx // 3), 3 * (box_idx % 3)

            for num in range(1, 10):
                # Find all cells in box where num is possible
                cells_with_num = []
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        if self.sudoku.grid[r][c] == 0 and \
                           num in self.sudoku.get_candidates(r, c):
                            cells_with_num.append((r, c))

                if 2 <= len(cells_with_num) <= 3:
                    # Check if all in same row
                    rows = set(r for r, c in cells_with_num)
                    if len(rows) == 1:
                        row = list(rows)[0]
                        # Remove num from other cells in this row outside the box
                        eliminations = []
                        for c in range(9):
                            if c < box_col or c >= box_col + 3:
                                if self.sudoku.grid[row][c] == 0 and \
                                   num in self.sudoku.pencil_marks[row][c]:
                                    self.sudoku.pencil_marks[row][c].discard(num)
                                    eliminations.append((row, c, {num}))
                                    found = True

                        if eliminations:
                            step = SolveStep(
                                'pointing_pair',
                                f"In box {box_idx+1}, {num} confined to row {row+1}, eliminating from rest of row",
                                cells_with_num,
                                [num],
                                eliminations
                            )
                            self.steps.append(step)
                            self._update_max_technique(2)

                    # Check if all in same column
                    cols = set(c for r, c in cells_with_num)
                    if len(cols) == 1:
                        col = list(cols)[0]
                        # Remove num from other cells in this column outside the box
                        eliminations = []
                        for r in range(9):
                            if r < box_row or r >= box_row + 3:
                                if self.sudoku.grid[r][col] == 0 and \
                                   num in self.sudoku.pencil_marks[r][col]:
                                    self.sudoku.pencil_marks[r][col].discard(num)
                                    eliminations.append((r, col, {num}))
                                    found = True

                        if eliminations:
                            step = SolveStep(
                                'pointing_pair',
                                f"In box {box_idx+1}, {num} confined to column {col+1}, eliminating from rest of column",
                                cells_with_num,
                                [num],
                                eliminations
                            )
                            self.steps.append(step)
                            self._update_max_technique(2)

        return found

    def _apply_box_line_reduction(self) -> bool:
        """Apply box-line reduction technique"""
        found = False

        # Check rows
        for r in range(9):
            for num in range(1, 10):
                cells_with_num = [c for c in range(9)
                                  if self.sudoku.grid[r][c] == 0 and
                                  num in self.sudoku.get_candidates(r, c)]

                if 2 <= len(cells_with_num) <= 3:
                    # Check if all in same box
                    boxes = set(c // 3 for c in cells_with_num)
                    if len(boxes) == 1:
                        box_col = list(boxes)[0] * 3
                        box_row = (r // 3) * 3

                        # Remove num from other cells in this box
                        eliminations = []
                        for br in range(box_row, box_row + 3):
                            if br != r:
                                for bc in range(box_col, box_col + 3):
                                    if self.sudoku.grid[br][bc] == 0 and \
                                       num in self.sudoku.pencil_marks[br][bc]:
                                        self.sudoku.pencil_marks[br][bc].discard(num)
                                        eliminations.append((br, bc, {num}))
                                        found = True

                        if eliminations:
                            step = SolveStep(
                                'box_line_reduction',
                                f"In row {r+1}, {num} confined to box, eliminating from rest of box",
                                [(r, c) for c in cells_with_num],
                                [num],
                                eliminations
                            )
                            self.steps.append(step)
                            self._update_max_technique(2)

        # Check columns
        for c in range(9):
            for num in range(1, 10):
                cells_with_num = [r for r in range(9)
                                  if self.sudoku.grid[r][c] == 0 and
                                  num in self.sudoku.get_candidates(r, c)]

                if 2 <= len(cells_with_num) <= 3:
                    # Check if all in same box
                    boxes = set(r // 3 for r in cells_with_num)
                    if len(boxes) == 1:
                        box_row = list(boxes)[0] * 3
                        box_col = (c // 3) * 3

                        # Remove num from other cells in this box
                        eliminations = []
                        for bc in range(box_col, box_col + 3):
                            if bc != c:
                                for br in range(box_row, box_row + 3):
                                    if self.sudoku.grid[br][bc] == 0 and \
                                       num in self.sudoku.pencil_marks[br][bc]:
                                        self.sudoku.pencil_marks[br][bc].discard(num)
                                        eliminations.append((br, bc, {num}))
                                        found = True

                        if eliminations:
                            step = SolveStep(
                                'box_line_reduction',
                                f"In column {c+1}, {num} confined to box, eliminating from rest of box",
                                [(r, c) for r in cells_with_num],
                                [num],
                                eliminations
                            )
                            self.steps.append(step)
                            self._update_max_technique(2)

        return found

    def _apply_naked_pairs(self) -> bool:
        """Find and apply naked pairs"""
        return self._apply_naked_subset(2, 'naked_pair')

    def _apply_naked_triples(self) -> bool:
        """Find and apply naked triples"""
        return self._apply_naked_subset(3, 'naked_triple')

    def _apply_naked_subset(self, subset_size: int, technique_name: str) -> bool:
        """Generic naked subset finder"""
        found = False

        # Check rows
        for r in range(9):
            cells = [(r, c) for c in range(9) if self.sudoku.grid[r][c] == 0]
            if self._find_naked_subset_in_group(cells, subset_size, technique_name, f"row {r+1}"):
                found = True

        # Check columns
        for c in range(9):
            cells = [(r, c) for r in range(9) if self.sudoku.grid[r][c] == 0]
            if self._find_naked_subset_in_group(cells, subset_size, technique_name, f"column {c+1}"):
                found = True

        # Check boxes
        for box_idx in range(9):
            box_row, box_col = 3 * (box_idx // 3), 3 * (box_idx % 3)
            cells = [(r, c) for r in range(box_row, box_row + 3)
                     for c in range(box_col, box_col + 3)
                     if self.sudoku.grid[r][c] == 0]
            if self._find_naked_subset_in_group(cells, subset_size, technique_name, f"box {box_idx+1}"):
                found = True

        return found

    def _find_naked_subset_in_group(self, cells: List[Tuple[int, int]], subset_size: int,
                                     technique_name: str, group_name: str) -> bool:
        """Find naked subset in a group of cells"""
        from itertools import combinations

        found = False
        n = len(cells)

        if n < subset_size:
            return False

        # Try all combinations of subset_size cells
        for combo in combinations(range(n), subset_size):
            # Get union of candidates in these cells
            union_candidates = set()
            combo_cells = [cells[i] for i in combo]

            for r, c in combo_cells:
                candidates = self.sudoku.get_candidates(r, c)
                if len(candidates) > subset_size:
                    break
                union_candidates.update(candidates)
            else:
                # If union has exactly subset_size candidates, it's a naked subset
                if len(union_candidates) == subset_size:
                    # Remove these candidates from other cells in the group
                    eliminations = []
                    for r, c in cells:
                        if (r, c) not in combo_cells:
                            removed = union_candidates & self.sudoku.pencil_marks[r][c]
                            if removed:
                                self.sudoku.pencil_marks[r][c] -= union_candidates
                                eliminations.append((r, c, removed))
                                found = True

                    if eliminations:
                        step = SolveStep(
                            technique_name,
                            f"In {group_name}, cells {combo_cells} form naked {technique_name.split('_')[1]} with {union_candidates}",
                            combo_cells,
                            list(union_candidates),
                            eliminations
                        )
                        self.steps.append(step)
                        level = self.TECHNIQUE_LEVELS.get(technique_name, 3)
                        self._update_max_technique(level)
                        return True  # Return after first found

        return found

    def _apply_hidden_pairs(self) -> bool:
        """Find and apply hidden pairs"""
        return self._apply_hidden_subset(2, 'hidden_pair')

    def _apply_hidden_triples(self) -> bool:
        """Find and apply hidden triples"""
        return self._apply_hidden_subset(3, 'hidden_triple')

    def _apply_hidden_subset(self, subset_size: int, technique_name: str) -> bool:
        """Generic hidden subset finder"""
        found = False

        # Check rows
        for r in range(9):
            cells = [(r, c) for c in range(9) if self.sudoku.grid[r][c] == 0]
            if self._find_hidden_subset_in_group(cells, subset_size, technique_name, f"row {r+1}"):
                found = True

        # Check columns
        for c in range(9):
            cells = [(r, c) for r in range(9) if self.sudoku.grid[r][c] == 0]
            if self._find_hidden_subset_in_group(cells, subset_size, technique_name, f"column {c+1}"):
                found = True

        # Check boxes
        for box_idx in range(9):
            box_row, box_col = 3 * (box_idx // 3), 3 * (box_idx % 3)
            cells = [(r, c) for r in range(box_row, box_row + 3)
                     for c in range(box_col, box_col + 3)
                     if self.sudoku.grid[r][c] == 0]
            if self._find_hidden_subset_in_group(cells, subset_size, technique_name, f"box {box_idx+1}"):
                found = True

        return found

    def _find_hidden_subset_in_group(self, cells: List[Tuple[int, int]], subset_size: int,
                                      technique_name: str, group_name: str) -> bool:
        """Find hidden subset in a group of cells"""
        from itertools import combinations

        found = False

        # For each combination of subset_size numbers
        for nums in combinations(range(1, 10), subset_size):
            # Find cells where these numbers can go
            cells_for_nums = set()
            for num in nums:
                for r, c in cells:
                    if num in self.sudoku.get_candidates(r, c):
                        cells_for_nums.add((r, c))

            # If exactly subset_size cells contain all these numbers
            if len(cells_for_nums) == subset_size:
                # These numbers are hidden in these cells
                # Remove all other candidates from these cells
                eliminations = []
                for r, c in cells_for_nums:
                    other_candidates = self.sudoku.pencil_marks[r][c] - set(nums)
                    if other_candidates:
                        self.sudoku.pencil_marks[r][c] = set(nums) & self.sudoku.pencil_marks[r][c]
                        eliminations.append((r, c, other_candidates))
                        found = True

                if eliminations:
                    step = SolveStep(
                        technique_name,
                        f"In {group_name}, {nums} form hidden {technique_name.split('_')[1]} in cells {list(cells_for_nums)}",
                        list(cells_for_nums),
                        list(nums),
                        eliminations
                    )
                    self.steps.append(step)
                    level = self.TECHNIQUE_LEVELS.get(technique_name, 3)
                    self._update_max_technique(level)
                    return True

        return found

    def _apply_x_wing(self) -> bool:
        """Apply X-Wing technique"""
        found = False

        # Check for X-Wing in rows
        for num in range(1, 10):
            rows_with_two = []
            for r in range(9):
                cols = [c for c in range(9) if self.sudoku.grid[r][c] == 0 and
                        num in self.sudoku.get_candidates(r, c)]
                if len(cols) == 2:
                    rows_with_two.append((r, cols))

            # Look for two rows with same column positions
            from itertools import combinations
            for (r1, cols1), (r2, cols2) in combinations(rows_with_two, 2):
                if cols1 == cols2:
                    # X-Wing found! Remove num from these columns in other rows
                    eliminations = []
                    for r in range(9):
                        if r != r1 and r != r2:
                            for c in cols1:
                                if self.sudoku.grid[r][c] == 0 and \
                                   num in self.sudoku.pencil_marks[r][c]:
                                    self.sudoku.pencil_marks[r][c].discard(num)
                                    eliminations.append((r, c, {num}))
                                    found = True

                    if eliminations:
                        step = SolveStep(
                            'x_wing',
                            f"X-Wing on {num} in rows {r1+1},{r2+1} and columns {cols1[0]+1},{cols1[1]+1}",
                            [(r1, cols1[0]), (r1, cols1[1]), (r2, cols1[0]), (r2, cols1[1])],
                            [num],
                            eliminations
                        )
                        self.steps.append(step)
                        self._update_max_technique(4)
                        return True

        # Check for X-Wing in columns
        for num in range(1, 10):
            cols_with_two = []
            for c in range(9):
                rows = [r for r in range(9) if self.sudoku.grid[r][c] == 0 and
                        num in self.sudoku.get_candidates(r, c)]
                if len(rows) == 2:
                    cols_with_two.append((c, rows))

            # Look for two columns with same row positions
            from itertools import combinations
            for (c1, rows1), (c2, rows2) in combinations(cols_with_two, 2):
                if rows1 == rows2:
                    # X-Wing found!
                    eliminations = []
                    for c in range(9):
                        if c != c1 and c != c2:
                            for r in rows1:
                                if self.sudoku.grid[r][c] == 0 and \
                                   num in self.sudoku.pencil_marks[r][c]:
                                    self.sudoku.pencil_marks[r][c].discard(num)
                                    eliminations.append((r, c, {num}))
                                    found = True

                    if eliminations:
                        step = SolveStep(
                            'x_wing',
                            f"X-Wing on {num} in columns {c1+1},{c2+1} and rows {rows1[0]+1},{rows1[1]+1}",
                            [(rows1[0], c1), (rows1[1], c1), (rows1[0], c2), (rows1[1], c2)],
                            [num],
                            eliminations
                        )
                        self.steps.append(step)
                        self._update_max_technique(4)
                        return True

        return found

    def _solve_backtrack(self) -> bool:
        """Solve using backtracking algorithm"""
        # Find empty cell
        for r in range(9):
            for c in range(9):
                if self.sudoku.grid[r][c] == 0:
                    # Try each number
                    for num in range(1, 10):
                        if self.sudoku.is_valid_move(r, c, num):
                            self.sudoku.grid[r][c] = num

                            if self._solve_backtrack():
                                return True

                            self.sudoku.grid[r][c] = 0

                    return False

        return True

    def _update_max_technique(self, level: int):
        """Update maximum technique level used"""
        self.max_technique_used = max(self.max_technique_used, level)

    def get_difficulty_rating(self) -> int:
        """Get difficulty rating based on techniques used (1-5)"""
        return self.max_technique_used

    def get_steps(self) -> List[SolveStep]:
        """Get list of solving steps"""
        return self.steps

    def get_hint(self) -> Optional[SolveStep]:
        """Get next logical step as a hint"""
        original_steps = len(self.steps)
        self.sudoku.update_pencil_marks()

        # Try each technique
        techniques = [
            self._apply_naked_singles,
            self._apply_hidden_singles,
            self._apply_pointing_pairs,
            self._apply_box_line_reduction,
            self._apply_naked_pairs,
            self._apply_hidden_pairs,
            self._apply_naked_triples,
            self._apply_hidden_triples,
            self._apply_x_wing,
        ]

        for technique in techniques:
            if technique():
                if len(self.steps) > original_steps:
                    return self.steps[-1]
                break

        return None
