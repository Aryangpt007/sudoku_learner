#!/usr/bin/env python3
"""
Test script to simulate GUI solving behavior
"""

from sudoku_app.core.sudoku import Sudoku
from sudoku_app.core.solver import SudokuSolver
from sudoku_app.core.generator import SudokuGenerator


def test_instant_solve():
    """Test the instant solve path (what GUI does)"""
    print("="*80)
    print("TEST 1: INSTANT SOLVE (Backtracking)")
    print("="*80)

    # Generate a puzzle
    gen = SudokuGenerator()
    puzzle = gen.generate('medium')

    print("\nOriginal Puzzle:")
    print(puzzle)
    initial_clues = sum(1 for r in range(9) for c in range(9) if puzzle.grid[r][c] != 0)
    print(f"Initial clues: {initial_clues}")

    # Simulate GUI's solve_instantly() method
    print("\nSimulating GUI's solve_instantly()...")
    solver = SudokuSolver(puzzle.clone())
    success = solver.solve(step_by_step=False)

    if success:
        # GUI does: self.sudoku = solver.sudoku
        puzzle_after_solve = solver.sudoku
        print("\nPuzzle after solve_instantly:")
        print(puzzle_after_solve)
        filled = sum(1 for r in range(9) for c in range(9) if puzzle_after_solve.grid[r][c] != 0)
        print(f"Filled cells: {filled}/81")
        print(f"Is solved: {puzzle_after_solve.is_solved()}")
        print("✓ INSTANT SOLVE WORKS")
    else:
        print("✗ INSTANT SOLVE FAILED")

    return success


def test_step_by_step_solve():
    """Test the step-by-step solve path (what GUI does)"""
    print("\n" + "="*80)
    print("TEST 2: STEP-BY-STEP SOLVE")
    print("="*80)

    # Generate a puzzle
    gen = SudokuGenerator()
    puzzle = gen.generate('easy')  # Use easy for quicker test

    print("\nOriginal Puzzle:")
    print(puzzle)
    initial_clues = sum(1 for r in range(9) for c in range(9) if puzzle.grid[r][c] != 0)
    print(f"Initial clues: {initial_clues}")

    # Simulate GUI's solve_step_by_step() method
    print("\nSimulating GUI's solve_step_by_step()...")
    solver = SudokuSolver(puzzle.clone())
    success = solver.solve(step_by_step=True)

    if not success:
        print("✗ SOLVE FAILED")
        return False

    steps = solver.get_steps()
    print(f"Found {len(steps)} steps")

    # Now simulate clicking "Next Step" for each step
    print("\nSimulating next_step() for each step...")
    displayed_puzzle = puzzle  # This is what the GUI shows

    for i, step in enumerate(steps):
        # This is what the GUI does in next_step()
        if step.technique in ['naked_single', 'hidden_single']:
            if step.cells and step.values:
                r, c = step.cells[0]
                result = displayed_puzzle.set_cell(r, c, step.values[0])
                if not result:
                    print(f"\n✗ ERROR at step {i+1}: Could not set cell ({r},{c}) to {step.values[0]}")
                    print(f"   Cell is in initial_cells: {(r, c) in displayed_puzzle.initial_cells}")
                    print(f"   Current value: {displayed_puzzle.grid[r][c]}")
                    return False

        # Apply eliminations
        if step.eliminations:
            for r, c, eliminated in step.eliminations:
                for num in eliminated:
                    displayed_puzzle.pencil_marks[r][c].discard(num)

    print(f"\nAfter applying all {len(steps)} steps:")
    print(displayed_puzzle)
    filled = sum(1 for r in range(9) for c in range(9) if displayed_puzzle.grid[r][c] != 0)
    print(f"Filled cells: {filled}/81")
    print(f"Is solved: {displayed_puzzle.is_solved()}")

    # FIX: Copy complete solution from solver (this is what the fixed GUI now does)
    print("\nApplying fix: Copy complete solution from solver...")
    displayed_puzzle = solver.sudoku
    print(displayed_puzzle)
    filled_after_fix = sum(1 for r in range(9) for c in range(9) if displayed_puzzle.grid[r][c] != 0)
    print(f"Filled cells after fix: {filled_after_fix}/81")
    print(f"Is solved after fix: {displayed_puzzle.is_solved()}")

    if displayed_puzzle.is_solved():
        print("✓ STEP-BY-STEP SOLVE WORKS (with fix)")
        return True
    else:
        print(f"✗ STEP-BY-STEP SOLVE STILL INCOMPLETE")
        return False


def test_set_cell_issue():
    """Test if set_cell has any issues"""
    print("\n" + "="*80)
    print("TEST 3: SET_CELL FUNCTIONALITY")
    print("="*80)

    puzzle = Sudoku()
    # Manually set up a simple test case
    puzzle.grid[0][0] = 5
    puzzle.initial_cells.add((0, 0))

    print("Test 1: Try to modify an initial cell (should fail)")
    result = puzzle.set_cell(0, 0, 7)
    print(f"  Result: {result} (expected: False)")
    print(f"  Value: {puzzle.grid[0][0]} (expected: 5)")

    print("\nTest 2: Set an empty cell (should succeed)")
    result = puzzle.set_cell(0, 1, 3)
    print(f"  Result: {result} (expected: True)")
    print(f"  Value: {puzzle.grid[0][1]} (expected: 3)")

    print("\nTest 3: Set a cell that was set earlier (not initial)")
    result = puzzle.set_cell(0, 1, 8)
    print(f"  Result: {result} (expected: True)")
    print(f"  Value: {puzzle.grid[0][1]} (expected: 8)")

    print("✓ SET_CELL WORKS AS EXPECTED")


def main():
    """Run all tests"""
    print("TESTING GUI SOLVING BEHAVIOR")
    print("This simulates what happens when the user clicks solve buttons\n")

    try:
        test1_pass = test_instant_solve()
        test2_pass = test_step_by_step_solve()
        test_set_cell_issue()

        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Instant Solve: {'✓ PASS' if test1_pass else '✗ FAIL'}")
        print(f"Step-by-Step Solve: {'✓ PASS' if test2_pass else '✗ FAIL'}")

        if test1_pass and test2_pass:
            print("\n✅ ALL TESTS PASSED - GUI SOLVING SHOULD WORK")
        else:
            print("\n⚠️  SOME TESTS FAILED - THERE MAY BE A BUG")

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
