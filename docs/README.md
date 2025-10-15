# VCE Exam Player Documentation

## Overview

The VCE Exam Player is a modern, feature-rich application for taking practice certification exams from VCE (Visual CertExam) files. It provides both command-line and graphical interfaces with comprehensive session management, progress tracking, and review capabilities.

## Quick Start

### Prerequisites
- Python 3.8+
- PyQt6
- Virtual environment (recommended)

### Installation
```bash
# Clone or download the project
cd vce-exam-player

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install PyQt6
```

### Running the Application

#### GUI Version (Recommended)
```bash
python3 main_gui.py
```

#### Command Line Version
```bash
python3 exam_interface.py "path/to/exam.vce"
```

## Features

### Core Functionality
- ✅ **VCE File Support**: Reads .vce and .vcex exam files
- ✅ **Interactive Exam Taking**: Full exam simulation with navigation
- ✅ **Session Management**: Save, resume, and review exam sessions
- ✅ **Progress Tracking**: Real-time progress monitoring
- ✅ **Automatic Scoring**: Pass/fail determination with detailed results
- ✅ **Question Types**: Single and multiple choice questions

### Advanced Features
- ✅ **Question Randomization**: Randomize question order for varied practice
- ✅ **Timer Support**: Optional time limits with warnings
- ✅ **Review Mode**: Detailed post-exam review with explanations
- ✅ **Session Export**: Export results for record keeping
- ✅ **Modern UI**: Contemporary dark theme with professional appearance

### User Interface
- ✅ **Tabbed Interface**: Question view and overview tabs
- ✅ **Question Overview**: Visual progress grid with status indicators
- ✅ **Navigation Controls**: Previous/Next with keyboard shortcuts
- ✅ **Mark for Review**: Flag questions for later review
- ✅ **Jump to Question**: Quick navigation to specific questions

## Documentation Structure

- [`USER_GUIDE.md`](USER_GUIDE.md) - Complete user guide and tutorials
- [`TECHNICAL_GUIDE.md`](TECHNICAL_GUIDE.md) - Technical implementation details
- [`DEVELOPMENT_LOG.md`](DEVELOPMENT_LOG.md) - Development history and changes
- [`API_REFERENCE.md`](API_REFERENCE.md) - Code documentation and API reference

## Project Structure

```
vce-exam-player/
├── docs/                    # Documentation
├── gui/                     # PyQt6 GUI components
│   ├── widgets/            # Custom GUI widgets
│   ├── main_window.py      # Main application window
│   ├── exam_taker.py       # Exam interface
│   └── results_viewer.py   # Results and review
├── sessions/               # Saved exam sessions
├── vce/                    # VCE exam files
├── exam_player.py          # Core exam logic
├── vce_parser.py           # VCE file parser
├── main_gui.py             # GUI application launcher
└── settings.json           # User preferences
```

## Support

For issues, questions, or contributions, please refer to the technical documentation or development logs in this documentation directory.