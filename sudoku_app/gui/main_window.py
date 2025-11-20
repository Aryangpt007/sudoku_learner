"""
Main Application Window
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from ..core.sudoku import Sudoku
from ..core.solver import SudokuSolver
from ..core.generator import SudokuGenerator
from ..utils.io_handler import IOHandler
from .grid import SudokuGrid
from .teaching import TeachingModule


class SudokuApp:
    """Main Sudoku application window"""

    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Learning Application")
        self.root.resizable(False, False)

        # Initialize with empty puzzle
        self.sudoku = Sudoku()
        self.generator = SudokuGenerator()
        self.solver = None
        self.solving_steps = []
        self.current_step = 0

        self.pencil_mode = False

        self._create_widgets()
        self._create_menu()

        # Generate initial puzzle
        self.generate_puzzle('easy')

    def _create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Puzzle...", command=self.show_new_puzzle_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Import Puzzle...", command=self.import_puzzle)
        file_menu.add_command(label="Export Puzzle...", command=self.export_puzzle)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Puzzle menu
        puzzle_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Puzzle", menu=puzzle_menu)
        puzzle_menu.add_command(label="Clear Non-Initial Cells", command=self.clear_puzzle)
        puzzle_menu.add_command(label="Check Solution", command=self.check_solution)
        puzzle_menu.add_command(label="Auto-fill Pencil Marks", command=self.auto_pencil_marks)

        # Solver menu
        solver_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Solver", menu=solver_menu)
        solver_menu.add_command(label="Get Hint", command=self.get_hint)
        solver_menu.add_command(label="Solve Step-by-Step", command=self.solve_step_by_step)
        solver_menu.add_command(label="Solve Instantly", command=self.solve_instantly)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Learning Module", command=self.show_teaching_module)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)

    def _create_widgets(self):
        """Create main window widgets"""
        # Main container
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack()

        # Left side - Grid
        grid_frame = tk.Frame(main_frame)
        grid_frame.pack(side=tk.LEFT, padx=10)

        self.grid_widget = SudokuGrid(grid_frame, self.sudoku, on_cell_change=self.on_grid_change)
        self.grid_widget.pack()

        # Pencil mode toggle
        pencil_frame = tk.Frame(grid_frame)
        pencil_frame.pack(pady=5)

        self.pencil_var = tk.BooleanVar()
        pencil_check = tk.Checkbutton(
            pencil_frame,
            text="Pencil Mode (for notes)",
            variable=self.pencil_var,
            command=self.toggle_pencil_mode,
            font=("Arial", 10)
        )
        pencil_check.pack()

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
            text="Generate New Puzzle",
            command=lambda: self.generate_puzzle(self.difficulty_var.get()),
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(pady=10, fill=tk.X)

        # Solver Controls
        solver_frame = tk.LabelFrame(control_frame, text="Solver", padx=10, pady=10)
        solver_frame.pack(fill=tk.X, pady=5)

        tk.Button(
            solver_frame,
            text="Get Hint",
            command=self.get_hint,
            bg="#2196F3",
            fg="white"
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            solver_frame,
            text="Solve Step-by-Step",
            command=self.solve_step_by_step,
            bg="#FF9800",
            fg="white"
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            solver_frame,
            text="Next Step",
            command=self.next_step,
            bg="#FFC107",
            fg="black"
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            solver_frame,
            text="Solve Instantly",
            command=self.solve_instantly,
            bg="#F44336",
            fg="white"
        ).pack(fill=tk.X, pady=2)

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
            text="Auto-fill Pencil Marks",
            command=self.auto_pencil_marks
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            other_frame,
            text="Clear Puzzle",
            command=self.clear_puzzle
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            other_frame,
            text="Check Solution",
            command=self.check_solution,
            bg="#9C27B0",
            fg="white"
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            other_frame,
            text="Learning Module",
            command=self.show_teaching_module,
            bg="#00BCD4",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(fill=tk.X, pady=10)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def generate_puzzle(self, difficulty: str):
        """Generate a new puzzle"""
        self.status_var.set(f"Generating {difficulty} puzzle...")
        self.root.update()

        try:
            self.sudoku = self.generator.generate(difficulty)
            self.grid_widget.set_sudoku(self.sudoku)
            self.solving_steps = []
            self.current_step = 0
            self.step_text.delete(1.0, tk.END)

            desc = SudokuGenerator.get_difficulty_description(difficulty)
            self.status_var.set(f"New {difficulty} puzzle generated!")
            messagebox.showinfo("New Puzzle", f"Generated a {difficulty} puzzle!\n\n{desc}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate puzzle: {e}")
            self.status_var.set("Error generating puzzle")

    def solve_instantly(self):
        """Solve the puzzle instantly"""
        if messagebox.askyesno("Solve Instantly", "Are you sure you want to solve the entire puzzle?"):
            self.status_var.set("Solving...")
            self.root.update()

            solver = SudokuSolver(self.sudoku.clone())
            if solver.solve(step_by_step=False):
                self.sudoku = solver.sudoku
                self.grid_widget.set_sudoku(self.sudoku)
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
                self.step_text.insert(tk.END, "Click 'Next Step' to see each technique.\n\n")
                self.step_text.insert(tk.END, f"Difficulty: Level {self.solver.get_difficulty_rating()}\n")

                self.status_var.set(f"Ready to show {len(self.solving_steps)} steps")
                messagebox.showinfo("Analysis Complete",
                                    f"Found solution using {len(self.solving_steps)} steps!\n"
                                    f"Difficulty Level: {self.solver.get_difficulty_rating()}\n\n"
                                    f"Click 'Next Step' to see each technique.")
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
            # Copy the complete solution from solver (in case backtracking filled remaining cells)
            if hasattr(self, 'solver') and self.solver.sudoku.is_solved():
                self.sudoku = self.solver.sudoku
                self.grid_widget.set_sudoku(self.sudoku)
            messagebox.showinfo("Complete", "All steps shown! Puzzle solved.")
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
        # For placement steps
        if step.technique in ['naked_single', 'hidden_single']:
            if step.cells and step.values:
                r, c = step.cells[0]
                self.sudoku.set_cell(r, c, step.values[0])

        # For elimination steps
        if step.eliminations:
            for r, c, eliminated in step.eliminations:
                for num in eliminated:
                    self.sudoku.pencil_marks[r][c].discard(num)

        self.grid_widget.update_all()

        self.current_step += 1
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

            self.status_var.set("Hint provided")
        else:
            messagebox.showinfo("No Hint", "No hints available. The puzzle might be solved or very difficult!")
            self.status_var.set("No hint available")

    def auto_pencil_marks(self):
        """Auto-fill all pencil marks"""
        self.grid_widget.auto_fill_pencil_marks()
        self.status_var.set("Pencil marks auto-filled")

    def clear_puzzle(self):
        """Clear all non-initial cells"""
        if messagebox.askyesno("Clear Puzzle", "Clear all your entries and start over?"):
            self.sudoku.clear_non_initial()
            self.grid_widget.update_all()
            self.solving_steps = []
            self.current_step = 0
            self.step_text.delete(1.0, tk.END)
            self.status_var.set("Puzzle cleared")

    def check_solution(self):
        """Check if current solution is correct"""
        if self.sudoku.is_solved():
            messagebox.showinfo("Correct!", "Congratulations! You solved it correctly!")
            self.status_var.set("Puzzle solved correctly!")
        elif self.sudoku.is_complete():
            messagebox.showwarning("Incorrect", "The puzzle is complete but has errors.")
            self.status_var.set("Solution has errors")
        else:
            # Count filled cells
            filled = sum(1 for r in range(9) for c in range(9) if self.sudoku.grid[r][c] != 0)
            messagebox.showinfo("Incomplete", f"Puzzle not yet complete.\n{filled}/81 cells filled.")
            self.status_var.set(f"{filled}/81 cells filled")

    def toggle_pencil_mode(self):
        """Toggle pencil marking mode"""
        self.pencil_mode = self.pencil_var.get()
        self.grid_widget.set_pencil_mode(self.pencil_mode)
        self.status_var.set("Pencil mode: " + ("ON" if self.pencil_mode else "OFF"))

    def on_grid_change(self):
        """Called when grid is modified"""
        # Could add validation or other logic here
        pass

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
                self.grid_widget.set_sudoku(self.sudoku)
                self.solving_steps = []
                self.current_step = 0
                self.step_text.delete(1.0, tk.END)
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
            "Sudoku Learning Application v1.0\n\n"
            "Features:\n"
            "• Five difficulty levels\n"
            "• Pencil marking support\n"
            "• Import/Export puzzles\n"
            "• AI Solver with step-by-step explanations\n"
            "• Comprehensive teaching module\n\n"
            "Learn and master Sudoku solving techniques!"
        )


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
