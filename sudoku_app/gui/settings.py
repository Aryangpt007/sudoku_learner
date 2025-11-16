"""
Settings and Preferences Dialog
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import json
import os


class Settings:
    """Application settings manager"""

    DEFAULT_SETTINGS = {
        'theme': 'light',
        'pencil_mark_size': 10,
        'cell_size': 60,
        'show_errors': True,
        'auto_update_pencil_marks': False,
        'highlight_same_numbers': True,
        'animation_speed': 'normal',  # slow, normal, fast, instant
        'sound_effects': False,
        'default_difficulty': 'medium',
        'show_timer': False,
        'confirm_solve_instantly': True,
        'confirm_clear_puzzle': True,
        'max_undo_history': 100,

        # Color customization
        'color_background': '#FFFFFF',
        'color_initial_cell': '#E0E0E0',
        'color_selected': '#BBDEFB',
        'color_highlight': '#E3F2FD',
        'color_same_number': '#FFF9C4',
        'color_error': '#FFCDD2',
        'color_initial_number': '#000000',
        'color_user_number': '#0D47A1',
        'color_pencil_marks': '#666666',
    }

    def __init__(self):
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.settings_file = os.path.expanduser('~/.sudoku_learner_settings.json')
        self.load()

    def load(self):
        """Load settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
        except Exception as e:
            print(f"Could not load settings: {e}")

    def save(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Could not save settings: {e}")

    def get(self, key: str, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)

    def set(self, key: str, value):
        """Set a setting value"""
        self.settings[key] = value

    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.DEFAULT_SETTINGS.copy()


class SettingsDialog(tk.Toplevel):
    """Settings dialog window"""

    def __init__(self, master, settings: Settings, on_apply=None):
        super().__init__(master)
        self.title("Settings & Preferences")
        self.geometry("600x500")
        self.resizable(False, False)

        self.settings = settings
        self.on_apply = on_apply
        self.temp_settings = settings.settings.copy()

        self._create_widgets()

    def _create_widgets(self):
        """Create settings interface"""
        # Notebook for tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # General tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        self._create_general_tab(general_frame)

        # Appearance tab
        appearance_frame = ttk.Frame(notebook)
        notebook.add(appearance_frame, text="Appearance")
        self._create_appearance_tab(appearance_frame)

        # Gameplay tab
        gameplay_frame = ttk.Frame(notebook)
        notebook.add(gameplay_frame, text="Gameplay")
        self._create_gameplay_tab(gameplay_frame)

        # Colors tab
        colors_frame = ttk.Frame(notebook)
        notebook.add(colors_frame, text="Colors")
        self._create_colors_tab(colors_frame)

        # Buttons at bottom
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(button_frame, text="Reset to Defaults", command=self._reset_defaults).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="Apply", command=self._apply, bg="#4CAF50", fg="white").pack(side=tk.RIGHT)

    def _create_general_tab(self, parent):
        """Create general settings tab"""
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Default difficulty
        tk.Label(frame, text="Default Difficulty:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)

        diff_var = tk.StringVar(value=self.temp_settings['default_difficulty'])
        difficulties = ['very_easy', 'easy', 'medium', 'hard', 'expert']
        diff_menu = ttk.Combobox(frame, textvariable=diff_var, values=difficulties, state="readonly", width=15)
        diff_menu.grid(row=0, column=1, sticky=tk.W, pady=5)
        diff_var.trace('w', lambda *args: self._update_temp('default_difficulty', diff_var.get()))

        # Max undo history
        tk.Label(frame, text="Max Undo History:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)

        undo_var = tk.IntVar(value=self.temp_settings['max_undo_history'])
        undo_spin = tk.Spinbox(frame, from_=10, to=500, textvariable=undo_var, width=10)
        undo_spin.grid(row=1, column=1, sticky=tk.W, pady=5)
        undo_var.trace('w', lambda *args: self._update_temp('max_undo_history', undo_var.get()))

        # Confirmation dialogs
        tk.Label(frame, text="Confirmations:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)

        confirm_solve_var = tk.BooleanVar(value=self.temp_settings['confirm_solve_instantly'])
        tk.Checkbutton(frame, text="Confirm before solving instantly", variable=confirm_solve_var,
                      command=lambda: self._update_temp('confirm_solve_instantly', confirm_solve_var.get())).grid(row=3, column=0, columnspan=2, sticky=tk.W)

        confirm_clear_var = tk.BooleanVar(value=self.temp_settings['confirm_clear_puzzle'])
        tk.Checkbutton(frame, text="Confirm before clearing puzzle", variable=confirm_clear_var,
                      command=lambda: self._update_temp('confirm_clear_puzzle', confirm_clear_var.get())).grid(row=4, column=0, columnspan=2, sticky=tk.W)

    def _create_appearance_tab(self, parent):
        """Create appearance settings tab"""
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Theme
        tk.Label(frame, text="Theme:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)

        theme_var = tk.StringVar(value=self.temp_settings['theme'])
        theme_menu = ttk.Combobox(frame, textvariable=theme_var, values=['light', 'dark'], state="readonly", width=15)
        theme_menu.grid(row=0, column=1, sticky=tk.W, pady=5)
        theme_var.trace('w', lambda *args: self._update_temp('theme', theme_var.get()))

        # Pencil mark size
        tk.Label(frame, text="Pencil Mark Font Size:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)

        pencil_var = tk.IntVar(value=self.temp_settings['pencil_mark_size'])
        pencil_spin = tk.Spinbox(frame, from_=8, to=14, textvariable=pencil_var, width=10)
        pencil_spin.grid(row=1, column=1, sticky=tk.W, pady=5)
        pencil_var.trace('w', lambda *args: self._update_temp('pencil_mark_size', pencil_var.get()))

        # Cell size
        tk.Label(frame, text="Cell Size (pixels):", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)

        cell_var = tk.IntVar(value=self.temp_settings['cell_size'])
        cell_spin = tk.Spinbox(frame, from_=50, to=80, textvariable=cell_var, width=10)
        cell_spin.grid(row=2, column=1, sticky=tk.W, pady=5)
        cell_var.trace('w', lambda *args: self._update_temp('cell_size', cell_var.get()))

        # Animation speed
        tk.Label(frame, text="Animation Speed:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=5)

        anim_var = tk.StringVar(value=self.temp_settings['animation_speed'])
        anim_menu = ttk.Combobox(frame, textvariable=anim_var, values=['slow', 'normal', 'fast', 'instant'], state="readonly", width=15)
        anim_menu.grid(row=3, column=1, sticky=tk.W, pady=5)
        anim_var.trace('w', lambda *args: self._update_temp('animation_speed', anim_var.get()))

    def _create_gameplay_tab(self, parent):
        """Create gameplay settings tab"""
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame, text="Gameplay Options:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=5)

        # Show errors
        show_errors_var = tk.BooleanVar(value=self.temp_settings['show_errors'])
        tk.Checkbutton(frame, text="Show errors (red background for invalid moves)", variable=show_errors_var,
                      command=lambda: self._update_temp('show_errors', show_errors_var.get())).pack(anchor=tk.W)

        # Auto update pencil marks
        auto_pencil_var = tk.BooleanVar(value=self.temp_settings['auto_update_pencil_marks'])
        tk.Checkbutton(frame, text="Auto-update pencil marks after each move", variable=auto_pencil_var,
                      command=lambda: self._update_temp('auto_update_pencil_marks', auto_pencil_var.get())).pack(anchor=tk.W)

        # Highlight same numbers
        highlight_var = tk.BooleanVar(value=self.temp_settings['highlight_same_numbers'])
        tk.Checkbutton(frame, text="Highlight cells with same number", variable=highlight_var,
                      command=lambda: self._update_temp('highlight_same_numbers', highlight_var.get())).pack(anchor=tk.W)

        # Show timer
        timer_var = tk.BooleanVar(value=self.temp_settings['show_timer'])
        tk.Checkbutton(frame, text="Show timer", variable=timer_var,
                      command=lambda: self._update_temp('show_timer', timer_var.get())).pack(anchor=tk.W)

        # Sound effects
        sound_var = tk.BooleanVar(value=self.temp_settings['sound_effects'])
        tk.Checkbutton(frame, text="Enable sound effects (when implemented)", variable=sound_var,
                      command=lambda: self._update_temp('sound_effects', sound_var.get())).pack(anchor=tk.W)

    def _create_colors_tab(self, parent):
        """Create color customization tab"""
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame, text="Color Customization:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=5)

        colors = [
            ('Background', 'color_background'),
            ('Initial Cell', 'color_initial_cell'),
            ('Selected Cell', 'color_selected'),
            ('Highlight', 'color_highlight'),
            ('Same Number', 'color_same_number'),
            ('Error', 'color_error'),
        ]

        for i, (label, key) in enumerate(colors):
            row_frame = tk.Frame(frame)
            row_frame.pack(fill=tk.X, pady=2)

            tk.Label(row_frame, text=label + ":", width=15, anchor=tk.W).pack(side=tk.LEFT)

            color_btn = tk.Button(row_frame, text="  ", bg=self.temp_settings[key], width=3,
                                 command=lambda k=key: self._choose_color(k))
            color_btn.pack(side=tk.LEFT, padx=5)

            tk.Label(row_frame, text=self.temp_settings[key]).pack(side=tk.LEFT)

    def _choose_color(self, key):
        """Open color chooser dialog"""
        color = colorchooser.askcolor(self.temp_settings[key])[1]
        if color:
            self.temp_settings[key] = color

    def _update_temp(self, key, value):
        """Update temporary settings"""
        self.temp_settings[key] = value

    def _apply(self):
        """Apply settings"""
        self.settings.settings = self.temp_settings.copy()
        self.settings.save()

        if self.on_apply:
            self.on_apply()

        messagebox.showinfo("Settings", "Settings applied! Some changes may require restarting the application.")
        self.destroy()

    def _reset_defaults(self):
        """Reset to default settings"""
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults?"):
            self.settings.reset_to_defaults()
            self.temp_settings = self.settings.settings.copy()
            self.destroy()
            # Reopen dialog
            SettingsDialog(self.master, self.settings, self.on_apply)
