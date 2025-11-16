"""
Teaching Module for Sudoku Techniques
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Dict, List


class TeachingModule(tk.Toplevel):
    """Teaching window for learning Sudoku techniques"""

    # Technique lessons with explanations and examples
    TECHNIQUES = {
        'Introduction': {
            'title': 'Welcome to Sudoku!',
            'level': 0,
            'content': """
Welcome to the Sudoku Learning Module!

WHAT IS SUDOKU?
Sudoku is a logic-based number puzzle. The goal is to fill a 9×9 grid with digits 1-9 such that:
• Each row contains all digits from 1 to 9
• Each column contains all digits from 1 to 9
• Each of the nine 3×3 boxes contains all digits from 1 to 9

HOW TO USE THIS APP:
1. Click on a cell to select it
2. Type a number (1-9) to fill the cell
3. Press 0 or Delete to clear a cell
4. Use arrow keys to move between cells
5. Enable "Pencil Mode" to add/remove candidate notes

LEARNING PATH:
Work through the techniques in order:
1. Naked Singles (Easiest)
2. Hidden Singles
3. Pointing Pairs
4. Box-Line Reduction
5. Naked Pairs
6. Hidden Pairs
7. Naked Triples
8. Hidden Triples
9. X-Wing (Advanced)

Let's start with the basics!
            """
        },
        'Naked Singles': {
            'title': 'Technique 1: Naked Singles',
            'level': 1,
            'content': """
NAKED SINGLES - The Most Basic Technique

DEFINITION:
A naked single is a cell that has only one possible candidate value.

HOW TO FIND:
1. Look at an empty cell
2. Check which numbers already appear in:
   - The same row
   - The same column
   - The same 3×3 box
3. If only ONE number is missing from all three, that's the answer!

EXAMPLE:
If a cell's row has {1,2,3,4,5,6,7,8}, column has {2,9}, and box has {3,4,5}:
• Numbers in row: 1,2,3,4,5,6,7,8
• Numbers in column: 2,9
• Numbers in box: 3,4,5
• All used numbers: {1,2,3,4,5,6,7,8,9} - missing only 9
Wait, 9 is in the column, so check again:
• The cell can only be 9 if it's not eliminated

PRACTICE:
Use the pencil marks feature to track candidates for each cell.
Look for cells with only one pencil mark - that's a naked single!

TIP: Naked singles are the foundation of Sudoku solving. Master this first!
            """
        },
        'Hidden Singles': {
            'title': 'Technique 2: Hidden Singles',
            'level': 1,
            'content': """
HIDDEN SINGLES - Finding Unique Placements

DEFINITION:
A hidden single occurs when a digit can only go in one cell within a row, column, or box,
even if that cell has multiple candidates.

HOW TO FIND:
1. Pick a number (1-9)
2. Look at a row, column, or box
3. Find all cells where this number could go
4. If it can only go in ONE cell, place it there!

EXAMPLE:
In a row with empty cells at positions [2,5,7,8]:
• Number 6 is already eliminated from positions 2, 7, and 8
• Number 6 can ONLY go in position 5
• Therefore, position 5 must be 6 (even if it has other candidates)

WHY "HIDDEN"?
The single is "hidden" among other candidates in that cell.
While the cell might have candidates {3,6,9}, the 6 is the "hidden single"
because it's the only place 6 can go in that row/column/box.

PRACTICE:
1. Pick a number
2. Scan each row looking for where it can go
3. If only one spot, you found a hidden single!
4. Repeat for columns and boxes

TIP: Check each number systematically through all rows, columns, and boxes.
            """
        },
        'Pointing Pairs': {
            'title': 'Technique 3: Pointing Pairs & Triples',
            'level': 2,
            'content': """
POINTING PAIRS/TRIPLES - Box-Line Interactions

DEFINITION:
When a candidate in a box is confined to a single row or column,
you can eliminate that candidate from the rest of that row or column.

HOW TO FIND:
1. Look at a 3×3 box
2. Find a candidate number
3. Check if it appears in only one row OR one column within the box
4. Eliminate that number from the rest of that row/column outside the box

EXAMPLE:
Box 1 (top-left) has candidate 7 only in row 1 positions:
• Box 1, row 1: cells can have 7
• Box 1, rows 2-3: cells cannot have 7
• Therefore, 7 in row 1 MUST be in box 1
• Eliminate 7 from row 1 in boxes 2 and 3

POINTING PAIR vs POINTING TRIPLE:
• Pointing Pair: The candidate appears in exactly 2 cells
• Pointing Triple: The candidate appears in exactly 3 cells
• Both work the same way!

