# Project Structure & Organization

## Directory Layout
```
vce-exam-player/
├── .kiro/                    # Kiro configuration and steering
├── .mypy_cache/             # MyPy type checking cache
├── __pycache__/             # Python bytecode cache
├── gui/                     # PyQt6 GUI components
│   ├── __pycache__/
│   ├── widgets/             # Custom GUI widgets
│   ├── exam_taker.py        # Main exam interface widget
│   ├── main_window.py       # Application main window
│   ├── results_viewer.py    # Results and review interface
│   └── settings_dialog.py   # Settings configuration dialog
├── memory-bank/             # Project documentation and context
├── resources/               # Static resources
│   └── icons/              # Application icons
├── sessions/                # JSON session save files
├── vce/                     # VCE exam files directory
└── venv/                    # Python virtual environment
```

## Core Application Files
- **`main.py`**: Primary application entry point
- **`main_gui.py`**: GUI application launcher
- **`exam_player.py`**: Core exam logic and session management
- **`vce_parser.py`**: VCE file format parser (binary and text)
- **`exam_interface.py`**: Command-line interface implementation

## Configuration & Data Files
- **`settings.json`**: User preferences and configuration
- **`.gitignore`**: Git ignore patterns
- **`GUI_PLAN.md`**: GUI implementation roadmap
- **`README.md`**: Project documentation and usage instructions

## Testing Files
- **`test_interface.py`**: Interface testing
- **`test_parser.py`**: Parser testing
- **`gui_test.py`**: GUI component testing

## Naming Conventions
- **Python Files**: Snake_case (e.g., `exam_player.py`)
- **Classes**: PascalCase (e.g., `ExamPlayer`, `MainWindow`)
- **Functions/Methods**: Snake_case (e.g., `load_vce_file()`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_PASSING_SCORE`)
- **Session Files**: `session_{timestamp}.json`

## Import Structure
- **Core modules** import from project root
- **GUI modules** use relative imports within `gui/` package
- **External dependencies** imported at module level
- **Type hints** from `typing` module used throughout

## Data Flow Architecture
1. **VCE Files** → `vce_parser.py` → `Exam` dataclass
2. **Exam Data** → `exam_player.py` → `ExamSession` management
3. **Session Data** → JSON persistence in `sessions/`
4. **GUI Components** → PyQt6 widgets in `gui/` directory
5. **User Settings** → `settings.json` configuration file