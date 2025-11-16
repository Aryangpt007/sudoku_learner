"""
Sudoku Grid Widget with pencil marking support
"""

import tkinter as tk
from tkinter import font
from typing import Optional, Callable, Set
from ..core.sudoku import Sudoku


class SudokuGrid(tk.Frame):
    """Interactive Sudoku grid widget"""

    def __init__(self, master, sudoku: Sudoku, on_cell_change: Optional[Callable] = None):
        super().__init__(master)

        self.sudoku = sudoku
        self.on_cell_change = on_cell_change

        self.selected_cell = None
        self.pencil_mode = False

        # Colors
        self.bg_color = "#FFFFFF"
        self.initial_cell_bg = "#E0E0E0"
        self.selected_bg = "#BBDEFB"
        self.same_number_bg = "#FFF9C4"
        self.error_bg = "#FFCDD2"
        self.highlight_bg = "#E3F2FD"

        self.grid_line_color = "#000000"
        self.box_line_color = "#000000"

        # Create canvas
        self.cell_size = 60
        self.canvas = tk.Canvas(
            self,
            width=self.cell_size * 9 + 1,
            height=self.cell_size * 9 + 1,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack()

        # Fonts
        self.number_font = font.Font(family="Arial", size=24, weight="bold")
        self.pencil_font = font.Font(family="Arial", size=8)

        # Cell rectangles and text items
        self.cell_rects = [[None for _ in range(9)] for _ in range(9)]
        self.cell_texts = [[None for _ in range(9)] for _ in range(9)]
        self.pencil_texts = [[{} for _ in range(9)] for _ in range(9)]

        self._create_grid()
        self._bind_events()

    def _create_grid(self):
        """Create the grid visualization"""
        # Draw cells
        for r in range(9):
            for c in range(9):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Determine background color
                bg = self.initial_cell_bg if self.sudoku.is_initial_cell(r, c) else self.bg_color

                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=bg,
                    outline="",
                    tags=f"cell_{r}_{c}"
                )
                self.cell_rects[r][c] = rect

                # Create text item for number
                x_center = x1 + self.cell_size // 2
                y_center = y1 + self.cell_size // 2

                value = self.sudoku.get_cell(r, c)
                text = str(value) if value != 0 else ""
                color = "#000000" if self.sudoku.is_initial_cell(r, c) else "#0D47A1"

                text_item = self.canvas.create_text(
                    x_center, y_center,
                    text=text,
                    font=self.number_font,
                    fill=color,
                    tags=f"text_{r}_{c}"
                )
                self.cell_texts[r][c] = text_item

                # Create pencil mark positions
                for prow in range(3):
                    for pcol in range(3):
                        num = prow * 3 + pcol + 1
                        px = x1 + 10 + pcol * 15
                        py = y1 + 10 + prow * 15

                        pencil_text = self.canvas.create_text(
                            px, py,
                            text="",
                            font=self.pencil_font,
                            fill="#666666",
                            tags=f"pencil_{r}_{c}_{num}"
                        )
                        self.pencil_texts[r][c][num] = pencil_text

        # Draw grid lines
        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            # Vertical lines
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, 9 * self.cell_size, width=width, fill=self.grid_line_color)
            # Horizontal lines
            y = i * self.cell_size
            self.canvas.create_line(0, y, 9 * self.cell_size, y, width=width, fill=self.grid_line_color)

    def _bind_events(self):
        """Bind mouse and keyboard events"""
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Key>", self._on_key)
        self.canvas.focus_set()

    def _on_click(self, event):
        """Handle mouse click"""
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if 0 <= row < 9 and 0 <= col < 9:
            self.select_cell(row, col)
            self.canvas.focus_set()

    def _on_key(self, event):
        """Handle keyboard input"""
        if self.selected_cell is None:
            return

        row, col = self.selected_cell

        # Number keys
        if event.char.isdigit():
            num = int(event.char)

            if self.pencil_mode:
                # Toggle pencil mark
                if num >= 1 and num <= 9:
                    marks = self.sudoku.get_pencil_marks(row, col)
                    self.sudoku.set_pencil_mark(row, col, num, num not in marks)
                    self.update_cell(row, col)
            else:
                # Set cell value
                if num == 0 or (num >= 1 and num <= 9):
                    if self.sudoku.set_cell(row, col, num):
                        self.update_all()
                        if self.on_cell_change:
                            self.on_cell_change()

        # Arrow keys
        elif event.keysym in ['Up', 'Down', 'Left', 'Right']:
            new_row, new_col = row, col
            if event.keysym == 'Up' and row > 0:
                new_row -= 1
            elif event.keysym == 'Down' and row < 8:
                new_row += 1
            elif event.keysym == 'Left' and col > 0:
                new_col -= 1
            elif event.keysym == 'Right' and col < 8:
                new_col += 1

            self.select_cell(new_row, new_col)

        # Delete/Backspace
        elif event.keysym in ['Delete', 'BackSpace']:
            if self.sudoku.set_cell(row, col, 0):
                self.update_all()
                if self.on_cell_change:
                    self.on_cell_change()

    def select_cell(self, row: int, col: int):
        """Select a cell"""
        if self.sudoku.is_initial_cell(row, col):
            # Can't select initial cells for editing
            # But still highlight them
            pass

        # Clear previous selection
        if self.selected_cell:
            old_row, old_col = self.selected_cell
            self._update_cell_color(old_row, old_col)

        self.selected_cell = (row, col)
        self._update_highlights()

    def _update_highlights(self):
        """Update cell highlighting"""
        if self.selected_cell is None:
            return

        sel_row, sel_col = self.selected_cell
        selected_value = self.sudoku.get_cell(sel_row, sel_col)

        for r in range(9):
            for c in range(9):
                if (r, c) == self.selected_cell:
                    # Selected cell
                    self.canvas.itemconfig(self.cell_rects[r][c], fill=self.selected_bg)
                elif r == sel_row or c == sel_col or \
                     (r // 3 == sel_row // 3 and c // 3 == sel_col // 3):
                    # Same row, column, or box
                    if self.sudoku.is_initial_cell(r, c):
                        self.canvas.itemconfig(self.cell_rects[r][c], fill="#C0C0C0")
                    else:
                        self.canvas.itemconfig(self.cell_rects[r][c], fill=self.highlight_bg)
                elif selected_value != 0 and self.sudoku.get_cell(r, c) == selected_value:
                    # Same number
                    self.canvas.itemconfig(self.cell_rects[r][c], fill=self.same_number_bg)
                else:
                    self._update_cell_color(r, c)

    def _update_cell_color(self, row: int, col: int):
        """Update a single cell's background color"""
        if self.sudoku.is_initial_cell(row, col):
            self.canvas.itemconfig(self.cell_rects[row][col], fill=self.initial_cell_bg)
        else:
            # Check for errors
            value = self.sudoku.get_cell(row, col)
            if value != 0 and not self.sudoku.is_valid_move(row, col, value):
                self.canvas.itemconfig(self.cell_rects[row][col], fill=self.error_bg)
            else:
                self.canvas.itemconfig(self.cell_rects[row][col], fill=self.bg_color)

    def update_cell(self, row: int, col: int):
        """Update display of a single cell"""
        value = self.sudoku.get_cell(row, col)

        if value != 0:
            # Show number
            self.canvas.itemconfig(self.cell_texts[row][col], text=str(value))
            # Hide pencil marks
            for num in range(1, 10):
                self.canvas.itemconfig(self.pencil_texts[row][col][num], text="")
        else:
            # Hide number
            self.canvas.itemconfig(self.cell_texts[row][col], text="")
            # Show pencil marks
            marks = self.sudoku.get_pencil_marks(row, col)
            for num in range(1, 10):
                if num in marks:
                    self.canvas.itemconfig(self.pencil_texts[row][col][num], text=str(num))
                else:
                    self.canvas.itemconfig(self.pencil_texts[row][col][num], text="")

        self._update_cell_color(row, col)

    def update_all(self):
        """Update display of all cells"""
        for r in range(9):
            for c in range(9):
                self.update_cell(r, c)

        self._update_highlights()

    def set_sudoku(self, sudoku: Sudoku):
        """Set a new Sudoku puzzle"""
        self.sudoku = sudoku
        self.selected_cell = None
        self.update_all()

    def set_pencil_mode(self, enabled: bool):
        """Enable or disable pencil mode"""
        self.pencil_mode = enabled

    def highlight_cells(self, cells: list, color: str):
        """Highlight specific cells with a color"""
        for r, c in cells:
            self.canvas.itemconfig(self.cell_rects[r][c], fill=color)

    def auto_fill_pencil_marks(self):
        """Auto-fill all pencil marks"""
        self.sudoku.update_pencil_marks()
        self.update_all()
