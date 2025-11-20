#!/usr/bin/env python3
"""
Comprehensive Solver Testing and Verification Utility

Tests the solver thoroughly across all difficulty levels to identify issues.

IMPORTANT NOTE ABOUT SOLVER BEHAVIOR:
The SudokuSolver works on an INTERNAL CLONE of the puzzle you pass to it.
When you create a solver with `solver = SudokuSolver(puzzle)`, the solver
creates `self.sudoku = puzzle.clone()` and works on that clone.

This means:
- The original puzzle passed to the solver is NEVER modified
- To check if the solver succeeded, you must check `solver.sudoku.is_solved()`
- NOT `puzzle.is_solved()` (the original puzzle remains unchanged)

This design is intentional to prevent modifying the original puzzle.
"""

import sys
from sudoku_app.core.sudoku import Sudoku
from sudoku_app.core.solver import SudokuSolver
from sudoku_app.core.generator import SudokuGenerator


class SolverTester:
    """Comprehensive solver testing utility"""

    def __init__(self):
        self.generator = SudokuGenerator()
        self.results = {
            'very_easy': [],
            'easy': [],
            'medium': [],
            'hard': [],
            'expert': []
        }

    def test_puzzle(self, puzzle: Sudoku, difficulty: str, puzzle_num: int):
        """Test a single puzzle thoroughly"""
        print(f"\n{'='*80}")
        print(f"Testing {difficulty.upper()} Puzzle #{puzzle_num}")
        print(f"{'='*80}")

        # Count initial clues
        clues = sum(1 for r in range(9) for c in range(9) if puzzle.grid[r][c] != 0)
        print(f"Initial clues: {clues}")

        # Display puzzle
        print("\nPuzzle:")
        print(puzzle)

        # Test 1: Logical solver
        print("\n" + "-"*80)
        print("TEST 1: Logical Solver (step-by-step)")
        print("-"*80)

        logical_puzzle = puzzle.clone()
        logical_solver = SudokuSolver(logical_puzzle)

        logical_success = logical_solver.solve(step_by_step=True)
        steps = logical_solver.get_steps()

        print(f"Logical solve success: {logical_success}")
        print(f"Number of steps: {len(steps)}")
        # IMPORTANT: Check solver.sudoku, not the original puzzle (solver works on a clone)
        print(f"Puzzle solved: {logical_solver.sudoku.is_solved()}")
        print(f"Difficulty rating: {logical_solver.get_difficulty_rating()}")

        if steps:
            print("\nSteps used:")
            technique_counts = {}
            for step in steps:
                technique_counts[step.technique] = technique_counts.get(step.technique, 0) + 1

            for technique, count in sorted(technique_counts.items()):
                print(f"  {technique}: {count} times")

        # Check if logical solver actually filled cells (check solver's internal grid)
        filled_by_logical = sum(1 for r in range(9) for c in range(9) if logical_solver.sudoku.grid[r][c] != 0)
        print(f"\nCells filled by logical solver: {filled_by_logical}/81")

        # Test 2: Backtracking solver
        print("\n" + "-"*80)
        print("TEST 2: Backtracking Solver (instant)")
        print("-"*80)

        backtrack_puzzle = puzzle.clone()
        backtrack_solver = SudokuSolver(backtrack_puzzle)

        backtrack_success = backtrack_solver.solve(step_by_step=False)

        print(f"Backtrack solve success: {backtrack_success}")
        # IMPORTANT: Check solver.sudoku, not the original puzzle
        print(f"Puzzle solved: {backtrack_solver.sudoku.is_solved()}")

        filled_by_backtrack = sum(1 for r in range(9) for c in range(9) if backtrack_solver.sudoku.grid[r][c] != 0)
        print(f"Cells filled by backtracking: {filled_by_backtrack}/81")

        # Comparison
        print("\n" + "-"*80)
        print("COMPARISON")
        print("-"*80)
        print(f"Logical solver: {'✓ SUCCESS' if logical_success and logical_solver.sudoku.is_solved() else '✗ FAILED'}")
        print(f"Backtrack solver: {'✓ SUCCESS' if backtrack_success and backtrack_solver.sudoku.is_solved() else '✗ FAILED'}")

        # Check if they got same solution
        if backtrack_success and logical_success:
            if backtrack_solver.sudoku.grid == logical_solver.sudoku.grid:
                print("Solutions match: ✓")
            else:
                print("Solutions differ: ✗ WARNING")
                print("\nLogical solution:")
                print(logical_solver.sudoku)
                print("\nBacktrack solution:")
                print(backtrack_solver.sudoku)

        # Store results
        result = {
            'puzzle_num': puzzle_num,
            'clues': clues,
            'logical_success': logical_success and logical_solver.sudoku.is_solved(),
            'logical_steps': len(steps),
            'logical_filled': filled_by_logical,
            'backtrack_success': backtrack_success and backtrack_solver.sudoku.is_solved(),
            'backtrack_filled': filled_by_backtrack,
            'difficulty_rating': logical_solver.get_difficulty_rating() if steps else 0,
            'techniques_used': list(technique_counts.keys()) if steps else []
        }

        return result

    def test_difficulty(self, difficulty: str, num_puzzles: int = 3):
        """Test multiple puzzles at a difficulty level"""
        print(f"\n\n{'#'*80}")
        print(f"# TESTING DIFFICULTY: {difficulty.upper()}")
        print(f"# Testing {num_puzzles} puzzles")
        print(f"{'#'*80}")

        for i in range(num_puzzles):
            try:
                print(f"\n\nGenerating {difficulty} puzzle {i+1}/{num_puzzles}...")
                puzzle = self.generator.generate(difficulty)

                result = self.test_puzzle(puzzle, difficulty, i+1)
                self.results[difficulty].append(result)

            except Exception as e:
                print(f"\n✗ ERROR testing puzzle {i+1}: {e}")
                import traceback
                traceback.print_exc()

    def print_summary(self):
        """Print summary of all tests"""
        print(f"\n\n{'='*80}")
        print("SUMMARY OF ALL TESTS")
        print(f"{'='*80}\n")

        for difficulty in ['very_easy', 'easy', 'medium', 'hard', 'expert']:
            results = self.results[difficulty]

            if not results:
                print(f"{difficulty.upper()}: No tests run")
                continue

            print(f"\n{difficulty.upper()}:")
            print("-" * 40)

            total = len(results)
            logical_success = sum(1 for r in results if r['logical_success'])
            backtrack_success = sum(1 for r in results if r['backtrack_success'])

            avg_clues = sum(r['clues'] for r in results) / total
            avg_steps = sum(r['logical_steps'] for r in results) / total
            avg_filled_logical = sum(r['logical_filled'] for r in results) / total
            avg_filled_backtrack = sum(r['backtrack_filled'] for r in results) / total

            print(f"  Puzzles tested: {total}")
            print(f"  Average clues: {avg_clues:.1f}")
            print(f"  Logical solver success: {logical_success}/{total} ({100*logical_success/total:.0f}%)")
            print(f"  Backtrack solver success: {backtrack_success}/{total} ({100*backtrack_success/total:.0f}%)")
            print(f"  Average steps found: {avg_steps:.1f}")
            print(f"  Average cells filled (logical): {avg_filled_logical:.1f}/81")
            print(f"  Average cells filled (backtrack): {avg_filled_backtrack:.1f}/81")

            # Show failures
            logical_failures = [r for r in results if not r['logical_success']]
            if logical_failures:
                print(f"\n  ⚠️  Logical solver FAILURES: {len(logical_failures)}")
                for f in logical_failures:
                    print(f"      Puzzle #{f['puzzle_num']}: {f['logical_filled']}/81 cells filled, {f['logical_steps']} steps")

            backtrack_failures = [r for r in results if not r['backtrack_success']]
            if backtrack_failures:
                print(f"\n  ⚠️  Backtrack solver FAILURES: {len(backtrack_failures)}")

        # Overall summary
        print(f"\n{'='*80}")
        print("OVERALL SUMMARY")
        print(f"{'='*80}")

        all_results = []
        for results in self.results.values():
            all_results.extend(results)

        if all_results:
            total = len(all_results)
            logical_ok = sum(1 for r in all_results if r['logical_success'])
            backtrack_ok = sum(1 for r in all_results if r['backtrack_success'])

            print(f"Total puzzles tested: {total}")
            print(f"Logical solver: {logical_ok}/{total} ({100*logical_ok/total:.0f}%) ✓")
            print(f"Backtrack solver: {backtrack_ok}/{total} ({100*backtrack_ok/total:.0f}%) ✓")

            if logical_ok < total:
                print(f"\n⚠️  WARNING: Logical solver has issues!")
                print(f"   Failed on {total - logical_ok} puzzles")

            if backtrack_ok < total:
                print(f"\n⚠️  CRITICAL: Backtrack solver has issues!")
                print(f"   Failed on {total - backtrack_ok} puzzles")

            if logical_ok == total and backtrack_ok == total:
                print(f"\n✅ ALL SOLVERS WORKING CORRECTLY!")

    def run_quick_test(self):
        """Run a quick test on all difficulties"""
        print("Running QUICK TEST (1 puzzle per difficulty)...\n")
        for difficulty in ['very_easy', 'easy', 'medium', 'hard', 'expert']:
            self.test_difficulty(difficulty, num_puzzles=1)
        self.print_summary()

    def run_thorough_test(self):
        """Run a thorough test on all difficulties"""
        print("Running THOROUGH TEST (3 puzzles per difficulty)...\n")
        for difficulty in ['very_easy', 'easy', 'medium', 'hard', 'expert']:
            self.test_difficulty(difficulty, num_puzzles=3)
        self.print_summary()

    def test_specific_difficulty(self, difficulty: str, num_puzzles: int = 3):
        """Test a specific difficulty level"""
        self.test_difficulty(difficulty, num_puzzles)
        self.print_summary()


def main():
    """Main test runner"""
    print("="*80)
    print("SUDOKU SOLVER TESTING AND VERIFICATION UTILITY")
    print("="*80)

    tester = SolverTester()

    if len(sys.argv) > 1:
        mode = sys.argv[1]

        if mode == 'quick':
            tester.run_quick_test()
        elif mode == 'thorough':
            tester.run_thorough_test()
        elif mode in ['very_easy', 'easy', 'medium', 'hard', 'expert']:
            num = int(sys.argv[2]) if len(sys.argv) > 2 else 3
            tester.test_specific_difficulty(mode, num)
        else:
            print(f"Unknown mode: {mode}")
            print("Usage: python test_solver_thorough.py [quick|thorough|very_easy|easy|medium|hard|expert] [num_puzzles]")
            return 1
    else:
        # Default: quick test
        tester.run_quick_test()

    return 0


if __name__ == "__main__":
    sys.exit(main())
