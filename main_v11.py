#!/usr/bin/env python3
"""
Sudoku Learning Application v1.1
Main entry point for enhanced version

NEW in v1.1:
- Undo/Redo functionality (Ctrl+Z / Ctrl+Shift+Z)
- Comprehensive keyboard shortcuts
- Visual pencil mode indicator
- Settings & Preferences dialog
- Improved step navigation with Play All feature
- Better status messages and user feedback
- Configurable pencil mark size and colors
"""

import tkinter as tk
from sudoku_app.gui.main_window_v11 import SudokuAppV11


def main():
    """Launch the Sudoku application v1.1"""
    root = tk.Tk()
    app = SudokuAppV11(root)
    root.mainloop()


if __name__ == "__main__":
    main()
