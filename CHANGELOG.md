# Changelog

All notable changes to the Sudoku Learning Application will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.1.0] - 2025-11-16

### 🎉 Major Features Added

#### Undo/Redo System
- **Full undo/redo functionality** with up to 100 moves tracked (configurable)
- Undo with `Ctrl+Z` or ↶ Undo button
- Redo with `Ctrl+Shift+Z`, `Ctrl+Y`, or ↷ Redo button
- Visual counter showing available undos/redos
- Works for both cell values and pencil marks
- Intelligent history management

#### Comprehensive Keyboard Shortcuts
**File Operations:**
- `Ctrl+N` - New Puzzle
- `Ctrl+O` - Open/Import Puzzle
- `Ctrl+E` - Export Puzzle
- `Ctrl+,` - Settings
- `Ctrl+Q` - Quit

**Edit Operations:**
- `Ctrl+Z` - Undo
- `Ctrl+Shift+Z` or `Ctrl+Y` - Redo
- `Space` - Toggle Pencil Mode

**Puzzle Operations:**
- `Ctrl+P` - Auto-fill Pencil Marks
- `Ctrl+K` - Check Solution

**Solver Operations:**
- `Ctrl+H` - Get Hint
- `Ctrl+S` - Solve Step-by-Step
- `Ctrl+Right` - Next Step
- `Ctrl+R` - Play All Steps
- `Ctrl+I` - Solve Instantly

**Help:**
- `F1` - Learning Module

#### Visual Pencil Mode Indicator
- **Large pencil icon** (✎) that changes color when pencil mode is active
- Orange bold icon when active, gray when inactive
- Special cursor in pencil mode
- Clear status bar messages
- Space bar quick toggle

#### Settings & Preferences System
- **Comprehensive settings dialog** with tabbed interface
- **General Tab:**
  - Default difficulty level
  - Max undo history (10-500)
  - Confirmation dialog toggles
- **Appearance Tab:**
  - Theme selection (light/dark)
  - Pencil mark font size (8-14)
  - Cell size (50-80 pixels)
  - Animation speed (slow/normal/fast/instant)
- **Gameplay Tab:**
  - Show/hide errors
  - Auto-update pencil marks
  - Highlight same numbers
  - Show timer
  - Sound effects toggle
- **Colors Tab:**
  - Customizable color scheme
  - Background, cells, highlights, errors
  - Color picker for each element
- Settings saved to user's home directory
- Apply settings without restart (most changes)

#### Improved Step Navigation
- **Play All Steps** feature with auto-advance
- Step counter showing progress (e.g., "Steps: 5/45")
- Configurable animation speed
- Pause auto-play at any time
- Better step display with technique names
- Visual feedback during step execution

### ✨ Enhancements

#### User Experience
- **Better status messages** with contextual information
- **Improved help system** with keyboard shortcuts reference
- **Enhanced About dialog** showing new features
- Confirmation dialogs now configurable
- More informative error messages

#### Visual Improvements
- Larger pencil marks (configurable 8-14pt)
- Better visual feedback for pencil mode
- Improved button labels with shortcuts
- More consistent color scheme
- Better spacing and layout

#### Performance
- Optimized history management
- Efficient undo/redo operations
- No performance impact from new features

### 🔧 Technical Improvements

#### New Modules
- `sudoku_app/core/history.py` - Move history management
- `sudoku_app/gui/settings.py` - Settings system
- `sudoku_app/gui/main_window_v11.py` - Enhanced main window

#### Code Quality
- Better separation of concerns
- More modular architecture
- Enhanced error handling
- Improved documentation

### 📚 Documentation
- Updated README with v1.1 features
- New CHANGELOG.md
- Enhanced inline documentation
- Keyboard shortcuts reference

### 🐛 Bug Fixes
- None (this is the first enhancement release)

### 🔄 Migration Notes
- **v1.0 → v1.1:** Fully backward compatible
- Old `main.py` still works (v1.0)
- Use `main_v11.py` for new features
- Settings file created in `~/.sudoku_learner_settings.json`

---

## [1.0.0] - 2025-11-16

### Initial Release

#### Core Features
- **Five difficulty levels**: Very Easy, Easy, Medium, Hard, Expert
- **Interactive 9×9 grid** with mouse and keyboard control
- **Pencil marking** support for candidate tracking
- **Import/Export** in JSON, SDK, and text formats

#### AI Solver
- **9 solving techniques** implemented:
  1. Naked Singles (Level 1)
  2. Hidden Singles (Level 1)
  3. Pointing Pairs/Triples (Level 2)
  4. Box-Line Reduction (Level 2)
  5. Naked Pairs (Level 2)
  6. Hidden Pairs (Level 2)
  7. Naked Triples (Level 3)
  8. Hidden Triples (Level 3)
  9. X-Wing (Level 4)

- **Three solving modes:**
  - Step-by-step with explanations
  - Instant solve
  - Hint system

#### Teaching Module
- **10 progressive lessons** from beginner to advanced
- Detailed explanations with examples
- Practice tips for each technique
- Easy navigation between lessons

#### Technical
- Pure Python with no external dependencies
- Tkinter-based GUI
- Cross-platform (Linux, Windows, macOS)
- Comprehensive test suite

#### Documentation
- Complete README
- Installation guide
- Usage documentation
- API documentation

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality (backward compatible)
- **PATCH** version for bug fixes (backward compatible)

---

## Upcoming Features

See [FUTURE_PLANS.md](FUTURE_PLANS.md) for the complete roadmap.

### Next Release (v1.2)
- Additional solving techniques (Swordfish, XY-Wing)
- Dark theme implementation
- Timer and statistics
- Improved animations

---

*For more details on each version, see the git tags and commit history.*
