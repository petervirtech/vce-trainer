# VCE Exam Player - Technical Guide

Comprehensive technical documentation for developers and contributors.

## 🏗️ System Architecture

### High-Level Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GUI Layer     │    │   CLI Layer     │    │  Core Engine    │
│  (PyQt6 UI)     │    │ (Terminal UI)   │    │ (exam_player)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────────────────────────────────────┐
         │              VCE Parser Layer                   │
         │              (vce_parser.py)                    │
         └─────────────────────────────────────────────────┘
                                 │
         ┌─────────────────────────────────────────────────┐
         │               Data Layer                        │
         │        (Sessions, Settings, VCE Files)         │
         └─────────────────────────────────────────────────┘
```

## 📦 Core Components

### 1. Exam Engine (`exam_player.py`)
**Purpose**: Central exam logic and session management  
**Responsibilities**:
- VCE file loading and parsing
- Exam session lifecycle management
- Question ordering and randomization
- Answer recording and scoring
- Session persistence

**Key Classes**:
```python
class ExamPlayer:
    - start_new_session()
    - select_answer()
    - mark_question()
    - end_session()
    - calculate_score()

class ExamSession:
    - session_id: str
    - answers: Dict[int, UserAnswer]
    - start_time: str
    - score: Optional[int]

class UserAnswer:
    - question_id: int
    - selected_answers: List[int]
    - is_correct: Optional[bool]
    - timestamp: str
```

### 2. VCE Parser (`vce_parser.py`)
**Purpose**: VCE file format parsing and question extraction  
**Responsibilities**:
- Binary VCE file decoding
- Question and answer extraction
- Metadata parsing (title, author, etc.)
- Error handling for corrupted files

**Key Classes**:
```python
class Exam:
    - title: str
    - questions: List[Question]
    - total_questions: int
    - passing_score: int

class Question:
    - id: int
    - question_text: str
    - answers: List[str]
    - correct_answers: List[int]
    - explanation: Optional[str]
```

### 3. GUI Framework (`gui/`)
**Purpose**: Modern PyQt6 user interface  
**Structure**:
```
gui/
├── main_window.py      # Main application window
├── exam_taker.py       # Exam interface widget
├── results_viewer.py   # Results and review interface
├── session_manager.py  # Session management UI
├── settings_dialog.py  # Configuration dialog
└── widgets/            # Custom UI components
    ├── question_overview.py
    └── timer_widget.py
```

### 4. Theme System (`modern_theme.py`)
**Purpose**: Contemporary UI styling  
**Features**:
- Dark theme with blue accents (#3B82F6)
- Qt-compatible CSS styling
- Responsive component design
- Accessibility-compliant colors

## 🔄 Data Flow Architecture

### Exam Session Flow
```
1. User loads VCE file
   ↓
2. VCE Parser extracts questions
   ↓
3. ExamPlayer creates session
   ↓
4. GUI displays questions
   ↓
5. User answers questions
   ↓
6. Answers recorded in session
   ↓
7. Session auto-saved
   ↓
8. Exam completed → Results calculated
   ↓
9. Review mode with detailed analysis
```

### Question Randomization
```python
def start_new_session(self, randomize_questions: bool = False, max_questions: int = 0):
    self.question_order = list(range(len(self.exam.questions)))
    
    if max_questions > 0 and max_questions < len(self.question_order):
        if randomize_questions:
            # Randomly select subset
            self.question_order = random.sample(self.question_order, max_questions)
        else:
            # Take first N questions
            self.question_order = self.question_order[:max_questions]
    elif randomize_questions:
        # Shuffle all questions
        random.shuffle(self.question_order)
```

### Session Persistence
```python
@dataclass
class ExamSession:
    session_id: str
    exam_title: str
    start_time: str
    end_time: Optional[str] = None
    status: str = "in_progress"
    answers: Optional[Dict[int, UserAnswer]] = None
    score: Optional[int] = None
    passed: Optional[bool] = None
```

### Answer Display Layout
```python
# Optimized layout for 4 answers
answers_container.setMinimumHeight(520)  # Container
scroll_area.setMinimumHeight(450)        # Scroll area
widget.setMinimumHeight(42)              # Each answer
```

## Data Structures

### Exam Data Model
```python
@dataclass
class Exam:
    title: str
    description: str
    author: str
    version: str
    total_questions: int
    passing_score: int
    time_limit: Optional[int]
    questions: List[Question]

@dataclass
class Question:
    id: int
    type: str  # "single" or "multiple"
    question_text: str
    answers: List[str]
    correct_answers: List[int]
    explanation: Optional[str] = None
