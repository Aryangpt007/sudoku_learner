# Sudoku Learning Application

A comprehensive Sudoku application built in Python with Tkinter, featuring an intelligent solver, puzzle generator, and interactive teaching module.

## Features

### 1. Five Difficulty Levels
Generate puzzles with five different difficulty levels:
- **Very Easy**: 45-50 clues, only basic techniques required
- **Easy**: 36-44 clues, naked and hidden singles
- **Medium**: 32-35 clues, requires pointing pairs and naked pairs
- **Hard**: 28-31 clues, requires advanced techniques like hidden pairs and triples
- **Expert**: 22-27 clues, may require X-Wing and other advanced techniques

### 2. Interactive Solving Area
- **Grid Interface**: Clean 9x9 Sudoku grid with visual separation of 3x3 boxes
- **Pencil Marking**: Toggle pencil mode to add candidate notes (1-9) to cells
- **Auto-fill Pencil Marks**: Automatically calculate and fill all possible candidates
- **Cell Navigation**: Click cells or use arrow keys to navigate
- **Input Validation**: Visual feedback for valid/invalid moves
- **Initial Cell Protection**: Original clues are locked and visually distinguished

### 3. Import/Export Functionality
Import and export puzzles in multiple formats:
- **JSON Format** (`.json`): Full puzzle data with optional solution
- **SDK Format** (`.sdk`): Standard Sudoku file format
- **Text Format** (`.txt`): Simple 81-character string representation

### 4. AI Sudoku Solver
Powerful solver implementing multiple techniques:

#### Solving Techniques Implemented:
1. **Naked Singles** (Level 1): Cells with only one possible value
2. **Hidden Singles** (Level 1): Numbers that can only go in one cell
3. **Pointing Pairs/Triples** (Level 2): Box-line intersections
4. **Box-Line Reduction** (Level 2): Line-box intersections
5. **Naked Pairs** (Level 2): Two cells sharing two candidates
6. **Hidden Pairs** (Level 2): Two numbers confined to two cells
7. **Naked Triples** (Level 3): Three cells sharing three candidates
8. **Hidden Triples** (Level 3): Three numbers confined to three cells
9. **X-Wing** (Level 4): Advanced pattern-based elimination

#### Solver Modes:
- **Step-by-Step Mode**: Shows each solving technique used with detailed explanations
- **Instant Solve**: Solves the entire puzzle immediately
- **Get Hint**: Provides the next logical move with explanation
- **Technique Display**: Each step shows which technique was used and why

### 5. Teaching Module
Comprehensive interactive learning system:
- **10 Progressive Lessons**: From beginner to advanced techniques
- **Detailed Explanations**: Each technique explained with theory and examples
- **Visual Examples**: Clear illustrations of pattern recognition
- **Practice Tips**: Specific guidance for finding each technique
- **Difficulty Progression**: Learn techniques in order of complexity
- **Easy Navigation**: Jump to any lesson or progress sequentially

## Installation

### Requirements
- Python 3.7 or higher
- tkinter (usually included with Python)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/Aryangpt007/sudoku_learner.git
cd sudoku_learner
```

2. No additional packages needed! The app uses only Python standard library.

3. Run the application:
```bash
python main.py
```

Or make it executable:
```bash
chmod +x main.py
./main.py
```

## Usage Guide

### Generating Puzzles
1. Select difficulty level from the right panel
2. Click "Generate New Puzzle"
3. Or use Menu → File → New Puzzle

### Playing
1. **Select a cell**: Click with mouse or use arrow keys
2. **Enter a number**: Type 1-9 to fill a cell
3. **Clear a cell**: Press 0, Delete, or Backspace
4. **Pencil marks**:
   - Enable "Pencil Mode" checkbox
   - Type numbers to toggle candidate marks
   - Disable to return to normal entry mode

### Using the Solver
1. **Get a Hint**: Shows the next logical move
2. **Step-by-Step Solve**:
   - Click to analyze the puzzle
   - Use "Next Step" to see each technique
   - View detailed explanations in the text area
3. **Instant Solve**: Solves the entire puzzle at once

### Learning Techniques
1. Open Menu → Help → Learning Module
2. Start with "Introduction" lesson
3. Progress through techniques in order
4. Use "Next" and "Previous" to navigate
5. Jump to specific lessons using the dropdown

### Import/Export
**Import**:
- Menu → File → Import Puzzle
- Select .json, .sdk, or .txt file
- Puzzle loads into the grid

**Export**:
- Menu → File → Export Puzzle
- Choose format and location
- Optional: Include solution (JSON only)

## Project Structure

```
sudoku_learner/
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies (none needed!)
├── README.md              # This file
└── sudoku_app/            # Main package
    ├── __init__.py
    ├── core/              # Core logic
    │   ├── __init__.py
    │   ├── sudoku.py      # Sudoku data structure and validation
    │   ├── solver.py      # AI solver with multiple techniques
    │   └── generator.py   # Puzzle generator with difficulty levels
    ├── gui/               # User interface
    │   ├── __init__.py
    │   ├── main_window.py # Main application window
    │   ├── grid.py        # Interactive Sudoku grid widget
    │   └── teaching.py    # Teaching module window
    └── utils/             # Utilities
        ├── __init__.py
        └── io_handler.py  # Import/export functionality
