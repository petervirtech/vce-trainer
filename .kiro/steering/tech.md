# Technology Stack & Build System

## Core Technologies
- **Python**: 3.8+ (primary language)
- **GUI Framework**: PyQt6 for desktop interface
- **CLI Framework**: Built-in Python argparse and input handling
- **Data Formats**: JSON for session persistence, binary VCE file parsing

## Key Libraries & Dependencies
- **PyQt6**: Modern GUI framework for cross-platform desktop app
- **pathlib**: File system operations
- **json**: Session data serialization
- **struct**: Binary VCE file parsing
- **zlib**: VCE file decompression
- **dataclasses**: Type-safe data structures
- **typing**: Type hints and annotations

## Project Structure
- **Core Logic**: `exam_player.py`, `vce_parser.py`, `exam_interface.py`
- **GUI Components**: `gui/` directory with PyQt6 widgets
- **Data Storage**: `sessions/` for JSON session files, `vce/` for exam files
- **Configuration**: `settings.json` for user preferences

## Development Environment
```bash
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies (when requirements.txt exists)
pip install -r requirements.txt

# Or install manually
pip install PyQt6
```

## Common Commands
```bash
# Run CLI interface
python3 exam_interface.py "path/to/exam.vce"

# Run GUI interface
python3 main_gui.py

# Run with specific VCE file
python3 main.py

# Type checking (if mypy configured)
mypy exam_player.py vce_parser.py

# Testing (basic Python testing)
python3 test_parser.py
python3 test_interface.py
```

## Code Quality Tools
- **MyPy**: Type checking (cache in `.mypy_cache/`)
- **Type Hints**: Extensive use throughout codebase
- **Dataclasses**: For structured data representation
- **Error Handling**: Comprehensive exception handling for file operations