WHY IT WORKS:
The number MUST go somewhere in the box. If it can only be in one row/column
within the box, it CAN'T be in that row/column outside the box.

PRACTICE:
Look at each box and each number (1-9). Find where the number can go in that box.
If confined to one line, check the rest of that line!

TIP: This is your first "elimination" technique - you're not placing numbers,
but removing impossible candidates.
            """
        },
        'Box-Line Reduction': {
            'title': 'Technique 4: Box-Line Reduction',
            'level': 2,
            'content': """
BOX-LINE REDUCTION - The Reverse of Pointing Pairs

DEFINITION:
When a candidate in a row or column is confined to a single box,
you can eliminate that candidate from the rest of that box.

HOW TO FIND:
1. Look at a row or column
2. Find a candidate number
3. Check if it appears only within one box in that row/column
4. Eliminate that number from the rest of that box

EXAMPLE:
Row 5 has candidate 3 only in columns 4-6 (which is box 5):
• Row 5: candidate 3 only possible in box 5
• Therefore, 3 in box 5 MUST be in row 5
• Eliminate 3 from other rows (4 and 6) in box 5

POINTING PAIRS vs BOX-LINE REDUCTION:
• Pointing Pairs: Box → Line (eliminate from line outside box)
• Box-Line Reduction: Line → Box (eliminate from box outside line)

They're complementary techniques!

WHY IT WORKS:
The number MUST go somewhere in the row/column. If it can only be in one box
within that line, it CAN'T be anywhere else in that box.

VISUAL TIP:
  Box-Line: ═══╬═══  (horizontal/vertical line limited to one box)
  Pointing:  ║ ═ ║   (box position limited to one line)

PRACTICE:
1. Pick a number and a row
2. Find where it can go in that row
3. If confined to one box, eliminate from rest of box
4. Repeat for columns!

TIP: Use this with pointing pairs for powerful eliminations!
            """
        },
        'Naked Pairs': {
            'title': 'Technique 5: Naked Pairs',
            'level': 2,
            'content': """
NAKED PAIRS - Two Cells, Two Numbers

DEFINITION:
When two cells in the same row, column, or box both have the exact same
two candidates, those numbers can be eliminated from all other cells in that unit.

HOW TO FIND:
1. Look for two cells with exactly the same two candidates (e.g., {3,7})
2. Both cells must be in the same row, column, or box
3. Eliminate those two numbers from all other cells in that unit

EXAMPLE:
Row 3 has two cells with candidates {2,8}:
• Cell A: {2,8}
• Cell B: {2,8}
• These cells MUST contain 2 and 8 (in some order)
• Remove 2 and 8 from all other cells in row 3

WHY IT WORKS:
Even though you don't know which cell gets which number, you know that
BOTH numbers are "locked" into those two cells. No other cell in the
row/column/box can use them.

IMPORTANT:
Both cells must have EXACTLY two candidates. If one cell has {2,8,9}, it's NOT a naked pair.

VARIANTS:
• The same logic works for Naked Triples (3 cells, 3 numbers)
• And Naked Quads (4 cells, 4 numbers)

PRACTICE:
1. Enable pencil marks
2. Look for cells with only 2 candidates
3. Find matching pairs
4. Eliminate those numbers from other cells

TIP: Fill in pencil marks to make naked pairs easier to spot!
            """
        },
        'Hidden Pairs': {
            'title': 'Technique 6: Hidden Pairs',
            'level': 2,
            'content': """
HIDDEN PAIRS - Two Numbers, Two Cells

DEFINITION:
When two candidates appear in only two cells within a row, column, or box,
those cells can only contain those two candidates (eliminate all others from those cells).

HOW TO FIND:
1. Pick two numbers (e.g., 4 and 9)
2. In a row/column/box, find where these numbers can go
3. If BOTH numbers can only go in the same two cells
4. Remove all OTHER candidates from those two cells

EXAMPLE:
In a row, candidates 5 and 7:
• Only cells A and B can contain 5
• Only cells A and B can contain 7
• Cell A might have {2,5,6,7,9}
• Cell B might have {1,5,7,8}
• Remove all except 5 and 7: A={5,7}, B={5,7}

WHY "HIDDEN"?
The pair is "hidden" among other candidates in the cells.
You have to actively look for two numbers that share the same two positions.

NAKED vs HIDDEN PAIRS:
• Naked Pair: Look at cells → Find matching candidates
• Hidden Pair: Look at candidates → Find matching cells

PRACTICE:
1. Pick two numbers
2. Find where they can go in a row/column/box
3. If they share exactly two positions, you found a hidden pair!
4. Clean up other candidates from those cells

