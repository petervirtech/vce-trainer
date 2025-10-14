# VCE Exam Player

A comprehensive exam simulation application that can read and play VCE (Visual CertExam) files for training and testing purposes.

## Features

- **VCE File Parsing**: Reads and parses .vce and .vcex exam files
- **Interactive Exam Interface**: Command-line interface for taking exams
- **Session Management**: Save and resume exam sessions
- **Progress Tracking**: Track answered questions and exam progress
- **Scoring System**: Automatic scoring with pass/fail determination
- **Review Mode**: Review completed exams with correct/incorrect indicators
- **Question Navigation**: Jump between questions, mark for review
- **Multiple Question Types**: Support for single and multiple choice questions

## Installation

1. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. **Clone or download the project files**:
   - `vce_parser.py` - VCE file parser module
   - `exam_player.py` - Core exam player functionality
   - `exam_interface.py` - Interactive command-line interface

## Usage

### Starting the Exam Interface

```bash
# Activate virtual environment
source venv/bin/activate

# Start the exam interface with a VCE file
python3 exam_interface.py "path/to/your/exam.vce"
```

### Available Commands

#### Main Menu
- `1` - Start New Exam: Begin a fresh exam session
- `2` - Resume Exam Session: Continue a previously saved session
- `3` - Review Completed Session: Review a finished exam with answers
- `4` - Show Available Sessions: List all saved exam sessions
- `5` - Exit: Quit the application

#### Exam Mode Commands
- `n` - Next question
- `p` - Previous question
- `j` - Jump to question (enter question number)
- `a` - Select answer (choose answer option(s))
- `m` - Mark question for review
- `s` - Show progress (answered/total questions)
- `e` - End exam (calculate final score)
- `q` - Quit to main menu

#### Review Mode Commands
- `n` - Next question
- `p` - Previous question
- `j` - Jump to question
- `q` - Back to main menu

## File Structure

```
vce-trainer/
├── vce/                          # Directory containing VCE files
│   ├── exam1.vce
│   └── exam2.vce
├── sessions/                     # Auto-created directory for session files
│   ├── session_1234567890.json   # Saved exam sessions
│   └── session_1234567891.json
├── vce_parser.py                 # VCE file parser module
├── exam_player.py                # Exam player core functionality
├── exam_interface.py             # Interactive CLI interface
├── main.py                       # Entry point (optional)
└── README.md                     # This file
```

## Session Files

Exam sessions are automatically saved as JSON files in the `sessions/` directory. Each session contains:

- Session metadata (ID, start time, duration)
- User answers and timing information
- Exam progress and scoring
- Question review status

## VCE File Format Support

The parser supports VCE files with the following features:

- Binary format parsing with signature detection
- Question text extraction and cleaning
- Multiple choice answer parsing
- Correct answer identification
- Basic exam metadata (title, author, etc.)

**Note**: Due to the proprietary nature of VCE format, some files may require format-specific adjustments for optimal parsing.

## Example Usage

```bash
# Start exam interface
source venv/bin/activate
python3 exam_interface.py "vce/Microsoft.actualtests.AZ-104.v2025-02-16.by.ida.206q.vce"

# The interface will show:
# Welcome to VCE Exam Player!
# ==================================================
#
# ==================================================
# VCE EXAM PLAYER - MAIN MENU
# ==================================================
# 1. Start New Exam
# 2. Resume Exam Session
# 3. Review Completed Session
# 4. Show Available Sessions
# 5. Exit
# ==================================================
# Select option (1-5):
```

## Troubleshooting

### Common Issues

1. **"VCE file not found"**: Ensure the file path is correct and the VCE file exists.

2. **"No sessions found"**: Sessions are saved in the `sessions/` directory. Check if it exists and contains `.json` files.

3. **Parsing errors**: Some VCE files may use different encoding or format variations. The parser includes fallback mechanisms but may need adjustments for specific files.

4. **Import errors**: Make sure you're running from the virtual environment where dependencies are installed.

### Debug Mode

To see detailed parsing information, the parser outputs debug information when processing VCE files. This can help identify format-specific issues.

## Development

### Adding New Features

The modular design makes it easy to extend:

- **New Question Types**: Add support in `vce_parser.py`
- **UI Improvements**: Modify `exam_interface.py`
- **Scoring Algorithms**: Update scoring logic in `exam_player.py`
- **Export Features**: Add result export functionality

### Testing

Test with multiple VCE files to ensure compatibility:
- Different exam providers
- Various question counts
- Different encoding formats

## License

This project is provided as-is for educational and training purposes.

## Contributing

Contributions are welcome! Areas for improvement:
- Enhanced VCE format support
- GUI interface (Tkinter/PyQt)
- Web-based interface (Flask/Django)
- Progress visualization
- Performance optimizations

---

**Note**: This tool is designed for legitimate educational use with properly licensed exam content. Ensure you have appropriate permissions for any VCE files you use.