```

### Session Management
```python
@dataclass
class UserAnswer:
    question_id: int
    selected_answers: List[int]
    time_spent: int
    timestamp: str
    is_correct: Optional[bool] = None
    is_marked: bool = False
```

## GUI Architecture

### Widget Hierarchy
```
MainWindow
├── QStackedWidget (main content)
│   ├── WelcomeWidget (home screen)
│   ├── ExamTakerWidget (exam interface)
│   │   ├── QTabWidget
│   │   │   ├── QuestionTab
│   │   │   │   ├── QuestionDisplay
│   │   │   │   └── AnswerSelection
│   │   │   └── OverviewTab
│   │   │       └── QuestionOverviewWidget
│   │   └── NavigationControls
│   └── ResultsViewerWidget (review mode)
├── MenuBar
├── StatusBar
└── SessionManager
```

### Event Flow
1. **File Loading**: VCE file → Parser → Exam object
2. **Session Start**: Exam → ExamPlayer → ExamSession
3. **Question Display**: ExamSession → ExamTakerWidget → UI
4. **Answer Recording**: UI → ExamPlayer → UserAnswer
5. **Session Save**: ExamSession → JSON → File system

## Performance Optimizations

### Layout Efficiency
- **Widget Reuse**: Answer widgets created/destroyed per question
- **Lazy Loading**: Questions loaded on-demand
- **Memory Management**: Proper widget cleanup and garbage collection

### Rendering Optimizations
- **CSS Simplification**: Removed unsupported properties (backdrop-filter, transform)
- **Layout Caching**: Efficient layout calculations
- **Scroll Optimization**: Proper scroll area configuration

### Data Management
- **Session Caching**: In-memory session data with periodic saves
- **Question Indexing**: Efficient question order management
- **Answer Tracking**: Optimized answer state management

## File Formats

### VCE File Structure
```
VCE files contain:
- Header information (title, author, version)
- Question data (text, answers, correct answers)
- Metadata (passing score, time limits)
- Binary encoding with compression
```

### Session Files (JSON)
```json
{
  "session_id": "session_1234567890",
  "exam_title": "Azure AZ-305 Practice Exam",
  "start_time": "2024-01-15T10:30:00",
  "status": "completed",
  "answers": {
    "1": {
      "question_id": 1,
      "selected_answers": [0],
      "is_correct": true,
      "is_marked": false
    }
  },
  "score": 85,
  "passed": true
}
```

### Settings File (JSON)
```json
{
  "randomize_questions": true,
  "max_questions": 50,
  "time_limit": 120,
  "auto_save_interval": 300
}
```

## Styling System

### Theme Architecture
```python
def apply_modern_theme(app: QApplication):
    # Set system fonts
    font = QFont("System", 13)
    app.setFont(font)
    
    # Configure color palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(16, 16, 20))
    
    # Apply stylesheet
    app.setStyleSheet(modern_stylesheet)
```

### Color System
```css
/* Primary Colors */
--primary: #3B82F6;      /* Blue accent */
--success: #10B981;      /* Green */
--error: #EF4444;        /* Red */
--warning: #F59E0B;      /* Orange */

/* Background Colors */
--bg-primary: #101014;   /* Main background */
--bg-secondary: #18181B; /* Surface background */
--bg-tertiary: #27272A;  /* Elevated surface */

/* Text Colors */
--text-primary: #F8FAFC; /* Primary text */
--text-secondary: #E5E7EB; /* Secondary text */
--text-muted: #9CA3AF;   /* Muted text */
```

## Error Handling

### Exception Management
```python
try:
    exam = parse_vce_file(file_path)
except VCEParseError as e:
    QMessageBox.critical(self, "Parse Error", f"Failed to parse VCE file: {e}")
except FileNotFoundError:
    QMessageBox.critical(self, "File Error", "VCE file not found")
except Exception as e:
    QMessageBox.critical(self, "Error", f"Unexpected error: {e}")
