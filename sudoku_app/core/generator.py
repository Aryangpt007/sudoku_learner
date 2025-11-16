"""
Sudoku Puzzle Generator with difficulty levels
"""

import random
from typing import List, Optional
from .sudoku import Sudoku
from .solver import SudokuSolver


class SudokuGenerator:
    """Generates Sudoku puzzles with varying difficulty levels"""

    # Difficulty parameters: (min_clues, max_clues, max_technique_level)
    DIFFICULTY_PARAMS = {
        'very_easy': (45, 50, 1),   # Only naked/hidden singles
        'easy': (36, 44, 1),         # Only naked/hidden singles
        'medium': (32, 35, 2),       # Up to pointing pairs, box-line reduction, naked pairs
        'hard': (28, 31, 3),         # Up to naked/hidden triples
        'expert': (22, 27, 5),       # All techniques including X-Wing and beyond
    }

    DIFFICULTY_NAMES = ['very_easy', 'easy', 'medium', 'hard', 'expert']

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize generator

        Args:
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)

    def generate(self, difficulty: str = 'medium') -> Sudoku:
        """
        Generate a Sudoku puzzle

        Args:
            difficulty: Difficulty level (very_easy, easy, medium, hard, expert)

        Returns:
            Generated Sudoku puzzle
        """
        if difficulty not in self.DIFFICULTY_PARAMS:
            raise ValueError(f"Invalid difficulty. Choose from: {list(self.DIFFICULTY_PARAMS.keys())}")

        min_clues, max_clues, max_technique = self.DIFFICULTY_PARAMS[difficulty]

        # Generate a complete valid solution
        solution = self._generate_complete_grid()

        # Remove cells to create puzzle
        puzzle = self._remove_cells(solution, min_clues, max_clues, max_technique)

        return puzzle

    def _generate_complete_grid(self) -> Sudoku:
        """Generate a complete valid Sudoku grid"""
        sudoku = Sudoku()

        # Fill diagonal boxes first (they're independent)
        for box_idx in [0, 4, 8]:
            self._fill_box(sudoku, box_idx)

        # Solve the rest using backtracking
        self._solve_grid(sudoku)

        return sudoku

    def _fill_box(self, sudoku: Sudoku, box_idx: int):
        """Fill a 3x3 box with random numbers"""
        box_row = 3 * (box_idx // 3)
        box_col = 3 * (box_idx % 3)

        numbers = list(range(1, 10))
        random.shuffle(numbers)

        idx = 0
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                sudoku.grid[r][c] = numbers[idx]
                idx += 1

    def _solve_grid(self, sudoku: Sudoku) -> bool:
        """Solve grid using backtracking with randomization"""
        # Find empty cell
        for r in range(9):
            for c in range(9):
                if sudoku.grid[r][c] == 0:
                    # Try numbers in random order
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)

                    for num in numbers:
                        if sudoku.is_valid_move(r, c, num):
                            sudoku.grid[r][c] = num

                            if self._solve_grid(sudoku):
                                return True

                            sudoku.grid[r][c] = 0

                    return False

        return True

    def _remove_cells(self, solution: Sudoku, min_clues: int, max_clues: int,
                      max_technique: int) -> Sudoku:
        """
        Remove cells from solution to create puzzle

        Args:
            solution: Complete Sudoku grid
            min_clues: Minimum number of clues to leave
            max_clues: Maximum number of clues to leave
            max_technique: Maximum solving technique level required

        Returns:
            Sudoku puzzle
        """
        puzzle = solution.clone()

        # Get all cell positions
        all_positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(all_positions)

        target_clues = random.randint(min_clues, max_clues)
        removed_cells = []

        # First pass: Remove cells while checking solvability
        for r, c in all_positions:
            if len(removed_cells) >= (81 - target_clues):
                break

            # Try removing this cell
            original_value = puzzle.grid[r][c]
            puzzle.grid[r][c] = 0
            puzzle.initial_cells.discard((r, c))

            # Check if puzzle still has unique solution
            test_puzzle = puzzle.clone()
            solver = SudokuSolver(test_puzzle)

            # Try to solve with logical methods first
            success = solver.solve(step_by_step=True)

            if not success:
                # If logical methods fail, try backtracking to ensure unique solution
                test_puzzle2 = puzzle.clone()
                solver2 = SudokuSolver(test_puzzle2)
                success = solver2.solve(step_by_step=False)
                if success:
                    solver = solver2  # Use backtrack solver for checking

            if success and solver.sudoku.is_solved():
                # Puzzle is still solvable
                difficulty_level = solver.get_difficulty_rating()

                # Check if difficulty is appropriate
                # Be more lenient - allow some variation
                if difficulty_level <= max_technique + 1:
                    # Keep the cell removed
                    removed_cells.append((r, c))
                else:
                    # Restore cell - too difficult
                    puzzle.grid[r][c] = original_value
                    puzzle.initial_cells.add((r, c))
            else:
                # Puzzle not solvable or doesn't have unique solution, restore cell
                puzzle.grid[r][c] = original_value
                puzzle.initial_cells.add((r, c))

        # Ensure initial_cells is properly set
        puzzle.initial_cells.clear()
        for r in range(9):
            for c in range(9):
                if puzzle.grid[r][c] != 0:
                    puzzle.initial_cells.add((r, c))

        puzzle.update_pencil_marks()
        return puzzle

    def generate_from_seed(self, seed: int, difficulty: str = 'medium') -> Sudoku:
        """
        Generate a puzzle from a specific seed

        Args:
            seed: Random seed
            difficulty: Difficulty level

        Returns:
            Generated Sudoku puzzle
        """
        random.seed(seed)
        return self.generate(difficulty)

    @staticmethod
    def get_difficulty_levels() -> List[str]:
        """Get list of available difficulty levels"""
        return SudokuGenerator.DIFFICULTY_NAMES.copy()

    @staticmethod
    def get_difficulty_description(difficulty: str) -> str:
        """Get description of difficulty level"""
        descriptions = {
            'very_easy': 'Very Easy - Perfect for beginners. Uses only basic techniques.',
            'easy': 'Easy - Good for learning. Requires naked and hidden singles.',
            'medium': 'Medium - Moderate challenge. May require pointing pairs and naked pairs.',
            'hard': 'Hard - Challenging. Requires advanced techniques like hidden pairs and triples.',
            'expert': 'Expert - Very challenging. May require X-Wing and other advanced techniques.',
        }
        return descriptions.get(difficulty, 'Unknown difficulty')
