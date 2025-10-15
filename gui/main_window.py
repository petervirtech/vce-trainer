"""
Main application window for VCE Exam Player GUI.
"""

import sys
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QTextEdit, QProgressBar, QStatusBar, QMenuBar,
    QMessageBox, QStackedWidget, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence

import json
from pathlib import Path

# Import ExamPlayer only when needed to avoid initialization issues
# from exam_player import ExamPlayer
from .exam_taker import ExamTakerWidget
from .results_viewer import ResultsViewerWidget
from .settings_dialog import SettingsDialog
from .session_manager import SessionManager


class MainWindow(QMainWindow):
    """Main application window for the VCE Exam Player."""

    # Signals
    exam_loaded = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.exam_player: Optional["ExamPlayer"] = None
        self.current_exam_file: Optional[Path] = None
        self.randomize_questions: bool = True  # Default to randomize
        self.max_questions: int = 0  # 0 means all questions
        self.time_limit: int = 0  # 0 means no time limit
        self.settings_file = Path("settings.json")
        
        # Session manager
        self.session_manager = SessionManager()
        self.session_manager.session_saved.connect(self.on_session_saved)
        self.session_manager.auto_save_completed.connect(self.on_auto_save_completed)

        # Load saved settings
        self.load_settings()

        # Simplify initialization for testing
        print("Initializing MainWindow...")

        try:
            self.setup_ui()
            self.setup_menus()
            self.setup_status_bar()
            self.show_welcome_screen()
            print("✓ MainWindow initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing MainWindow: {e}")
            import traceback
            traceback.print_exc()
            raise

    def setup_ui(self):
        """Set up the main user interface."""
        self.setWindowTitle("VCE Exam Player")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)

        # Create central widget with stacked layout for different screens
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        # Header section
        self.setup_header()

        # Main content area - stacked widget for different views
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Footer section
        self.setup_footer()

    def setup_header(self):
        """Set up the header section."""
        header_layout = QHBoxLayout()

        # Modern logo/title area with icon
        title_container = QWidget()
        title_container_layout = QHBoxLayout(title_container)
        title_container_layout.setContentsMargins(0, 0, 0, 0)
        
        # App icon (using emoji for now)
        icon_label = QLabel("🎓")
        icon_label.setStyleSheet("""
            font-size: 32px;
            padding: 8px;
        """)
        title_container_layout.addWidget(icon_label)
        
        # Title with modern typography
        title_label = QLabel("VCE Exam Player")
        title_label.setProperty("class", "title")
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #F8FAFC;
            padding: 12px 8px;
            background: none;
            border: none;
        """)
        title_container_layout.addWidget(title_label)
        
        title_container_layout.addStretch()
        header_layout.addWidget(title_container)

        header_layout.addStretch()

        # Modern action button with icon
        self.load_button = QPushButton("📁 Load VCE File")
        self.load_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3B82F6, stop:1 #2563EB);
                color: white;
                border: none;
                padding: 16px 32px;
                border-radius: 16px;
                font-size: 16px;
                font-weight: 600;
                min-width: 160px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #60A5FA, stop:1 #3B82F6);
    
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563EB, stop:1 #1D4ED8);
            }
        """)
        self.load_button.clicked.connect(self.load_vce_file)
        header_layout.addWidget(self.load_button)

        self.main_layout.addLayout(header_layout)

    def setup_footer(self):
        """Set up the footer section."""
        footer_layout = QHBoxLayout()

        # Status info
        self.status_label = QLabel("Ready to load VCE file")
        self.status_label.setStyleSheet("color: #CAC4D0; padding: 10px;")
        footer_layout.addWidget(self.status_label)

        footer_layout.addStretch()

        # Progress bar (initially hidden)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        footer_layout.addWidget(self.progress_bar)

        self.main_layout.addLayout(footer_layout)

    def setup_menus(self):
        """Set up the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        load_action = QAction('Load VCE File', self)
        load_action.setShortcut(QKeySequence.StandardKey.Open)
        load_action.triggered.connect(self.load_vce_file)
        file_menu.addAction(load_action)

        file_menu.addSeparator()

        resume_action = QAction('Resume Session', self)
        resume_action.setShortcut(QKeySequence('Ctrl+R'))
        resume_action.triggered.connect(self.show_resume_dialog)
        file_menu.addAction(resume_action)

        review_action = QAction('Review Completed Session', self)
        review_action.setShortcut(QKeySequence('Ctrl+Shift+R'))
        review_action.triggered.connect(self.show_review_dialog)
        file_menu.addAction(review_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu('View')

        settings_action = QAction('Settings', self)
        settings_action.triggered.connect(self.show_settings)
        view_menu.addAction(settings_action)

        # Help menu
        help_menu = menubar.addMenu('Help')

        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_status_bar(self):
        """Set up the status bar."""
        self.status_bar = self.statusBar()

        # Current exam info
        self.exam_info_label = QLabel("No exam loaded")
        self.status_bar.addWidget(self.exam_info_label)

        self.status_bar.addPermanentWidget(QLabel("Ready"))

    def show_welcome_screen(self):
        """Show the welcome screen."""
        welcome_widget = QWidget()
        layout = QVBoxLayout(welcome_widget)

        # Welcome message
        welcome_label = QLabel("Welcome to VCE Exam Player")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #FB8C00;
            margin: 20px;
        """)
        layout.addWidget(welcome_label)

        # Description
        desc_label = QLabel(
            "Load a VCE exam file to start practicing for your certification exams.\n"
            "Supports interactive question navigation, progress tracking, and review modes."
        )
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            font-size: 16px;
            color: #CAC4D0;
            margin: 20px;
            line-height: 1.5;
        """)
        layout.addWidget(desc_label)

        # Quick start instructions
        instructions = QLabel(
            "Getting Started:\n"
            "1. Click 'Load VCE File' or use File → Load VCE File\n"
            "2. Select your .vce or .vcex exam file\n"
            "3. Start taking the exam with full navigation and progress tracking"
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setWordWrap(True)
        instructions.setStyleSheet("""
            font-size: 14px;
            color: #E6E1E5;
            background-color: #49454F;
            padding: 20px;
            border-radius: 12px;
            margin: 20px;
            line-height: 1.6;
        """)
        layout.addWidget(instructions)

        # Randomization option
        self.randomize_checkbox = QCheckBox("Randomize question order")
        self.randomize_checkbox.setChecked(self.randomize_questions)
        self.randomize_checkbox.stateChanged.connect(self.on_randomize_changed)
        self.randomize_checkbox.setStyleSheet("""
            font-size: 14px;
            color: #EAE1D9;
            margin: 15px 20px 5px 20px;
        """)
        layout.addWidget(self.randomize_checkbox)

        # Question limit option
        from PyQt6.QtWidgets import QSpinBox
        limit_layout = QHBoxLayout()
        limit_label = QLabel("Number of questions:")
        limit_label.setStyleSheet("font-size: 14px; color: #EAE1D9; margin-left: 20px;")
        self.question_limit_spin = QSpinBox()
        self.question_limit_spin.setRange(0, 1000)
        self.question_limit_spin.setValue(self.max_questions)
        self.question_limit_spin.setSpecialValueText("All questions")
        self.question_limit_spin.setStyleSheet("""
            QSpinBox {
                border: 1px solid #9C8978;
                border-radius: 4px;
                padding: 4px;
                background-color: #15120E;
                color: #EAE1D9;
                min-width: 80px;
            }
        """)
        self.question_limit_spin.valueChanged.connect(self.on_question_limit_changed)
        limit_layout.addWidget(limit_label)
        limit_layout.addWidget(self.question_limit_spin)
        limit_layout.addStretch()
        layout.addLayout(limit_layout)

        # Recent sessions section
        self.setup_recent_sessions(layout)

        layout.addStretch()

        # Add to stacked widget
        self.stacked_widget.addWidget(welcome_widget)
        self.stacked_widget.setCurrentWidget(welcome_widget)

    def load_vce_file(self):
        """Load a VCE file through file dialog."""
        try:
            # File dialog
            file_dialog = QFileDialog(self)
            file_dialog.setWindowTitle("Select VCE Exam File")
            file_dialog.setNameFilter("VCE Files (*.vce *.vcex);;All Files (*)")

            # Default to vce directory if it exists
            vce_dir = Path("vce")
            if vce_dir.exists():
                file_dialog.setDirectory(str(vce_dir))

            if file_dialog.exec():
                selected_files = file_dialog.selectedFiles()
                if selected_files:
                    file_path = Path(selected_files[0])
                    self.load_exam_file(file_path)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file dialog: {e}")

    def load_exam_file(self, file_path: Path):
        """Load and parse the exam file."""
        try:
            self.status_label.setText(f"Loading exam: {file_path.name}")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress

            # Load the exam
            from exam_player import ExamPlayer
            self.exam_player = ExamPlayer(str(file_path))
            self.current_exam_file = file_path

            # Start exam session
            session_id = self.exam_player.start_new_session(
                randomize_questions=self.randomize_questions,
                max_questions=self.max_questions
            )

            # Set up session manager
            self.session_manager.set_exam_player(self.exam_player)

            # Clear any existing exam widgets to prevent caching
            while self.stacked_widget.count() > 1:  # Keep welcome screen (index 0)
                widget = self.stacked_widget.widget(1)
                self.stacked_widget.removeWidget(widget)
                widget.deleteLater()

            # Create new exam taker widget
            self.exam_taker_widget = ExamTakerWidget(self.exam_player)
            self.exam_taker_widget.exam_completed.connect(self.show_results)
            self.stacked_widget.addWidget(self.exam_taker_widget)
            self.stacked_widget.setCurrentWidget(self.exam_taker_widget)

            # Update UI
            self.progress_bar.setVisible(False)
            self.status_label.setText("Exam loaded successfully")

            # Update status bar
            exam_title = self.exam_player.exam.title
            self.exam_info_label.setText(f"Exam: {exam_title}")

            # Emit signal that exam is loaded
            self.exam_loaded.emit()

            # Show exam loaded message
            QMessageBox.information(
                self,
                "Exam Loaded",
                f"Exam loaded successfully!\n"
                f"Title: {exam_title}\n"
                f"Questions: {self.exam_player.exam.total_questions}\n"
                f"Session ID: {session_id}\n"
                f"Ready to start taking the exam."
            )

        except Exception as e:
            self.progress_bar.setVisible(False)
            self.status_label.setText("GUI test failed")
            QMessageBox.critical(self, "Error", f"GUI test failed:\n{str(e)}")

    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About VCE Exam Player",
            "<h3>VCE Exam Player</h3>"
            "<p>A modern GUI application for taking VCE certification exams.</p>"
            "<p><b>Version:</b> 1.0.0</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Interactive exam taking</li>"
            "<li>Progress tracking</li>"
            "<li>Session management</li>"
            "<li>Review mode</li>"
            "</ul>"
        )

    def closeEvent(self, event):
        """Handle application close event."""
        reply = QMessageBox.question(
            self,
            'Confirm Exit',
            'Are you sure you want to exit?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def on_randomize_changed(self, state):
        """Handle randomization checkbox change."""
        self.randomize_questions = state == 2  # Qt.CheckState.Checked
        self.save_settings()

    def on_question_limit_changed(self, value):
        """Handle question limit spin box change."""
        self.max_questions = value
        self.save_settings()

    def load_settings(self):
        """Load settings from file."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                self.randomize_questions = settings.get('randomize_questions', True)
                self.max_questions = settings.get('max_questions', 0)
                self.time_limit = settings.get('time_limit', 0)
        except Exception as e:
            print(f"Warning: Could not load settings: {e}")

    def save_settings(self):
        """Save settings to file."""
        try:
            settings = {
                'randomize_questions': self.randomize_questions,
                'max_questions': self.max_questions,
                'time_limit': self.time_limit
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save settings: {e}")

    def show_results(self):
        """Show the results and review interface."""
        if not self.exam_player or not self.exam_player.current_session:
            return

        # Create results viewer widget
        self.results_viewer = ResultsViewerWidget(self.exam_player)
        self.results_viewer.back_to_main.connect(self.show_welcome_screen)
        self.results_viewer.review_completed.connect(self.show_welcome_screen)

        # Add to stacked widget and switch
        self.stacked_widget.addWidget(self.results_viewer)
        self.stacked_widget.setCurrentWidget(self.results_viewer)

    def show_settings(self):
        """Show the settings dialog."""
        dialog = SettingsDialog(self)
        dialog.set_settings(self.randomize_questions, self.max_questions, self.time_limit)

        if dialog.exec():
            settings = dialog.get_settings()
            self.randomize_questions = settings['randomize_questions']
            self.max_questions = settings['max_questions']
            self.time_limit = settings['time_limit']

            # Update the welcome screen controls
            self.randomize_checkbox.setChecked(self.randomize_questions)
            if hasattr(self, 'question_limit_spin'):
                self.question_limit_spin.setValue(self.max_questions)

            self.save_settings()

    def show_resume_dialog(self):
        """Show dialog to resume a session."""
        resumable_sessions = self.session_manager.get_resumable_sessions()
        
        if not resumable_sessions:
            QMessageBox.information(
                self,
                "No Sessions",
                "No resumable sessions found.\nStart a new exam to create a session."
            )
            return
        
        # Create session selection dialog
        from .session_dialog import SessionSelectionDialog
        dialog = SessionSelectionDialog(resumable_sessions, "Resume Session", self)
        
        if dialog.exec():
            selected_session = dialog.get_selected_session()
            if selected_session:
                self.resume_session(selected_session)

    def show_review_dialog(self):
        """Show dialog to review a completed session."""
        completed_sessions = self.session_manager.get_completed_sessions()
        
        if not completed_sessions:
            QMessageBox.information(
                self,
                "No Sessions",
                "No completed sessions found.\nComplete an exam to review results."
            )
            return
        
        # Create session selection dialog
        from .session_dialog import SessionSelectionDialog
        dialog = SessionSelectionDialog(completed_sessions, "Review Session", self)
        
        if dialog.exec():
            selected_session = dialog.get_selected_session()
            if selected_session:
                self.review_session(selected_session)

    def resume_session(self, session_info: dict):
        """Resume a session from session info."""
        try:
            session_id = session_info['session_id']
            
            # Load the session
            session = self.session_manager.load_session(session_id)
            if not session:
                QMessageBox.critical(self, "Error", f"Failed to load session {session_id}")
                return
            
            # We need to recreate the exam player with the original VCE file
            # For now, we'll ask the user to select the VCE file
            QMessageBox.information(
                self,
                "Select VCE File",
                f"Please select the original VCE file for session:\n{session.exam_title}"
            )
            
            # Open file dialog
            file_dialog = QFileDialog(self)
            file_dialog.setWindowTitle("Select Original VCE File")
            file_dialog.setNameFilter("VCE Files (*.vce *.vcex);;All Files (*)")
            
            if file_dialog.exec():
                selected_files = file_dialog.selectedFiles()
                if selected_files:
                    file_path = Path(selected_files[0])
                    
                    # Load the exam
                    from exam_player import ExamPlayer
                    self.exam_player = ExamPlayer(str(file_path))
                    
                    # Restore the session
                    self.exam_player.current_session = session
                    
                    # Set up session manager
                    self.session_manager.set_exam_player(self.exam_player)
                    
                    # Clear existing widgets
                    while self.stacked_widget.count() > 1:
                        widget = self.stacked_widget.widget(1)
                        self.stacked_widget.removeWidget(widget)
                        widget.deleteLater()
                    
                    # Create exam taker widget
                    self.exam_taker_widget = ExamTakerWidget(self.exam_player)
                    self.exam_taker_widget.exam_completed.connect(self.show_results)
                    self.stacked_widget.addWidget(self.exam_taker_widget)
                    self.stacked_widget.setCurrentWidget(self.exam_taker_widget)
                    
                    # Update UI
                    self.exam_info_label.setText(f"Exam: {session.exam_title} (Resumed)")
                    
                    QMessageBox.information(
                        self,
                        "Session Resumed",
                        f"Successfully resumed session from {session.start_time[:10]}"
                    )
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to resume session: {e}")

    def review_session(self, session_info: dict):
        """Review a completed session."""
        try:
            session_id = session_info['session_id']
            
            # Load the session
            session = self.session_manager.load_session(session_id)
            if not session:
                QMessageBox.critical(self, "Error", f"Failed to load session {session_id}")
                return
            
            # Create a dummy exam player for review
            # We'll create a minimal exam structure from the session
            from exam_player import ExamPlayer, Exam, Question
            
            # Create dummy questions based on session answers
            questions = []
            if session.answers:
                for q_num, user_answer in session.answers.items():
                    question = Question(
                        id=q_num,
                        type="single",
                        question_text=f"Question {q_num} (from completed session)",
                        answers=["Answer A", "Answer B", "Answer C", "Answer D"],
                        correct_answers=[0],  # Will be updated from session
                        explanation="Review from completed session"
                    )
                    questions.append(question)
            
            # Create dummy exam
            dummy_exam = Exam(
                title=session.exam_title,
                description="Review Session",
                author="Session Review",
                version="1.0",
                total_questions=len(questions),
                passing_score=70,
                time_limit=None,
                questions=questions
            )
            
            # Create exam player with dummy exam
            self.exam_player = ExamPlayer.__new__(ExamPlayer)
            self.exam_player.exam = dummy_exam
            self.exam_player.current_session = session
            self.exam_player.question_order = list(range(len(questions)))
            
            # Show results viewer
            self.show_results()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to review session: {e}")

    def setup_recent_sessions(self, parent_layout):
        """Set up recent sessions section on welcome screen."""
        # Recent sessions header
        recent_label = QLabel("Recent Sessions")
        recent_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #FB8C00;
            margin: 20px 20px 10px 20px;
        """)
        parent_layout.addWidget(recent_label)

        # Recent sessions list
        from PyQt6.QtWidgets import QListWidget, QListWidgetItem
        self.recent_sessions_list = QListWidget()
        self.recent_sessions_list.setMaximumHeight(150)
        self.recent_sessions_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #9C8978;
                border-radius: 8px;
                background-color: #15120E;
                color: #EAE1D9;
                font-size: 12px;
                margin: 0px 20px;
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #51453A;
            }
            QListWidget::item:hover {
                background-color: #6B5B4F;
            }
        """)
        self.recent_sessions_list.itemDoubleClicked.connect(self.on_recent_session_clicked)
        parent_layout.addWidget(self.recent_sessions_list)

        # Load recent sessions
        self.load_recent_sessions()

    def load_recent_sessions(self):
        """Load and display recent sessions."""
        try:
            # Get recent sessions (both resumable and completed)
            all_sessions = self.session_manager.list_sessions()
            recent_sessions = all_sessions[:5]  # Show last 5 sessions

            self.recent_sessions_list.clear()

            if not recent_sessions:
                from PyQt6.QtWidgets import QListWidgetItem
                item = QListWidgetItem("No recent sessions found. Load a VCE file to start.")
                item.setData(Qt.ItemDataRole.UserRole, None)
                self.recent_sessions_list.addItem(item)
                return

            from PyQt6.QtWidgets import QListWidgetItem
            for session in recent_sessions:
                # Format session display
                exam_title = session.get('exam_title', 'Unknown Exam')[:40]
                status = session.get('status', 'unknown')
                score = session.get('score')

                if status == 'completed' and score is not None:
                    display_text = f"{exam_title}... - Score: {score}% ({'PASSED' if score >= 70 else 'FAILED'})"
                else:
                    display_text = f"{exam_title}... - {status.title()}"

                item = QListWidgetItem(display_text)
                item.setData(Qt.ItemDataRole.UserRole, session)
                self.recent_sessions_list.addItem(item)

        except Exception as e:
            print(f"Error loading recent sessions: {e}")

    def on_recent_session_clicked(self, item):
        """Handle recent session double-click."""
        session_data = item.data(Qt.ItemDataRole.UserRole)
        if not session_data:
            return

        status = session_data.get('status', 'unknown')

        if status == 'in_progress':
            # Resume session
            self.resume_session(session_data)
        elif status == 'completed':
            # Review session
            self.review_session(session_data)
        else:
            QMessageBox.information(
                self,
                "Unknown Status",
                f"Cannot handle session with status: {status}"
            )

    def on_session_saved(self, session_id: str):
        """Handle session saved signal."""
        self.status_label.setText(f"Session {session_id} saved")

    def on_auto_save_completed(self):
        """Handle auto-save completion."""
        # Could show a subtle indicator that auto-save occurred
        pass