```

### Graceful Degradation
- **Missing Files**: Fallback to default settings
- **Corrupted Sessions**: Session recovery mechanisms
- **Invalid VCE Files**: Clear error messages and recovery options

## Testing Strategy

### Unit Testing
- **Parser Testing**: VCE file parsing validation
- **Session Testing**: Session lifecycle verification
- **Scoring Testing**: Answer evaluation accuracy

### Integration Testing
- **GUI Testing**: Widget interaction validation
- **File I/O Testing**: Session save/load verification
- **Theme Testing**: CSS rendering validation

### User Acceptance Testing
- **Answer Display**: All 4 answers visible
- **Randomization**: Console output verification
- **Session Flow**: Complete exam lifecycle testing

## Deployment Considerations

### Dependencies
```
PyQt6>=6.0.0
Python>=3.8
```

### Platform Support
- **macOS**: Native system fonts and styling
- **Windows**: Windows-specific font fallbacks
- **Linux**: Ubuntu/system font support

### Performance Requirements
- **Memory**: ~50MB typical usage
- **Storage**: Minimal (sessions and settings)
- **CPU**: Low usage, GUI rendering only

## Future Enhancements

### Planned Features
- **Plugin System**: Custom question type support
- **Analytics Dashboard**: Performance tracking
- **Cloud Sync**: Session synchronization
- **Mobile Support**: Responsive design for tablets

### Technical Debt
- **Code Documentation**: Comprehensive docstring coverage
- **Test Coverage**: Increase unit test coverage to 90%+
- **Performance Profiling**: Identify optimization opportunities
- **Accessibility**: Enhanced screen reader support

This technical guide provides comprehensive information for developers working with or extending the VCE Exam Player codebase.## 
🎨 UI Architecture

### Widget Hierarchy
```
MainWindow (QMainWindow)
├── QStackedWidget (main content)
│   ├── WelcomeWidget
│   ├── ExamTakerWidget
│   │   ├── QTabWidget
│   │   │   ├── Question Tab
│   │   │   │   ├── Question Display (QTextEdit)
│   │   │   │   └── Answer Selection (QScrollArea)
│   │   │   │       └── Answer Widgets (QRadioButton/QCheckBox)
│   │   │   └── Overview Tab (QuestionOverviewWidget)
│   │   └── Navigation Controls
│   └── ResultsViewerWidget
│       ├── Results Summary
│       ├── Question List (QListWidget)
│       └── Question Detail Panel
├── MenuBar
├── StatusBar
└── Timer Widget
```

### Layout Optimization
Recent improvements have simplified the answer display structure:

```python
# Before: Complex nesting causing layout conflicts
answers_frame -> answers_layout -> scroll_area -> scroll_widget -> scroll_layout

# After: Clean, direct structure  
answers_container -> container_layout -> scroll_area -> answers_widget -> scroll_layout
```

**Container Sizing**:
- **Scroll Area**: 450-500px height (optimized from 350-400px)
- **Container**: 520-580px height (optimized from 450-500px)
- **Answer Widgets**: 42-55px height each with 4px spacing

## 💾 Data Management

### Session Persistence
**Format**: JSON files in `sessions/` directory  
**Structure**:
```json
{
  "session_id": "session_1234567890",
  "exam_title": "Azure AZ-305 Practice",
  "start_time": "2024-12-01T10:00:00",
  "end_time": "2024-12-01T11:30:00",
  "status": "completed",
  "answers": {
    "1": {
      "question_id": 1,
      "selected_answers": [0],
      "is_correct": true,
      "timestamp": "2024-12-01T10:05:00"
    }
  },
  "score": 85,
  "passed": true
}
```

### Settings Management
**File**: `settings.json`  
**Configuration**:
```json
{
  "randomize_questions": true,
  "max_questions": 50,
  "time_limit": 90,
  "theme": "dark",
  "auto_save_interval": 30
}
```

## 🔧 Design Patterns

### 1. Model-View-Controller (MVC)
- **Model**: `ExamPlayer`, `ExamSession` (business logic)
- **View**: GUI widgets (`MainWindow`, `ExamTakerWidget`)
- **Controller**: Event handlers and signal connections

### 2. Observer Pattern
- **Signals/Slots**: PyQt6 signal system for UI updates
- **Event Handling**: User actions trigger appropriate responses
- **State Synchronization**: UI reflects model state changes

### 3. Strategy Pattern
- **Question Selection**: Different strategies for randomized vs sequential
- **Scoring**: Configurable scoring algorithms
- **Theme Application**: Pluggable theme system

### 4. Factory Pattern
- **Widget Creation**: Dynamic widget creation based on question type
- **Parser Selection**: Different parsers for different VCE formats
- **Session Creation**: Session factory with different configurations

## 🚀 Performance Optimization

### Memory Management
- **Widget Lifecycle**: Proper cleanup of dynamically created widgets
- **Session Data**: Efficient storage and retrieval of large sessions
- **VCE Parsing**: Streaming parser for large files
- **Garbage Collection**: Explicit cleanup of resources

### UI Responsiveness
- **Lazy Loading**: Questions loaded on-demand
- **Background Processing**: Non-blocking file operations
- **Efficient Updates**: Minimal UI redraws
- **Caching**: Parsed VCE data cached in memory

### Scalability Features
- **Large Exams**: Support for 1000+ question exams
- **Multiple Sessions**: Concurrent session management
- **File Size**: Efficient handling of large VCE files
- **Memory Usage**: Optimized data structures

## 🔒 Security & Reliability

### Data Integrity
- **Session Validation**: Checksums for session files
- **Error Recovery**: Graceful handling of corrupted data
- **Backup Strategy**: Automatic session backups
- **Data Validation**: Input sanitization and validation

### Error Handling
- **Exception Management**: Comprehensive try-catch blocks
- **User Feedback**: Clear error messages and recovery options
- **Logging**: Detailed logging for debugging
- **Graceful Degradation**: Fallback options for failures

## 🧪 Testing Framework

### Test Structure
```
tests/
├── unit/
│   ├── test_exam_player.py
│   ├── test_vce_parser.py
│   └── test_session_manager.py
├── integration/
│   ├── test_gui_integration.py
│   └── test_end_to_end.py
└── fixtures/
    ├── sample.vce
    └── test_sessions/
