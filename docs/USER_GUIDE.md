# VCE Exam Player - User Guide

## Getting Started

### 1. Launch the Application
```bash
python3 main_gui.py
```

### 2. Load a VCE File
- Click "📁 Load VCE File" on the welcome screen
- Navigate to your VCE exam file (.vce or .vcex)
- Select the file and click "Open"

### 3. Configure Settings (Optional)
- **Randomize Questions**: Check to randomize question order
- **Question Limit**: Set maximum number of questions (0 = all)
- **Time Limit**: Set exam time limit (0 = no limit)

## Taking an Exam

### Interface Overview
The exam interface consists of:
- **Top Bar**: Progress indicator and timer
- **Question Tab**: Current question and answer options
- **Overview Tab**: Visual grid of all questions with status
- **Navigation Bar**: Previous, Next, Mark for Review, Jump to Question

### Answering Questions
1. **Read the Question**: Question text appears in the top section
2. **Select Answer(s)**:
   - **Single Choice**: Click one radio button (○)
   - **Multiple Choice**: Check multiple checkboxes (☐)
3. **Navigate**: Use Previous/Next buttons or keyboard shortcuts

### Navigation Controls
- **Previous**: Go to previous question (Ctrl+P)
- **Next**: Go to next question (Ctrl+N)
- **Mark for Review**: Flag question for later review (Ctrl+M)
- **Jump to Question**: Go directly to specific question (Ctrl+J)
- **Overview**: Switch to overview tab (Ctrl+O)

### Question Overview
The Overview tab shows:
- **Green**: Answered questions
- **Red**: Marked for review
- **Gray**: Unanswered questions
- **Blue**: Current question

Click any question in the overview to jump directly to it.

## Session Management

### Auto-Save
- Your progress is automatically saved every few minutes
- Sessions are saved when you navigate between questions
- No need to manually save your work

### Resume Session
1. Go to **File → Resume Session**
2. Select from available sessions
3. Choose the session to continue
4. Select the original VCE file when prompted

### Review Completed Session
1. Go to **File → Review Completed Session**
2. Select a completed exam session
3. Review your answers with correct/incorrect highlighting

## Exam Completion

### Finishing the Exam
1. Answer all questions or click "Finish Exam" on the last question
2. Review your final score and pass/fail status
3. Choose to review your answers or return to main menu

### Results Review
- **Green Answers**: Correct answers
- **Red Answers**: Incorrect answers (your selections)
- **Explanations**: Available for some questions
- **Export**: Save results to text file

## Settings and Preferences

### Randomization
- **Enable**: Questions appear in random order
- **Disable**: Questions appear in original sequence
- **Verification**: Check console output for confirmation

### Question Limits
- **All Questions**: Set to 0 or leave blank
- **Limited Set**: Enter specific number (e.g., 50)
- **Random Selection**: Combined with randomization for varied practice

### Time Management
- **No Time Limit**: Set to 0 for unlimited time
- **Timed Exam**: Set minutes for realistic exam simulation
- **Warnings**: Receive alerts when time is running low

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Next Question | Ctrl+N |
| Previous Question | Ctrl+P |
| Mark for Review | Ctrl+M |
| Jump to Question | Ctrl+J |
| Question Tab | Ctrl+Q |
| Overview Tab | Ctrl+O |
| Load VCE File | Ctrl+O |
| Resume Session | Ctrl+R |
| Review Session | Ctrl+Shift+R |

## Tips for Effective Practice

### Study Strategy
1. **First Pass**: Take exam without time pressure
2. **Review Mode**: Study incorrect answers and explanations
3. **Timed Practice**: Simulate real exam conditions
4. **Random Order**: Practice with randomized questions

### Using Randomization
- Enable randomization to avoid memorizing question order
- Practice with different question sets using question limits
- Verify randomization is working by checking console output

### Session Management
- Use resume feature for long exams
- Review completed sessions to identify weak areas
- Export results for progress tracking

## Troubleshooting

### Common Issues

**Q: Only 2-3 answers showing instead of 4**
A: This has been fixed in the latest version. All 4 answers should display correctly.

**Q: Randomization not working**
A: Check the console output for confirmation. You should see messages like:
- `🎲 Randomized: Selected questions [3, 10, 21, 24]` (randomized)
- `📋 Sequential: Using questions [0, 1, 2, 3]` (sequential)

**Q: Can't load VCE file**
A: Ensure the file is a valid .vce or .vcex format and not corrupted.

**Q: Session won't resume**
A: Make sure you select the same VCE file that was used for the original session.

### Getting Help
- Check the console output for error messages
- Verify your VCE files are valid
- Ensure PyQt6 is properly installed
- Check file permissions for the sessions directory

## Advanced Features

### Export Functionality
- Export exam results to text files
- Include detailed answer breakdown
- Save for record keeping or analysis

### Multiple VCE Files
- Load different VCE files for varied practice
- Each file maintains separate session history
- Switch between different certification topics

### Customization
- Adjust interface settings via View → Settings
- Modify question limits and time constraints
- Configure auto-save intervals (future feature)

This user guide covers all the essential features for effective exam preparation with the VCE Exam Player.