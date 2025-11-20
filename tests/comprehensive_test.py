"""
Comprehensive Code Review and Bug Check
Run this to test all major functionalities
"""

import sys
from sudoku_app.core.sudoku import Sudoku
from sudoku_app.core.solver import SudokuSolver
from sudoku_app.core.generator import SudokuGenerator
from sudoku_app.utils.io_handler import IOHandler
import tempfile
import os

print("="*70)
print("COMPREHENSIVE CODE REVIEW AND BUG CHECK")
print("="*70)

errors_found = []
warnings_found = []
tests_passed = 0
tests_failed = 0

def test_section(name):
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print("="*70)

def report_error(msg):
    global tests_failed
    errors_found.append(msg)
    tests_failed += 1
    print(f"❌ ERROR: {msg}")

def report_warning(msg):
    warnings_found.append(msg)
    print(f"⚠️  WARNING: {msg}")

def report_pass(msg):
    global tests_passed
    tests_passed += 1
    print(f"✓ {msg}")

# Test 1: Sudoku Core
test_section("Sudoku Core Functionality")
try:
    sudoku = Sudoku()
    sudoku.set_cell(0, 0, 5)
    assert sudoku.get_cell(0, 0) == 5
    report_pass("Cell setting and getting works")

    # Test validation
    sudoku.set_cell(0, 1, 5)
    if not sudoku.is_valid_move(0, 2, 5):
        report_pass("Validation correctly detects invalid moves")
    else:
        report_error("Validation failed to detect invalid move")

    # Test pencil marks
    sudoku2 = Sudoku()
    sudoku2.update_pencil_marks()
    marks = sudoku2.get_pencil_marks(0, 0)
    if len(marks) == 9:
        report_pass("Pencil marks initialized correctly")
    else:
        report_error(f"Pencil marks incorrect: expected 9, got {len(marks)}")

    # Test is_complete and is_solved
    if not sudoku.is_complete():
        report_pass("is_complete() works correctly")
    else:
        report_error("is_complete() returned true for incomplete puzzle")

except Exception as e:
    report_error(f"Sudoku core test failed: {e}")

# Test 2: Solver Techniques
test_section("Solver Techniques")
try:
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
    if solver.solve(step_by_step=False):
        if solver.sudoku.is_solved():
            report_pass("Instant solve works correctly")
        else:
            report_error("Solver finished but puzzle not solved")
    else:
        report_error("Solver failed to solve puzzle")

    # Test step-by-step solve
    sudoku2 = Sudoku(grid)
    solver2 = SudokuSolver(sudoku2)
    if solver2.solve(step_by_step=True):
        steps = solver2.get_steps()
        if len(steps) > 0:
            report_pass(f"Step-by-step solver found {len(steps)} steps")

            # Check if steps have required attributes
            step = steps[0]
            if hasattr(step, 'technique') and hasattr(step, 'description'):
                report_pass("Step objects have correct attributes")
            else:
                report_error("Step objects missing required attributes")
        else:
            report_warning("Step-by-step solver completed but no steps recorded")
    else:
        report_error("Step-by-step solver failed")

    # Test hint system
    sudoku3 = Sudoku(grid)
    solver3 = SudokuSolver(sudoku3)
    hint = solver3.get_hint()
    if hint:
        report_pass("Hint system works")
    else:
        report_warning("Hint system returned None (might be ok for some puzzles)")