```

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **GUI Tests**: User interface testing
- **End-to-End Tests**: Complete workflow testing

## 📈 Extensibility

### Plugin Architecture
- **Parser Plugins**: Support for additional file formats
- **Theme Plugins**: Custom theme development
- **Export Plugins**: Different result export formats
- **Widget Plugins**: Custom UI components

### Configuration System
- **Settings Framework**: Extensible configuration management
- **User Preferences**: Customizable user experience
- **Admin Settings**: System-wide configuration options
- **Environment Variables**: Runtime configuration

## 🔄 Recent Technical Improvements

### Answer Display Fix
**Problem**: Only 2-3 answers showing instead of all 4 (A, B, C, D)  
**Solution**: Simplified layout with proper container sizing
- Removed complex nested scroll areas causing layout conflicts
- Added direct container with proper height allocation
- Result: All 4 answers now display reliably across all question types

### Modern UI Implementation
**Improvements**:
- Contemporary dark theme with blue accents (#3B82F6)
- System fonts with proper weight hierarchy
- Rounded corners, subtle shadows, hover effects
- Clean spacing and visual hierarchy

### Review Mode Enhancement
**Features**:
- Green for correct, red for incorrect, gray for unanswered
- Rich HTML formatting with color-coded status labels
- Clear indicators like `[CORRECT ANSWER]`, `[INCORRECT - Your Answer]`
- Better contrast and readability

## 🛠️ Development Setup

### Environment Requirements
```bash
# Python 3.8+ required
python3 --version

# Virtual environment setup
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install PyQt6
```

### Project Structure
```
vce-exam-player/
├── .kiro/                    # Kiro configuration
├── .mypy_cache/             # Type checking cache
├── __pycache__/             # Python bytecode cache
├── gui/                     # PyQt6 GUI components
├── docs/                    # Documentation
├── sessions/                # JSON session files
├── vce/                     # VCE exam files
├── exam_player.py           # Core exam logic
├── vce_parser.py           # VCE file parser
├── main_gui.py             # GUI launcher
└── settings.json           # Configuration
```

### Development Commands
```bash
# Run GUI application
python3 main_gui.py

# Run CLI interface
python3 exam_interface.py "path/to/exam.vce"

# Type checking (if mypy installed)
mypy exam_player.py vce_parser.py

# Run tests
python3 test_parser.py
python3 test_interface.py
```

## 📊 Code Quality Standards

### Type Safety
- **Type Hints**: Extensive use throughout codebase
- **Dataclasses**: For structured data representation
- **MyPy**: Static type checking
- **Runtime Validation**: Input validation and sanitization

### Documentation Standards
- **Docstrings**: Comprehensive function and class documentation
- **Inline Comments**: Clear explanations of complex logic
- **Type Annotations**: Full type hint coverage
- **Usage Examples**: Code samples and demonstrations

### Performance Guidelines
- **Efficient Algorithms**: Optimized data structures and algorithms
- **Memory Management**: Proper resource cleanup
- **UI Responsiveness**: Non-blocking operations
- **Caching Strategies**: Intelligent data caching

---

This technical guide provides comprehensive information for developers working with or extending the VCE Exam Player application. The architecture is designed for maintainability, extensibility, and performance.