```

## Technical Details

### Sudoku Generation Algorithm
1. Generate complete valid solution using backtracking with randomization
2. Remove cells strategically based on difficulty parameters
3. Verify puzzle has unique solution using logical solver
4. Ensure required technique level matches difficulty

### Solver Implementation
- **Logical Solver**: Uses human-like solving techniques
- **Backtracking Solver**: For instant solving or when logic fails
- **Step Recording**: Tracks each technique application for teaching
- **Candidate Management**: Maintains pencil marks for logical deduction

### GUI Architecture
- **Tkinter-based**: Cross-platform compatibility
- **Canvas Grid**: Custom-drawn Sudoku grid with highlighting
- **Event Handling**: Mouse and keyboard input support
- **Real-time Validation**: Immediate feedback on moves

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| 1-9 | Enter number (or toggle pencil mark in pencil mode) |
| 0, Delete, Backspace | Clear cell |
| Arrow Keys | Navigate between cells |
| Mouse Click | Select cell |

## File Formats

### JSON Format
```json
{
  "grid": [[0,0,3,...], ...],
  "initial_cells": [[0,2], [0,5], ...],
  "solution": [[1,2,3,...], ...]  // Optional
}
```

### SDK Format
```
..3.2.6..
9..3.5..1
..18.64..
...
```

### Text Format
```
003020600900305001001806400...
```

## Tips for Players

### Beginners
1. Start with "Very Easy" or "Easy" difficulty
2. Use pencil marks to track candidates
3. Complete the Teaching Module lessons in order
4. Focus on mastering Naked and Hidden Singles first
5. Use "Auto-fill Pencil Marks" to see all possibilities

### Intermediate
1. Practice "Medium" and "Hard" puzzles
2. Learn to spot Pointing Pairs and Box-Line Reduction
3. Study the step-by-step solver to see techniques in action
4. Try to solve without hints, use hints when stuck

### Advanced
1. Challenge yourself with "Expert" puzzles
2. Master advanced techniques like X-Wing
3. Try to minimize hint usage
4. Race against the step-by-step solver

## Educational Use

This application is perfect for:
- **Learning Sudoku**: Comprehensive teaching module
- **Teaching Logic**: Demonstrates logical deduction
- **Computer Science Education**: Example of AI, algorithms, and GUI programming
- **Personal Improvement**: Track progress through difficulty levels

## Contributing

Contributions are welcome! Areas for enhancement:
- Additional solving techniques (Swordfish, Jellyfish, Coloring, etc.)
- Puzzle database with rated difficulties
- Timer and statistics tracking
- Hints with visual highlighting
- Mobile-friendly version
- Alternative grid sizes (4x4, 16x16)

## License

See LICENSE file for details.

## Acknowledgments

- Sudoku puzzle logic based on standard Sudoku rules
- Solving techniques from the Sudoku community
- Built with Python and Tkinter

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the Teaching Module for gameplay help
- Review this README for technical details

---

**Enjoy learning and playing Sudoku!** 🎯
