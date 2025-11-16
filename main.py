#!/usr/bin/env python3
"""
Sudoku Learning Application
Main entry point
"""

import tkinter as tk
from sudoku_app.gui.main_window import SudokuApp


def main():
    """Launch the Sudoku application"""
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
