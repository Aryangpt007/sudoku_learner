"""
Import/Export functionality for Sudoku puzzles
"""

import json
from typing import Dict, Any
from ..core.sudoku import Sudoku


class IOHandler:
    """Handles import and export of Sudoku puzzles"""

    @staticmethod
    def export_to_json(sudoku: Sudoku, filepath: str, include_solution: bool = False):
        """
        Export Sudoku to JSON file

        Args:
            sudoku: Sudoku puzzle to export
            filepath: Path to save file
            include_solution: Whether to include the solution
        """
        data = {
            'grid': [row[:] for row in sudoku.grid],
            'initial_cells': list(sudoku.initial_cells),
        }

        if include_solution:
            # Solve to get solution
            from ..core.solver import SudokuSolver
            solver_sudoku = sudoku.clone()
            solver = SudokuSolver(solver_sudoku)
            solver.solve(step_by_step=False)
            data['solution'] = [row[:] for row in solver_sudoku.grid]

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def import_from_json(filepath: str) -> Sudoku:
        """
        Import Sudoku from JSON file

        Args:
            filepath: Path to JSON file

        Returns:
            Sudoku puzzle
        """
        with open(filepath, 'r') as f:
            data = json.load(f)

        grid = data['grid']
        sudoku = Sudoku(grid)

        if 'initial_cells' in data:
            sudoku.initial_cells = set(tuple(cell) for cell in data['initial_cells'])

        sudoku.update_pencil_marks()
        return sudoku

    @staticmethod
    def export_to_text(sudoku: Sudoku, filepath: str):
        """
        Export Sudoku to simple text file (81 characters)

        Args:
            sudoku: Sudoku puzzle to export
            filepath: Path to save file
        """
        with open(filepath, 'w') as f:
            f.write(sudoku.to_string())
            f.write('\n')

    @staticmethod
    def import_from_text(filepath: str) -> Sudoku:
        """
        Import Sudoku from text file

        Args:
            filepath: Path to text file

        Returns:
            Sudoku puzzle
        """
        with open(filepath, 'r') as f:
            line = f.read().strip()

        return Sudoku.from_string(line)

    @staticmethod
    def export_to_sdk(sudoku: Sudoku, filepath: str):
        """
        Export to .sdk format (simple text format used by many Sudoku programs)

        Args:
            sudoku: Sudoku puzzle to export
            filepath: Path to save file
        """
        with open(filepath, 'w') as f:
            for r in range(9):
                for c in range(9):
                    val = sudoku.grid[r][c]
                    f.write(str(val) if val != 0 else '.')
                f.write('\n')

    @staticmethod
    def import_from_sdk(filepath: str) -> Sudoku:
        """
        Import from .sdk format

        Args:
            filepath: Path to .sdk file

        Returns:
            Sudoku puzzle
        """
        grid = []
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) == 9:
                    row = [int(c) if c.isdigit() and c != '0' else 0 for c in line]
                    grid.append(row)

        if len(grid) != 9:
            raise ValueError("Invalid .sdk file format")

        return Sudoku(grid)

    @staticmethod
    def detect_format(filepath: str) -> str:
        """
        Detect file format from extension

        Args:
            filepath: Path to file

        Returns:
            Format name ('json', 'text', or 'sdk')
        """
        if filepath.endswith('.json'):
            return 'json'
        elif filepath.endswith('.sdk'):
            return 'sdk'
        else:
            return 'text'

    @staticmethod
    def import_puzzle(filepath: str) -> Sudoku:
        """
        Import puzzle with automatic format detection

        Args:
            filepath: Path to file

        Returns:
            Sudoku puzzle
        """
        format_type = IOHandler.detect_format(filepath)

        if format_type == 'json':
            return IOHandler.import_from_json(filepath)
        elif format_type == 'sdk':
            return IOHandler.import_from_sdk(filepath)
        else:
            return IOHandler.import_from_text(filepath)

    @staticmethod
    def export_puzzle(sudoku: Sudoku, filepath: str, include_solution: bool = False):
        """
        Export puzzle with automatic format detection

        Args:
            sudoku: Sudoku puzzle to export
            filepath: Path to save file
            include_solution: Whether to include solution (JSON only)
        """
        format_type = IOHandler.detect_format(filepath)

        if format_type == 'json':
            IOHandler.export_to_json(sudoku, filepath, include_solution)
        elif format_type == 'sdk':
            IOHandler.export_to_sdk(sudoku, filepath)
        else:
            IOHandler.export_to_text(sudoku, filepath)
