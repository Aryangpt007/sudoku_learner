#!/usr/bin/env python3
"""
Simple test script to verify core functionality
"""

from sudoku_app.core.sudoku import Sudoku
from sudoku_app.core.solver import SudokuSolver
from sudoku_app.core.generator import SudokuGenerator
from sudoku_app.utils.io_handler import IOHandler


def test_sudoku_basic():
    """Test basic Sudoku functionality"""
    print("Testing Sudoku basic functionality...")

    # Create empty sudoku
    sudoku = Sudoku()
    assert sudoku.grid[0][0] == 0, "Empty grid should have 0s"

    # Test setting a cell
    assert sudoku.set_cell(0, 0, 5) == True, "Should be able to set cell"
    assert sudoku.get_cell(0, 0) == 5, "Cell should contain 5"

    # Test invalid move
    sudoku.set_cell(0, 1, 5)  # Same row, same number
    assert sudoku.is_valid_move(0, 2, 5) == False, "Should detect invalid move"

    print("✓ Basic Sudoku functionality works!")


def test_solver():
    """Test solver with a simple puzzle"""
    print("\nTesting Solver...")

    # Simple puzzle
    grid = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]

    sudoku = Sudoku(grid)
    solver = SudokuSolver(sudoku)

    # Test instant solve
    success = solver.solve(step_by_step=False)
    assert success, "Should solve the puzzle"
    assert solver.sudoku.is_solved(), "Puzzle should be solved"

    print("✓ Solver works!")

    # Test step-by-step solving
    sudoku2 = Sudoku(grid)
    solver2 = SudokuSolver(sudoku2)
    success = solver2.solve(step_by_step=True)

    if success:
        steps = solver2.get_steps()
        print(f"  Found {len(steps)} solving steps")
        if steps:
            print(f"  First technique used: {steps[0].technique}")

    print("✓ Step-by-step solver works!")


def test_generator():
    """Test puzzle generator"""
    print("\nTesting Generator...")

    generator = SudokuGenerator(seed=42)

    # Generate easy puzzle
    sudoku = generator.generate('easy')

    # Count clues
    clues = sum(1 for r in range(9) for c in range(9) if sudoku.grid[r][c] != 0)
    print(f"  Generated puzzle with {clues} clues")

    assert 30 <= clues <= 55, f"Clue count should be reasonable, got {clues}"

    # Verify it's solvable
    solver = SudokuSolver(sudoku.clone())
    success = solver.solve(step_by_step=False)
    assert success, "Generated puzzle should be solvable"

    print("✓ Generator works!")


def test_import_export():
    """Test import/export functionality"""
    print("\nTesting Import/Export...")

    # Create a test puzzle
    grid = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]
    sudoku = Sudoku(grid)

    # Test string conversion
    s = sudoku.to_string()
    assert len(s) == 81, "String should be 81 characters"

    sudoku2 = Sudoku.from_string(s)
    assert sudoku2.grid == sudoku.grid, "Should reconstruct same grid"

    print("✓ String conversion works!")

    # Test JSON export/import
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name

    try:
        IOHandler.export_to_json(sudoku, temp_file)
        sudoku3 = IOHandler.import_from_json(temp_file)
        assert sudoku3.grid == sudoku.grid, "Should import same grid"
        print("✓ JSON import/export works!")
    finally:
        os.unlink(temp_file)


def main():
    """Run all tests"""
    print("=" * 50)
    print("Sudoku Application Core Functionality Tests")
    print("=" * 50)

    try:
        test_sudoku_basic()
        test_solver()
        test_generator()
        test_import_export()

        print("\n" + "=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
        print("\nYou can now run the application with:")
        print("  python main.py")

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