TIP: Hidden pairs are harder to spot than naked pairs.
Check systematically: try all pairs of numbers!

ADVANCED TIP: After removing extra candidates, a hidden pair often
becomes a naked pair!
            """
        },
        'Naked Triples': {
            'title': 'Technique 7: Naked Triples',
            'level': 3,
            'content': """
NAKED TRIPLES - Three Cells, Three Numbers

DEFINITION:
When three cells in the same row, column, or box collectively contain only
three candidates (distributed among them), those numbers can be eliminated
from all other cells in that unit.

HOW TO FIND:
1. Look for three cells in the same row/column/box
2. The union of their candidates should be exactly 3 numbers
3. Eliminate those three numbers from all other cells in that unit

EXAMPLE:
Three cells in a column:
• Cell A: {2,5}
• Cell B: {2,7}
• Cell C: {5,7}
• Union: {2,5,7} - exactly 3 numbers!
• Remove 2, 5, and 7 from all other cells in the column

IMPORTANT VARIATIONS:
The three cells don't need to each have all three candidates:
• Valid: {2,5}, {2,7}, {5,7}
• Valid: {2,5,7}, {2,5}, {5,7}
• Valid: {2,5,7}, {2,5,7}, {2,5,7}
• NOT valid: {2,5,8}, {2,7}, {5,7} - has 4 numbers!

WHY IT WORKS:
The three numbers MUST be distributed among the three cells.
Even if you don't know the exact arrangement, those numbers are
"locked" into those three positions.

PRACTICE:
1. Look for cells with 2-3 candidates
2. Find groups of 3 cells
3. Check if their union has exactly 3 numbers
4. Eliminate from other cells!

TIP: Naked triples are harder to spot than pairs.
Use pencil marks and look systematically!

RELATED: Naked Quads work the same way (4 cells, 4 numbers).
            """
        },
        'Hidden Triples': {
            'title': 'Technique 8: Hidden Triples',
            'level': 3,
            'content': """
HIDDEN TRIPLES - Three Numbers, Three Cells

DEFINITION:
When three candidates appear in only three cells within a row, column, or box,
those cells can only contain those three candidates (eliminate all others from those cells).

HOW TO FIND:
1. Pick three numbers (e.g., 1, 6, and 8)
2. In a row/column/box, find where these numbers can go
3. If these three numbers can ONLY go in the same three cells
4. Remove all OTHER candidates from those three cells

EXAMPLE:
In a box, candidates 3, 4, and 9:
• Number 3 can go in cells A, B, C only
• Number 4 can go in cells A, B, C only
• Number 9 can go in cells A, B, C only
• Cell A might have {2,3,4,9}, Cell B might have {1,3,9}, Cell C might have {4,5,9}
• Clean up: A={3,4,9}, B={3,9}, C={4,9}

WHY IT WORKS:
These three numbers MUST go somewhere. If they can only fit in three cells,
those cells can't contain any other numbers.

FINDING HIDDEN TRIPLES:
This is challenging! You need to check many combinations:
• Try all combinations of 3 numbers from {1,2,3,4,5,6,7,8,9}
• For each combo, check if they're confined to exactly 3 cells
• That's 84 combinations per row/column/box!

SHORTCUT:
Look for numbers that have limited placement options.
If three numbers each appear in only 3-4 cells, investigate if they share positions.

PRACTICE:
1. Find numbers with few possible positions
2. Check if 2-3 of these numbers share the same cells
3. If you find a third number completing the pattern, clean up!

TIP: Hidden triples are rare and hard to spot.
Focus on mastering easier techniques first!

RELATIONSHIP: After cleaning, a hidden triple often becomes a naked triple!
            """
        },
        'X-Wing': {
            'title': 'Technique 9: X-Wing',
            'level': 4,
            'content': """
X-WING - Advanced Pattern Elimination

DEFINITION:
When a candidate appears in exactly two cells in each of two rows (or columns),
and these cells are aligned in columns (or rows), you can eliminate that candidate
from all other cells in those columns (or rows).

HOW TO FIND (Row-based X-Wing):
1. Pick a candidate number
2. Find two rows where this number appears in exactly 2 cells each
3. Check if the column positions are the same in both rows
4. If yes, eliminate the number from those columns in all other rows

VISUAL PATTERN (X shape):
  Row A:    . . X . . X . . .
  Row B:    . . . . . . . . .
  Row C:    . . X . . X . . .
            └─┘           └─┘
         Col 3           Col 6

If candidate 5 appears only at these X positions in rows A and C,
eliminate 5 from column 3 and column 6 in all other rows.