except Exception as e:
    report_error(f"Solver test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Generator
test_section("Puzzle Generator")
try:
    gen = SudokuGenerator(seed=12345)

    difficulties = ['very_easy', 'easy', 'medium', 'hard', 'expert']
    for diff in difficulties:
        try:
            puzzle = gen.generate(diff)
            clues = sum(1 for r in range(9) for c in range(9) if puzzle.grid[r][c] != 0)

            # Check clue count is reasonable
            if 20 <= clues <= 55:
                report_pass(f"{diff}: generated {clues} clues")
            else:
                report_warning(f"{diff}: unusual clue count {clues}")

            # Verify puzzle is solvable
            solver = SudokuSolver(puzzle.clone())
            if solver.solve(step_by_step=False):
                if solver.sudoku.is_solved():
                    report_pass(f"{diff}: puzzle is solvable")
                else:
                    report_error(f"{diff}: solver finished but not solved")
            else:
                report_error(f"{diff}: generated puzzle not solvable")

        except Exception as e:
            report_error(f"Generator failed for {diff}: {e}")

except Exception as e:
    report_error(f"Generator test failed: {e}")

# Test 4: Import/Export
test_section("Import/Export Functionality")
try:
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
    if len(s) == 81:
        report_pass("to_string() produces 81-character string")
    else:
        report_error(f"to_string() produced {len(s)} characters")

    sudoku2 = Sudoku.from_string(s)
    if sudoku2.grid == sudoku.grid:
        report_pass("from_string() reconstructs grid correctly")
    else:
        report_error("from_string() failed to reconstruct grid")

    # Test JSON export/import
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_json = f.name

    try:
        IOHandler.export_to_json(sudoku, temp_json, include_solution=False)
        report_pass("JSON export successful")

        sudoku3 = IOHandler.import_from_json(temp_json)
        if sudoku3.grid == sudoku.grid:
            report_pass("JSON import successful")
        else:
            report_error("JSON import produced different grid")
    finally:
        os.unlink(temp_json)

    # Test SDK format
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sdk', delete=False) as f:
        temp_sdk = f.name

    try:
        IOHandler.export_to_sdk(sudoku, temp_sdk)
        report_pass("SDK export successful")

        sudoku4 = IOHandler.import_from_sdk(temp_sdk)
        if sudoku4.grid == sudoku.grid:
            report_pass("SDK import successful")
        else:
            report_error("SDK import produced different grid")
    finally:
        os.unlink(temp_sdk)

except Exception as e:
    report_error(f"Import/Export test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Edge Cases
test_section("Edge Cases and Error Handling")
try:
    # Test empty grid
    empty = Sudoku()
    if empty.get_candidates(0, 0) == set(range(1, 10)):
        report_pass("Empty grid candidates correct")
    else:
        report_error("Empty grid candidates incorrect")

    # Test invalid string import
    try:
        invalid = Sudoku.from_string("12345")  # Too short
        report_error("Should reject invalid string length")
    except ValueError:
        report_pass("Correctly rejects invalid string length")

    # Test cell boundary checking
    sudoku = Sudoku()
    try:
        # These should work
        sudoku.is_valid_move(0, 0, 5)
        sudoku.is_valid_move(8, 8, 5)
        report_pass("Boundary cells accessible")
    except Exception as e:
        report_error(f"Boundary check failed: {e}")

    # Test clone functionality
    grid = [[i+j for j in range(9)] for i in range(9)]
    grid[0][0] = 5
    s1 = Sudoku(grid)
    s2 = s1.clone()
    s2.grid[0][0] = 9
    if s1.grid[0][0] == 5 and s2.grid[0][0] == 9:
        report_pass("Clone creates independent copy")
    else:
        report_error("Clone may share data with original")

except Exception as e:
    report_error(f"Edge case test failed: {e}")

# Test 6: Performance Check
test_section("Performance Check")
try:
    import time

    # Generator performance
    gen = SudokuGenerator(seed=999)
    start = time.time()
    puzzle = gen.generate('easy')
    elapsed = time.time() - start

    if elapsed < 10:
        report_pass(f"Generator completed in {elapsed:.2f}s (good)")
    elif elapsed < 30:
        report_warning(f"Generator took {elapsed:.2f}s (acceptable but slow)")
    else:
        report_warning(f"Generator took {elapsed:.2f}s (very slow)")

    # Solver performance
    start = time.time()
    solver = SudokuSolver(puzzle)
    solver.solve(step_by_step=False)
    elapsed = time.time() - start

    if elapsed < 1:
        report_pass(f"Solver completed in {elapsed:.3f}s (excellent)")
    elif elapsed < 5:
        report_pass(f"Solver completed in {elapsed:.2f}s (good)")
    else:
        report_warning(f"Solver took {elapsed:.2f}s (slow)")

except Exception as e:
    report_error(f"Performance test failed: {e}")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Tests Passed: {tests_passed}")
print(f"Tests Failed: {tests_failed}")
print(f"Errors Found: {len(errors_found)}")
print(f"Warnings: {len(warnings_found)}")

if errors_found:
    print("\n❌ ERRORS FOUND:")
    for i, error in enumerate(errors_found, 1):
        print(f"  {i}. {error}")

if warnings_found:
    print("\n⚠️  WARNINGS:")
    for i, warning in enumerate(warnings_found, 1):
        print(f"  {i}. {warning}")

if not errors_found:
    print("\n✅ All critical functionality working correctly!")
    print("The application is ready to use.")
else:
    print(f"\n⚠️  Found {len(errors_found)} critical issues that need attention.")

print("\n" + "="*70)
sys.exit(0 if not errors_found else 1)
