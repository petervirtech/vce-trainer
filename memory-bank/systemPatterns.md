# System Patterns

## Architectural Patterns

### **Separation of Concerns**
- **Parser Layer** (`vce_parser.py`): Responsible for VCE file format parsing and data extraction
- **Business Logic Layer** (`exam_player.py`): Core exam logic, scoring, session management
- **Presentation Layer**: CLI (`exam_interface.py`) and GUI (`gui/` directory) interfaces

### **Model-View Separation**
- **Model**: Exam data structures, session state, progress tracking
- **View**: UI components (widgets, windows) displaying exam content
- **Controller**: Event handlers and user interaction logic

## Design Patterns

### **Signal/Slot Pattern (PyQt6)**
- Used for decoupling UI components and event handling
- Examples: File selection → exam loading, navigation buttons → question changes
- Enables loose coupling between GUI elements

### **Factory Pattern**
- Exam player instantiation based on VCE file type
- Widget creation for different question types (single/multiple choice)

### **Observer Pattern**
- Progress tracking and status updates
- Timer events and UI refresh notifications

### **Command Pattern**
- User actions (next question, submit answer, mark for review)
- Undo/redo functionality for answer changes

## Module Organization

### **Directory Structure**
```
vce-trainer/
├── gui/                    # UI components
│   ├── main_window.py      # Main application window
│   └── widgets/            # Reusable UI components
├── resources/              # Assets and styling
├── sessions/               # Persistent session data
└── memory-bank/            # Project context documentation
```

### **Import Hierarchy**
- Core modules: `vce_parser`, `exam_player`
- Interface modules: `exam_interface`, `main_gui`
- GUI modules: `gui.main_window`, widget components

## Data Flow Patterns

### **Exam Loading Flow**
1. File selection → VCE parser → Exam data structure
2. Data structure → Exam player initialization
3. Player → UI components population

### **Question Navigation Flow**
1. User input (button click) → Controller method
2. Controller → Model update (current question index)
3. Model change → View refresh (display new question)

### **Session Persistence**
- JSON serialization for exam state
- Automatic save on navigation/answer changes
- Resume capability via deserialization

## Error Handling Patterns
- Graceful degradation for unsupported VCE formats
- User-friendly error messages in GUI
- Logging for debugging and troubleshooting

## Cross-Platform Patterns
- PyQt6 abstraction layer for OS-specific differences
- Path handling with `pathlib` for file system operations
- Virtual environment usage for dependency management

---

*Patterns documented: 2025-10-07T11:01:30Z*