EXAMPLE:
Candidate 7 appears in:
• Row 2: columns 4 and 7 only
• Row 8: columns 4 and 7 only
• Eliminate 7 from columns 4 and 7 in rows 1,3,4,5,6,7,9

WHY IT WORKS:
In row 2, the 7 goes in column 4 OR column 7.
In row 8, the 7 goes in column 4 OR column 7.
• If row 2 has 7 in col 4, then row 8 has 7 in col 7
• If row 2 has 7 in col 7, then row 8 has 7 in col 4
Either way, columns 4 and 7 have 7 in rows 2 and 8 only!

COLUMN-BASED X-WING:
Same logic, but:
• Find two columns with exactly 2 cells each
• Check if row positions align
• Eliminate from those rows in other columns

PRACTICE:
1. Pick a number
2. Find rows/columns where it appears exactly twice
3. Look for alignment patterns
4. Make eliminations!

TIP: X-Wing is an advanced technique. Make sure you're comfortable
with all previous techniques first!

RELATED: Swordfish (3×3 pattern) and Jellyfish (4×4) are extensions of X-Wing.
            """
        }
    }

    # Order of lessons
    LESSON_ORDER = [
        'Introduction',
        'Naked Singles',
        'Hidden Singles',
        'Pointing Pairs',
        'Box-Line Reduction',
        'Naked Pairs',
        'Hidden Pairs',
        'Naked Triples',
        'Hidden Triples',
        'X-Wing'
    ]

    def __init__(self, master):
        super().__init__(master)
        self.title("Sudoku Learning Module")
        self.geometry("800x600")

        self.current_lesson = 0

        self._create_widgets()
        self._show_lesson(0)

    def _create_widgets(self):
        """Create the teaching interface"""
        # Top frame with navigation
        nav_frame = tk.Frame(self)
        nav_frame.pack(fill=tk.X, padx=10, pady=5)

        self.prev_button = tk.Button(nav_frame, text="◄ Previous", command=self._prev_lesson)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.lesson_label = tk.Label(nav_frame, text="", font=("Arial", 12, "bold"))
        self.lesson_label.pack(side=tk.LEFT, expand=True)

        self.next_button = tk.Button(nav_frame, text="Next ►", command=self._next_lesson)
        self.next_button.pack(side=tk.RIGHT, padx=5)

        # Lesson selector
        selector_frame = tk.Frame(self)
        selector_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(selector_frame, text="Jump to lesson:").pack(side=tk.LEFT)

        self.lesson_combo = ttk.Combobox(selector_frame, values=self.LESSON_ORDER, state="readonly", width=30)
        self.lesson_combo.pack(side=tk.LEFT, padx=5)
        self.lesson_combo.bind("<<ComboboxSelected>>", self._on_lesson_selected)

        # Content area
        content_frame = tk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.title_label = tk.Label(content_frame, text="", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        self.content_text = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            font=("Courier", 10),
            padx=10,
            pady=10
        )
        self.content_text.pack(fill=tk.BOTH, expand=True)

        # Progress indicator
        progress_frame = tk.Frame(self)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)

        self.progress_label = tk.Label(progress_frame, text="")
        self.progress_label.pack()

    def _show_lesson(self, index: int):
        """Display a lesson"""
        if 0 <= index < len(self.LESSON_ORDER):
            self.current_lesson = index
            lesson_name = self.LESSON_ORDER[index]
            lesson = self.TECHNIQUES[lesson_name]

            self.lesson_label.config(text=f"Lesson {index + 1} of {len(self.LESSON_ORDER)}")
            self.title_label.config(text=lesson['title'])

            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, lesson['content'].strip())

            self.lesson_combo.set(lesson_name)

            # Update buttons
            self.prev_button.config(state=tk.NORMAL if index > 0 else tk.DISABLED)
            self.next_button.config(state=tk.NORMAL if index < len(self.LESSON_ORDER) - 1 else tk.DISABLED)

            self.progress_label.config(
                text=f"Progress: {index + 1}/{len(self.LESSON_ORDER)} lessons • Level: {lesson['level']}"
            )

    def _prev_lesson(self):
        """Show previous lesson"""
        self._show_lesson(self.current_lesson - 1)

    def _next_lesson(self):
        """Show next lesson"""
        self._show_lesson(self.current_lesson + 1)

    def _on_lesson_selected(self, event):
        """Handle lesson selection from combobox"""
        lesson_name = self.lesson_combo.get()
        if lesson_name in self.LESSON_ORDER:
            index = self.LESSON_ORDER.index(lesson_name)
            self._show_lesson(index)
