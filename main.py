#!/usr/bin/env python3
"""
Sudoku Learning Application
Main entry point

Current Version: 1.1
- Undo/Redo functionality (Ctrl+Z / Ctrl+Shift+Z)
- 30+ keyboard shortcuts
- Visual pencil mode indicator
- Settings & Preferences dialog
- Play All Steps feature for solver
- Improved UX and status messages
- Configurable colors and sizes

Note: To use the basic v1.0 interface (no undo/shortcuts),
      import from sudoku_app.gui.main_window instead.
"""

import tkinter as tk
from sudoku_app.gui.main_window_v11 import SudokuAppV11


def main():
    """Launch the Sudoku application"""
    root = tk.Tk()
    app = SudokuAppV11(root)
    root.mainloop()


if __name__ == "__main__":
    main()
