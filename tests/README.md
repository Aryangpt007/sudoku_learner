# Test Suite

## Quick Start

```bash
# Run all comprehensive tests (30 tests)
python tests/comprehensive_test.py

# Quick solver verification (1 puzzle per difficulty)
python tests/test_solver_thorough.py quick

# Thorough solver verification (3 puzzles per difficulty)
python tests/test_solver_thorough.py thorough

# Test specific difficulty level
python tests/test_solver_thorough.py medium 5

# Test GUI solving behavior
python tests/test_gui_solving.py
```

## Test Files

### comprehensive_test.py
**30 tests covering all core functionality:**
- Sudoku grid operations
- All 9 solving techniques
- Puzzle generation (5 difficulty levels)
- Import/Export functionality
- Grid widget operations

**Usage:** `python tests/comprehensive_test.py`

### test_solver_thorough.py
**Comprehensive solver verification utility:**
- Tests all 5 difficulty levels
- Compares logical vs backtracking solvers
- Shows technique usage statistics
- Verifies 100% success rate

**Usage:**
```bash
python tests/test_solver_thorough.py [quick|thorough|very_easy|easy|medium|hard|expert] [num_puzzles]
```

### test_gui_solving.py
**GUI behavior simulation tests:**
- Tests instant solve (backtracking)
- Tests step-by-step solve (logical + backtracking)
- Verifies complete solution display
- Tests set_cell functionality

**Usage:** `python tests/test_gui_solving.py`

### test_core.py
**Core module unit tests:**
- Basic Sudoku operations
- Grid validation
- Cell setting
- Candidate calculation

**Usage:** `python tests/test_core.py`

## Expected Results

All tests should pass with 100% success rate:
- ✅ 30/30 comprehensive tests
- ✅ 15/15 solver verification (3 per difficulty × 5 difficulties)
- ✅ 3/3 GUI behavior tests
- ✅ All core unit tests

## Test Results

See [../TESTING.md](../TESTING.md) for detailed test results and bug fix documentation.
