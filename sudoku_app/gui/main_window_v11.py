"""
Main Application Window - Version 1.1
Enhanced with undo/redo, keyboard shortcuts, settings, and improved UX
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
from ..core.sudoku import Sudoku
from ..core.solver import SudokuSolver
from ..core.generator import SudokuGenerator
from ..core.history import HistoryManager, Move, MoveType
from ..utils.io_handler import IOHandler
from .grid import SudokuGrid
from .teaching import TeachingModule
from .settings import Settings, SettingsDialog


class SudokuAppV11:
    """Main Sudoku application window - Version 1.1"""

    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Learning Application v1.1")
        self.root.resizable(False, False)

        # Settings
        self.settings = Settings()

        # Initialize with empty puzzle
        self.sudoku = Sudoku()
        self.history = HistoryManager(max_history=self.settings.get('max_undo_history', 100))
        self.sudoku.history_manager = self.history

        self.generator = SudokuGenerator()
        self.solver = None
        self.solving_steps = []
        self.current_step = 0
        self.pencil_mode = False
        self.auto_play_active = False

        # Timer
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_id = None

        self._create_widgets()
        self._create_menu()
        self._setup_keyboard_shortcuts()

        # Generate initial puzzle
        default_diff = self.settings.get('default_difficulty', 'easy')
        self.difficulty_var.set(default_diff)
        self.generate_puzzle(default_diff)

    def _create_menu(self):
        """Create menu bar with shortcuts"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Puzzle...", command=self.show_new_puzzle_dialog, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Import Puzzle...", command=self.import_puzzle, accelerator="Ctrl+O")
        file_menu.add_command(label="Export Puzzle...", command=self.export_puzzle, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Settings...", command=self.show_settings, accelerator="Ctrl+,")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")

        # Edit menu (NEW in v1.1)
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Shift+Z")
        edit_menu.add_separator()
        edit_menu.add_command(label="Toggle Pencil Mode", command=self.toggle_pencil_mode, accelerator="Space")

        # Puzzle menu
        puzzle_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Puzzle", menu=puzzle_menu)
        puzzle_menu.add_command(label="Clear Non-Initial Cells", command=self.clear_puzzle)
        puzzle_menu.add_command(label="Check Solution", command=self.check_solution, accelerator="Ctrl+K")
        puzzle_menu.add_command(label="Auto-fill Pencil Marks", command=self.auto_pencil_marks, accelerator="Ctrl+P")

        # Solver menu
        solver_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Solver", menu=solver_menu)
        solver_menu.add_command(label="Get Hint", command=self.get_hint, accelerator="Ctrl+H")
        solver_menu.add_command(label="Solve Step-by-Step", command=self.solve_step_by_step, accelerator="Ctrl+S")
        solver_menu.add_command(label="Next Step", command=self.next_step, accelerator="Ctrl+Right")
        solver_menu.add_command(label="Play All Steps", command=self.play_all_steps, accelerator="Ctrl+R")
        solver_menu.add_command(label="Solve Instantly", command=self.solve_instantly, accelerator="Ctrl+I")

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Learning Module", command=self.show_teaching_module, accelerator="F1")
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)

    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        # File operations
        self.root.bind('<Control-n>', lambda e: self.show_new_puzzle_dialog())
        self.root.bind('<Control-N>', lambda e: self.show_new_puzzle_dialog())
        self.root.bind('<Control-o>', lambda e: self.import_puzzle())
        self.root.bind('<Control-O>', lambda e: self.import_puzzle())
        self.root.bind('<Control-e>', lambda e: self.export_puzzle())
        self.root.bind('<Control-E>', lambda e: self.export_puzzle())
        self.root.bind('<Control-comma>', lambda e: self.show_settings())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-Q>', lambda e: self.root.quit())

        # Edit operations
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-Z>', lambda e: self.undo())
        self.root.bind('<Control-Shift-Z>', lambda e: self.redo())
        self.root.bind('<Control-Shift-z>', lambda e: self.redo())
        self.root.bind('<Control-y>', lambda e: self.redo())  # Alternative redo
        self.root.bind('<Control-Y>', lambda e: self.redo())

        # Puzzle operations
        self.root.bind('<Control-k>', lambda e: self.check_solution())
        self.root.bind('<Control-K>', lambda e: self.check_solution())
        self.root.bind('<Control-p>', lambda e: self.auto_pencil_marks())
        self.root.bind('<Control-P>', lambda e: self.auto_pencil_marks())

        # Solver operations
        self.root.bind('<Control-h>', lambda e: self.get_hint())
        self.root.bind('<Control-H>', lambda e: self.get_hint())
        self.root.bind('<Control-s>', lambda e: self.solve_step_by_step())
        self.root.bind('<Control-S>', lambda e: self.solve_step_by_step())
        self.root.bind('<Control-Right>', lambda e: self.next_step())
        self.root.bind('<Control-r>', lambda e: self.play_all_steps())
        self.root.bind('<Control-R>', lambda e: self.play_all_steps())
        self.root.bind('<Control-i>', lambda e: self.solve_instantly())
        self.root.bind('<Control-I>', lambda e: self.solve_instantly())

        # Help
        self.root.bind('<F1>', lambda e: self.show_teaching_module())

    def _create_widgets(self):
        """Create main window widgets"""
        # Main container
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack()

        # Left side - Grid
        grid_frame = tk.Frame(main_frame)
        grid_frame.pack(side=tk.LEFT, padx=10)

        # Grid widget
        cell_size = self.settings.get('cell_size', 60)
        pencil_size = self.settings.get('pencil_mark_size', 10)

        self.grid_widget = SudokuGrid(grid_frame, self.sudoku, on_cell_change=self.on_grid_change)
        self.grid_widget.pencil_font.config(size=pencil_size)
        self.grid_widget.pack()

        # Control panel below grid
        controls_below_grid = tk.Frame(grid_frame)
        controls_below_grid.pack(pady=5)

        # Pencil mode toggle with visual indicator
        pencil_frame = tk.Frame(controls_below_grid)
        pencil_frame.pack(side=tk.LEFT, padx=5)

        self.pencil_var = tk.BooleanVar()
        self.pencil_indicator = tk.Label(pencil_frame, text="✎", font=("Arial", 16), fg="gray")
        self.pencil_indicator.pack(side=tk.LEFT)

        pencil_check = tk.Checkbutton(
            pencil_frame,
            text="Pencil Mode (Space)",
            variable=self.pencil_var,
            command=self.toggle_pencil_mode,
            font=("Arial", 10)
        )
        pencil_check.pack(side=tk.LEFT)

        # Undo/Redo buttons
        undo_frame = tk.Frame(controls_below_grid)
        undo_frame.pack(side=tk.LEFT, padx=5)

        self.undo_button = tk.Button(
            undo_frame,
            text="↶ Undo",
            command=self.undo,
            state=tk.DISABLED,
            width=8
        )
        self.undo_button.pack(side=tk.LEFT, padx=2)

        self.redo_button = tk.Button(
            undo_frame,
            text="↷ Redo",
            command=self.redo,
            state=tk.DISABLED,
            width=8
        )
        self.redo_button.pack(side=tk.LEFT, padx=2)

        # Timer (if enabled)
        if self.settings.get('show_timer', False):
            self.timer_label = tk.Label(controls_below_grid, text="00:00", font=("Arial", 14, "bold"))
            self.timer_label.pack(side=tk.LEFT, padx=10)

        # Right side - Controls
        control_frame = tk.Frame(main_frame)
        control_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)

        # Puzzle Generation
        gen_frame = tk.LabelFrame(control_frame, text="Generate Puzzle", padx=10, pady=10)
        gen_frame.pack(fill=tk.X, pady=5)

        tk.Label(gen_frame, text="Difficulty:").pack()

        self.difficulty_var = tk.StringVar(value="easy")
        difficulties = SudokuGenerator.get_difficulty_levels()

        for diff in difficulties:
            rb = tk.Radiobutton(
                gen_frame,
                text=diff.replace('_', ' ').title(),
                variable=self.difficulty_var,
                value=diff
            )
            rb.pack(anchor=tk.W)

        tk.Button(
            gen_frame,
            text="Generate New Puzzle (Ctrl+N)",
            command=lambda: self.generate_puzzle(self.difficulty_var.get()),
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9, "bold")
        ).pack(pady=10, fill=tk.X)

        # Solver Controls
        solver_frame = tk.LabelFrame(control_frame, text="Solver", padx=10, pady=10)
        solver_frame.pack(fill=tk.X, pady=5)

        tk.Button(
            solver_frame,
            text="Get Hint (Ctrl+H)",
            command=self.get_hint,
            bg="#2196F3",
            fg="white"
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            solver_frame,
            text="Solve Step-by-Step (Ctrl+S)",
            command=self.solve_step_by_step,
            bg="#FF9800",
            fg="white"
        ).pack(fill=tk.X, pady=2)

        # Step navigation frame
        step_nav_frame = tk.Frame(solver_frame)
        step_nav_frame.pack(fill=tk.X, pady=2)

        tk.Button(
            step_nav_frame,
            text="Next Step",
            command=self.next_step,
            bg="#FFC107",
            fg="black",
            width=10
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        tk.Button(
            step_nav_frame,
            text="Play All",
            command=self.play_all_steps,
            bg="#FF5722",
            fg="white",
            width=10
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        tk.Button(
            solver_frame,
            text="Solve Instantly (Ctrl+I)",
            command=self.solve_instantly,
            bg="#F44336",
            fg="white"
        ).pack(fill=tk.X, pady=2)

        # Step counter label
        self.step_counter_label = tk.Label(solver_frame, text="", font=("Arial", 9), fg="gray")
        self.step_counter_label.pack()

        # Step display
        step_display_frame = tk.LabelFrame(control_frame, text="Current Step", padx=10, pady=10)
        step_display_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.step_text = tk.Text(step_display_frame, wrap=tk.WORD, height=15, width=35, font=("Arial", 9))
        step_scroll = tk.Scrollbar(step_display_frame, command=self.step_text.yview)
        self.step_text.config(yscrollcommand=step_scroll.set)

        self.step_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        step_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Other controls
        other_frame = tk.LabelFrame(control_frame, text="Actions", padx=10, pady=10)
        other_frame.pack(fill=tk.X, pady=5)

        tk.Button(
            other_frame,
            text="Auto-fill Pencil Marks (Ctrl+P)",
            command=self.auto_pencil_marks
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            other_frame,
            text="Clear Puzzle",
            command=self.clear_puzzle
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            other_frame,
            text="Check Solution (Ctrl+K)",
            command=self.check_solution,
            bg="#9C27B0",
            fg="white"
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            other_frame,
            text="Learning Module (F1)",
            command=self.show_teaching_module,
            bg="#00BCD4",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(fill=tk.X, pady=10)

        # Status bar
        self.status_var = tk.StringVar(value="Ready - Press F1 for help")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def undo(self):
        """Undo last move"""
        if not self.history.can_undo():
            return

        move = self.history.undo()
        if move:
            # Restore the cell to its old state
            if move.move_type == MoveType.SET_VALUE:
                self.sudoku.grid[move.row][move.col] = move.old_value
                if move.old_value == 0:
                    self.sudoku.pencil_marks[move.row][move.col] = move.old_pencil_marks.copy()
            elif move.move_type == MoveType.SET_PENCIL_MARK:
                self.sudoku.pencil_marks[move.row][move.col] = move.old_pencil_marks.copy()

            self.grid_widget.update_all()
            self.update_undo_redo_buttons()
            self.status_var.set(f"Undone: {move.move_type.value} at ({move.row+1},{move.col+1})")

    def redo(self):
        """Redo last undone move"""
        if not self.history.can_redo():
            return

        move = self.history.redo()
        if move:
            # Reapply the move
            if move.move_type == MoveType.SET_VALUE:
                self.sudoku.grid[move.row][move.col] = move.new_value
                if move.new_value != 0:
                    self.sudoku.pencil_marks[move.row][move.col] = set()
            elif move.move_type == MoveType.SET_PENCIL_MARK:
                self.sudoku.pencil_marks[move.row][move.col] = move.new_pencil_marks.copy()

            self.grid_widget.update_all()
            self.update_undo_redo_buttons()
            self.status_var.set(f"Redone: {move.move_type.value} at ({move.row+1},{move.col+1})")

    def update_undo_redo_buttons(self):
        """Update undo/redo button states"""
        self.undo_button.config(
            state=tk.NORMAL if self.history.can_undo() else tk.DISABLED,
            text=f"↶ Undo ({self.history.get_undo_count()})"
        )
        self.redo_button.config(
            state=tk.NORMAL if self.history.can_redo() else tk.DISABLED,
            text=f"↷ Redo ({self.history.get_redo_count()})"
        )

    def record_move(self, move_type: MoveType, row: int, col: int, old_value=None, new_value=None,
                   old_pencil_marks=None, new_pencil_marks=None):
        """Record a move in history"""
        move = Move(move_type, row, col, old_value, new_value, old_pencil_marks, new_pencil_marks)
        self.history.add_move(move)
        self.update_undo_redo_buttons()

    def toggle_pencil_mode(self):
        """Toggle pencil marking mode with visual feedback"""
        self.pencil_mode = self.pencil_var.get()
        self.grid_widget.set_pencil_mode(self.pencil_mode)

        # Update visual indicator
        if self.pencil_mode:
            self.pencil_indicator.config(fg="#FF9800", font=("Arial", 16, "bold"))
            self.status_var.set("Pencil mode: ON - Type numbers to toggle marks")
            # Change cursor
            self.grid_widget.canvas.config(cursor="pencil")
        else:
            self.pencil_indicator.config(fg="gray", font=("Arial", 16))
            self.status_var.set("Pencil mode: OFF - Type numbers to fill cells")
            self.grid_widget.canvas.config(cursor="")

    def play_all_steps(self):
        """Play through all solving steps automatically"""
        if not self.solving_steps:
            messagebox.showinfo("No Steps", "Click 'Solve Step-by-Step' first!")
            return

        if self.current_step >= len(self.solving_steps):
            messagebox.showinfo("Complete", "All steps already shown!")
            return

        self.auto_play_active = True
        self._play_next_step_auto()

    def _play_next_step_auto(self):
        """Play next step with delay"""
        if not self.auto_play_active or self.current_step >= len(self.solving_steps):
            self.auto_play_active = False
            return

        self.next_step()

        # Get delay based on animation speed setting
        speed = self.settings.get('animation_speed', 'normal')
        delays = {'slow': 2000, 'normal': 1000, 'fast': 500, 'instant': 0}
        delay = delays.get(speed, 1000)

        if delay > 0:
            self.root.after(delay, self._play_next_step_auto)
        else:
            self._play_next_step_auto()

    def show_settings(self):
        """Show settings dialog"""
        SettingsDialog(self.root, self.settings, on_apply=self._apply_settings)

    def _apply_settings(self):
        """Apply settings after changes"""
        # Update grid colors and sizes
        if self.grid_widget:
            pencil_size = self.settings.get('pencil_mark_size', 10)
            self.grid_widget.pencil_font.config(size=pencil_size)
            self.grid_widget.update_all()

        # Update history size
        max_history = self.settings.get('max_undo_history', 100)
        self.history.max_history = max_history

    def show_shortcuts(self):
        """Show keyboard shortcuts help"""
        shortcuts_text = """
KEYBOARD SHORTCUTS

File Operations:
  Ctrl+N      New Puzzle
  Ctrl+O      Open/Import Puzzle
  Ctrl+E      Export Puzzle
  Ctrl+,      Settings
  Ctrl+Q      Quit

Edit Operations:
  Ctrl+Z      Undo
  Ctrl+Shift+Z  Redo
  Ctrl+Y      Redo (alternative)
  Space       Toggle Pencil Mode

Puzzle Operations:
  Ctrl+P      Auto-fill Pencil Marks
  Ctrl+K      Check Solution

Solver Operations:
  Ctrl+H      Get Hint
  Ctrl+S      Solve Step-by-Step
  Ctrl+Right  Next Step
  Ctrl+R      Play All Steps
  Ctrl+I      Solve Instantly

Help:
  F1          Learning Module

Grid Navigation:
  Arrow Keys  Move between cells
  1-9         Enter number (or toggle pencil mark)
  0, Delete   Clear cell
        """

        msg_window = tk.Toplevel(self.root)
        msg_window.title("Keyboard Shortcuts")
        msg_window.geometry("400x500")

        text_widget = tk.Text(msg_window, wrap=tk.WORD, font=("Courier", 10), padx=20, pady=20)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(1.0, shortcuts_text)
        text_widget.config(state=tk.DISABLED)

        tk.Button(msg_window, text="Close", command=msg_window.destroy).pack(pady=10)

    # The rest of the methods remain the same but with updated status messages
    # I'll include key methods below

    def generate_puzzle(self, difficulty: str):
        """Generate a new puzzle"""
        self.status_var.set(f"Generating {difficulty} puzzle...")
        self.root.update()

        try:
            self.sudoku = Sudoku()
            self.history = HistoryManager(max_history=self.settings.get('max_undo_history', 100))
            self.sudoku.history_manager = self.history

            self.sudoku = self.generator.generate(difficulty)
            self.grid_widget.set_sudoku(self.sudoku)
            self.solving_steps = []
            self.current_step = 0
            self.step_text.delete(1.0, tk.END)
            self.step_counter_label.config(text="")

            self.update_undo_redo_buttons()

            # Start timer if enabled
            if self.settings.get('show_timer', False):
                self.start_timer()

            desc = SudokuGenerator.get_difficulty_description(difficulty)
            self.status_var.set(f"New {difficulty} puzzle generated! Press Ctrl+H for hint, Ctrl+S to solve step-by-step")
            messagebox.showinfo("New Puzzle", f"Generated a {difficulty} puzzle!\n\n{desc}\n\nTip: Press F1 to open the Learning Module!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate puzzle: {e}")
            self.status_var.set("Error generating puzzle")

    def start_timer(self):
        """Start the solve timer"""
        self.timer_running = True
        self.timer_seconds = 0
        self._update_timer()

    def _update_timer(self):
        """Update timer display"""
        if not self.timer_running:
            return

        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60
        if hasattr(self, 'timer_label'):
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

        self.timer_seconds += 1
        self.timer_id = self.root.after(1000, self._update_timer)

    def stop_timer(self):
        """Stop the timer"""
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

    def solve_instantly(self):
        """Solve the puzzle instantly"""
        confirm = self.settings.get('confirm_solve_instantly', True)
        if confirm and not messagebox.askyesno("Solve Instantly", "Are you sure you want to solve the entire puzzle?"):
            return

        self.status_var.set("Solving...")
        self.root.update()

        solver = SudokuSolver(self.sudoku.clone())
        if solver.solve(step_by_step=False):
            self.sudoku = solver.sudoku
            self.grid_widget.set_sudoku(self.sudoku)
            self.stop_timer()
            self.status_var.set("Puzzle solved!")
            messagebox.showinfo("Solved", "Puzzle solved successfully!")
        else:
            messagebox.showerror("Error", "Could not solve this puzzle")
            self.status_var.set("Failed to solve")

    def solve_step_by_step(self):
        """Prepare step-by-step solving"""
        self.status_var.set("Analyzing puzzle...")
        self.root.update()

        self.solver = SudokuSolver(self.sudoku.clone())
        success = self.solver.solve(step_by_step=True)

        if success:
            self.solving_steps = self.solver.get_steps()
            self.current_step = 0

            if self.solving_steps:
                self.step_text.delete(1.0, tk.END)
                self.step_text.insert(tk.END, f"Found {len(self.solving_steps)} solving steps!\n\n")
                self.step_text.insert(tk.END, "Click 'Next Step' or press Ctrl+Right to see each technique.\n")
                self.step_text.insert(tk.END, "Click 'Play All' or press Ctrl+R to auto-play all steps.\n\n")
                self.step_text.insert(tk.END, f"Difficulty: Level {self.solver.get_difficulty_rating()}\n")

                self.step_counter_label.config(text=f"Steps: 0/{len(self.solving_steps)}")

                self.status_var.set(f"Ready to show {len(self.solving_steps)} steps - Press Ctrl+Right for next")
                messagebox.showinfo("Analysis Complete",
                                    f"Found solution using {len(self.solving_steps)} steps!\n"
                                    f"Difficulty Level: {self.solver.get_difficulty_rating()}\n\n"
                                    f"Click 'Next Step' (Ctrl+Right) to see each technique.\n"
                                    f"Click 'Play All' (Ctrl+R) to auto-play through all steps.")
            else:
                messagebox.showinfo("Already Solved", "This puzzle is already solved!")
                self.status_var.set("Puzzle already solved")
        else:
            messagebox.showerror("Error", "Could not solve this puzzle using logical techniques.\n"
                                          "Try 'Solve Instantly' for backtracking solution.")
            self.status_var.set("Could not solve logically")

    def next_step(self):
        """Show next solving step"""
        if not self.solving_steps:
            messagebox.showinfo("No Steps", "Click 'Solve Step-by-Step' first!")
            return

        if self.current_step >= len(self.solving_steps):
            messagebox.showinfo("Complete", "All steps shown! Puzzle solved.")
            self.stop_timer()
            return

        step = self.solving_steps[self.current_step]

        # Display step information
        self.step_text.delete(1.0, tk.END)
        self.step_text.insert(tk.END, f"Step {self.current_step + 1} of {len(self.solving_steps)}\n\n")
        self.step_text.insert(tk.END, f"Technique: {step.technique.replace('_', ' ').title()}\n\n")
        self.step_text.insert(tk.END, f"{step.description}\n\n")

        if step.cells:
            self.step_text.insert(tk.END, f"Cells involved: {step.cells}\n")
        if step.values:
            self.step_text.insert(tk.END, f"Values: {step.values}\n")
        if step.eliminations:
            self.step_text.insert(tk.END, f"\nEliminations:\n")
            for r, c, eliminated in step.eliminations:
                self.step_text.insert(tk.END, f"  ({r+1},{c+1}): remove {eliminated}\n")

        # Highlight involved cells
        self.grid_widget.highlight_cells(step.cells, "#FFEB3B")

        # Apply the step to the grid
        if step.technique in ['naked_single', 'hidden_single']:
            if step.cells and step.values:
                r, c = step.cells[0]
                self.sudoku.set_cell(r, c, step.values[0])

        if step.eliminations:
            for r, c, eliminated in step.eliminations:
                for num in eliminated:
                    self.sudoku.pencil_marks[r][c].discard(num)

        self.grid_widget.update_all()

        self.current_step += 1
        self.step_counter_label.config(text=f"Steps: {self.current_step}/{len(self.solving_steps)}")
        self.status_var.set(f"Step {self.current_step}/{len(self.solving_steps)}: {step.technique}")

    def get_hint(self):
        """Get a hint for the next move"""
        self.status_var.set("Finding hint...")
        self.root.update()

        solver = SudokuSolver(self.sudoku.clone())
        hint = solver.get_hint()

        if hint:
            self.step_text.delete(1.0, tk.END)
            self.step_text.insert(tk.END, "HINT\n\n")
            self.step_text.insert(tk.END, f"Technique: {hint.technique.replace('_', ' ').title()}\n\n")
            self.step_text.insert(tk.END, f"{hint.description}\n\n")

            if hint.cells:
                self.step_text.insert(tk.END, f"Look at: {hint.cells}\n")
                self.grid_widget.highlight_cells(hint.cells, "#FFEB3B")

            self.status_var.set("Hint provided - Check the step display")
        else:
            messagebox.showinfo("No Hint", "No hints available. The puzzle might be solved or very difficult!")
            self.status_var.set("No hint available")

    def auto_pencil_marks(self):
        """Auto-fill all pencil marks"""
        self.grid_widget.auto_fill_pencil_marks()
        self.status_var.set("Pencil marks auto-filled")

    def clear_puzzle(self):
        """Clear all non-initial cells"""
        confirm = self.settings.get('confirm_clear_puzzle', True)
        if confirm and not messagebox.askyesno("Clear Puzzle", "Clear all your entries and start over?"):
            return

        self.sudoku.clear_non_initial()
        self.grid_widget.update_all()
        self.solving_steps = []
        self.current_step = 0
        self.step_text.delete(1.0, tk.END)
        self.step_counter_label.config(text="")
        self.history.clear()
        self.update_undo_redo_buttons()
        self.status_var.set("Puzzle cleared")

    def check_solution(self):
        """Check if current solution is correct"""
        if self.sudoku.is_solved():
            self.stop_timer()
            time_text = ""
            if hasattr(self, 'timer_label'):
                time_text = f"\n\nTime: {self.timer_label.cget('text')}"

            messagebox.showinfo("Correct!", f"Congratulations! You solved it correctly!{time_text}")
            self.status_var.set("Puzzle solved correctly!")
        elif self.sudoku.is_complete():
            messagebox.showwarning("Incorrect", "The puzzle is complete but has errors.")
            self.status_var.set("Solution has errors")
        else:
            filled = sum(1 for r in range(9) for c in range(9) if self.sudoku.grid[r][c] != 0)
            messagebox.showinfo("Incomplete", f"Puzzle not yet complete.\n{filled}/81 cells filled.")
            self.status_var.set(f"{filled}/81 cells filled")

    def on_grid_change(self):
        """Called when grid is modified"""
        self.update_undo_redo_buttons()

    def import_puzzle(self):
        """Import puzzle from file"""
        filepath = filedialog.askopenfilename(
            title="Import Puzzle",
            filetypes=[
                ("JSON files", "*.json"),
                ("SDK files", "*.sdk"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )

        if filepath:
            try:
                self.sudoku = IOHandler.import_puzzle(filepath)
                self.history = HistoryManager(max_history=self.settings.get('max_undo_history', 100))
                self.grid_widget.set_sudoku(self.sudoku)
                self.solving_steps = []
                self.current_step = 0
                self.step_text.delete(1.0, tk.END)
                self.step_counter_label.config(text="")
                self.update_undo_redo_buttons()
                self.status_var.set(f"Imported from {filepath}")
                messagebox.showinfo("Success", "Puzzle imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import puzzle:\n{e}")

    def export_puzzle(self):
        """Export puzzle to file"""
        filepath = filedialog.asksaveasfilename(
            title="Export Puzzle",
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
                ("SDK files", "*.sdk"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )

        if filepath:
            try:
                include_solution = messagebox.askyesno(
                    "Include Solution?",
                    "Include the solution in the export?\n(JSON format only)"
                )
                IOHandler.export_puzzle(self.sudoku, filepath, include_solution)
                self.status_var.set(f"Exported to {filepath}")
                messagebox.showinfo("Success", "Puzzle exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export puzzle:\n{e}")

    def show_teaching_module(self):
        """Open the teaching module window"""
        TeachingModule(self.root)

    def show_new_puzzle_dialog(self):
        """Show dialog for creating new puzzle"""
        self.generate_puzzle(self.difficulty_var.get())

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About Sudoku Learning App",
            "Sudoku Learning Application v1.1\n\n"
            "NEW in v1.1:\n"
            "• Undo/Redo functionality\n"
            "• Keyboard shortcuts\n"
            "• Visual pencil mode indicator\n"
            "• Settings & preferences\n"
            "• Improved step navigation\n"
            "• Play all steps feature\n\n"
            "Features:\n"
            "• Five difficulty levels\n"
            "• Pencil marking support\n"
            "• Import/Export puzzles\n"
            "• AI Solver with step-by-step explanations\n"
            "• Comprehensive teaching module\n\n"
            "Press F1 for help or Ctrl+, for settings!"
        )


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SudokuAppV11(root)
    root.mainloop()


if __name__ == "__main__":
    main()
