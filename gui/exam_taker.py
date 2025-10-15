"""
Exam Taker Widget for VCE Exam Player GUI.
Handles question display, answer selection, and exam navigation.
"""

import sys
from typing import List, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton,
    QCheckBox, QButtonGroup, QPushButton, QTextEdit, QScrollArea,
    QFrame, QMessageBox, QProgressBar, QSplitter, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QKeySequence, QShortcut

from exam_player import ExamPlayer
from .widgets import QuestionOverviewWidget, TimerWidget


class ExamTakerWidget(QWidget):
    """Widget for taking exams with question display and answer selection."""

    # Signals
    answer_selected = pyqtSignal(int, list)  # question_num, selected_answers
    next_question_requested = pyqtSignal()
    previous_question_requested = pyqtSignal()
    mark_question_requested = pyqtSignal(int)  # question_num
    exam_completed = pyqtSignal()

    def __init__(self, exam_player: ExamPlayer):
        super().__init__()
        self.player = exam_player
        self.current_question_num = 1
        self.answer_widgets: List[QWidget] = []
        self.button_group = QButtonGroup()

        self.setup_ui()
        self.setup_shortcuts()
        self.load_question(self.current_question_num)

    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)

        # Top bar with timer and progress
        self.setup_top_bar(layout)

        # Main content area with tabs
        self.setup_main_content(layout)

        # Navigation area
        self.setup_navigation(layout)

    def setup_question_display(self, parent_layout: QVBoxLayout):
        """Set up the question display area."""
        question_frame = QFrame()
        question_frame.setFrameStyle(QFrame.Shape.Box)
        question_layout = QVBoxLayout(question_frame)

        # Question number and type
        self.question_header = QLabel()
        self.question_header.setStyleSheet("font-weight: bold; font-size: 18px; color: #FB8C00;")
        question_layout.addWidget(self.question_header)

        # Question text - more compact
        self.question_text = QTextEdit()
        self.question_text.setReadOnly(True)
        self.question_text.setMinimumHeight(80)   # Further reduced to save space
        self.question_text.setMaximumHeight(140)  # Reduced max height for more answer space
        self.question_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid rgba(75, 85, 99, 0.3);
                border-radius: 8px;
                padding: 12px;
                background-color: rgba(24, 24, 27, 0.8);
                color: #F3F4F6;
                font-size: 15px;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border: 2px solid #3B82F6;
            }
        """)
        question_layout.addWidget(self.question_text)

        parent_layout.addWidget(question_frame)

    def setup_answer_selection(self, parent_layout: QVBoxLayout):
        """Set up the answer selection area."""
        # Create answers container with proper sizing
        answers_container = QWidget()
        answers_container.setStyleSheet("""
            QWidget {
                background-color: rgba(24, 24, 27, 0.8);
                border: 1px solid rgba(75, 85, 99, 0.3);
                border-radius: 12px;
                padding: 10px;
            }
        """)
        
        # Use a simple vertical layout
        container_layout = QVBoxLayout(answers_container)
        container_layout.setSpacing(8)
        container_layout.setContentsMargins(16, 16, 16, 16)

        # Answer selection label
        self.answers_label = QLabel("Select your answer(s):")
        self.answers_label.setStyleSheet("""
            font-weight: bold; 
            font-size: 16px; 
            color: #3B82F6; 
            margin-bottom: 0px;
        """)
        container_layout.addWidget(self.answers_label)
        
        # Create scroll area for answers to ensure all are visible
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        # Create widget to hold answer widgets
        self.answers_widget = QWidget()
        self.answers_widget.setStyleSheet("background-color: transparent;")
        self.scroll_layout = QVBoxLayout(self.answers_widget)
        self.scroll_layout.setSpacing(4)
        self.scroll_layout.setContentsMargins(6, 6, 6, 6)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll_area.setWidget(self.answers_widget)
        scroll_area.setMinimumHeight(450)  # Much larger height to avoid scrolling
        scroll_area.setMaximumHeight(500)  # Generous max height
        
        container_layout.addWidget(scroll_area)
        
        # Set much larger container height to accommodate all answers comfortably
        answers_container.setMinimumHeight(520)
        answers_container.setMaximumHeight(580)
        
        parent_layout.addWidget(answers_container)

    def setup_navigation(self, parent_layout: QVBoxLayout):
        """Set up the navigation and control buttons."""
        nav_layout = QHBoxLayout()

        # Previous button
        self.prev_button = QPushButton("← Previous")
        self.prev_button.clicked.connect(self.previous_question)
        nav_layout.addWidget(self.prev_button)

        # Mark for review button
        self.mark_button = QPushButton("⚑ Mark for Review")
        self.mark_button.setCheckable(True)
        self.mark_button.clicked.connect(self.toggle_mark_question)
        nav_layout.addWidget(self.mark_button)

        # Jump to question button
        jump_button = QPushButton("⤴ Jump to Question (Ctrl+J)")
        jump_button.clicked.connect(self.show_jump_dialog)
        nav_layout.addWidget(jump_button)

        # Spacer
        nav_layout.addStretch()

        # Next button
        self.next_button = QPushButton("Next →")
        self.next_button.clicked.connect(self.next_question)
        nav_layout.addWidget(self.next_button)

        parent_layout.addLayout(nav_layout)

    def setup_top_bar(self, parent_layout: QVBoxLayout):
        """Set up the top bar with timer and progress."""
        top_layout = QHBoxLayout()
        
        # Progress info
        self.progress_label = QLabel()
        self.progress_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #FB8C00;
            padding: 8px;
        """)
        top_layout.addWidget(self.progress_label)
        
        top_layout.addStretch()
        
        # Timer widget
        time_limit = getattr(self.player.exam, 'time_limit', 0) or 0
        self.timer_widget = TimerWidget(time_limit)
        self.timer_widget.time_warning.connect(self.on_time_warning)
        self.timer_widget.time_expired.connect(self.on_time_expired)
        top_layout.addWidget(self.timer_widget)
        
        parent_layout.addLayout(top_layout)
        
        # Start timer
        self.timer_widget.start_timer()

    def setup_main_content(self, parent_layout: QVBoxLayout):
        """Set up the main content area with tabs."""
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #9C8978;
                border-radius: 8px;
                background-color: #1F1B16;
            }
            QTabBar::tab {
                background-color: #51453A;
                color: #D5C4B5;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #FB8C00;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #6B5B4F;
            }
        """)
        
        # Question tab
        question_widget = QWidget()
        question_layout = QVBoxLayout(question_widget)
        
        # Question display area
        self.setup_question_display(question_layout)
        
        # Answer selection area
        self.setup_answer_selection(question_layout)
        
        self.tab_widget.addTab(question_widget, "Question")
        
        # Overview tab
        self.overview_widget = QuestionOverviewWidget(self.player)
        self.overview_widget.question_selected.connect(self.jump_to_question)
        self.tab_widget.addTab(self.overview_widget, "Overview")
        
        parent_layout.addWidget(self.tab_widget)

    def setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        # Navigation shortcuts
        next_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        next_shortcut.activated.connect(self.next_question)
        
        prev_shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        prev_shortcut.activated.connect(self.previous_question)
        
        # Mark shortcut
        mark_shortcut = QShortcut(QKeySequence("Ctrl+M"), self)
        mark_shortcut.activated.connect(self.toggle_mark_question)
        
        # Overview shortcut
        overview_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        overview_shortcut.activated.connect(lambda: self.tab_widget.setCurrentIndex(1))
        
        # Question shortcut
        question_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        question_shortcut.activated.connect(lambda: self.tab_widget.setCurrentIndex(0))
        
        # Jump to question shortcut
        jump_shortcut = QShortcut(QKeySequence("Ctrl+J"), self)
        jump_shortcut.activated.connect(self.show_jump_dialog)

    def on_time_warning(self, minutes_remaining: int):
        """Handle time warning."""
        from PyQt6.QtWidgets import QMessageBox
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Time Warning")
        msg_box.setText(f"⏰ Only {minutes_remaining} minutes remaining!")
        msg_box.setInformativeText("Please manage your time carefully.")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.exec()

    def on_time_expired(self):
        """Handle time expiration."""
        from PyQt6.QtWidgets import QMessageBox
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Time Expired")
        msg_box.setText("⏰ Time has expired!")
        msg_box.setInformativeText("The exam will be submitted automatically.")
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.exec()
        self.complete_exam()

    def jump_to_question(self, question_num: int):
        """Jump to a specific question from overview."""
        if 1 <= question_num <= len(self.player.question_order):
            self.current_question_num = question_num
            self.load_question(question_num)
            # Switch back to question tab
            self.tab_widget.setCurrentIndex(0)

    def load_question(self, question_num: int):
        """Load and display a specific question."""
        if not (1 <= question_num <= len(self.player.question_order)):
            return

        self.current_question_num = question_num
        # Use question_order to get the correct question (handles randomization)
        question_idx = self.player.question_order[question_num - 1]
        question = self.player.exam.questions[question_idx]

        # Update progress
        total_questions = len(self.player.question_order)
        self.progress_label.setText(f"Question {question_num} of {total_questions}")

        # Update question header
        question_type = "Multiple Choice" if len(question.correct_answers) > 1 else "Single Choice"
        self.question_header.setText(f"Question {question_num} of {total_questions} - {question_type}")
        
        # Update overview widget
        if hasattr(self, 'overview_widget'):
            self.overview_widget.set_current_question(question_num)

        # Update question text
        self.question_text.setPlainText(question.question_text)

        # Clear existing answer widgets
        self.clear_answer_widgets()

        # Create new answer widgets
        self.create_answer_widgets(question)

        # Update navigation buttons
        self.update_navigation_buttons()

        # Update mark button state
        self.update_mark_button()

    def create_answer_widgets(self, question):
        """Create answer selection widgets based on question type."""
        is_multiple_choice = len(question.correct_answers) > 1

        for i, answer_text in enumerate(question.answers):
            # Create widget
            if is_multiple_choice:
                widget = QCheckBox(f"{chr(65 + i)}. {answer_text}")
                widget.stateChanged.connect(self.on_answer_changed)
            else:
                widget = QRadioButton(f"{chr(65 + i)}. {answer_text}")
                self.button_group.addButton(widget, i)
                widget.toggled.connect(self.on_answer_changed)

            # Clean, modern styling optimized for 4 answers
            widget.setStyleSheet("""
                QCheckBox, QRadioButton {
                    font-size: 14px;
                    font-weight: 500;
                    color: #F3F4F6;
                    padding: 8px 12px;
                    margin: 2px 0;
                    background-color: rgba(39, 39, 42, 0.8);
                    border: 1px solid rgba(75, 85, 99, 0.5);
                    border-radius: 8px;
                }
                QCheckBox:hover, QRadioButton:hover {
                    background-color: rgba(59, 130, 246, 0.1);
                    border: 1px solid rgba(96, 165, 250, 0.7);
                }
                QCheckBox:checked, QRadioButton:checked {
                    background-color: rgba(59, 130, 246, 0.3);
                    border: 2px solid #3B82F6;
                    color: #FFFFFF;
                    font-weight: 600;
                }
                QCheckBox::indicator, QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
            """)
            
            # Set optimal height for fitting 4 answers
            widget.setMinimumHeight(42)
            widget.setMaximumHeight(55)
            
            # Add to the answers layout
            self.scroll_layout.addWidget(widget)
            self.answer_widgets.append(widget)

        # Ensure proper layout updates
        self.answers_widget.adjustSize()
        self.answers_widget.updateGeometry()
        
        # Load existing answers if any
        self.load_existing_answers()

    def clear_answer_widgets(self):
        """Clear all answer widgets."""
        for widget in self.answer_widgets:
            widget.setParent(None)
            widget.deleteLater()
        self.answer_widgets.clear()
        self.button_group = QButtonGroup()  # Reset button group

    def load_existing_answers(self):
        """Load previously selected answers for current question."""
        if (self.player.current_session and
            self.player.current_session.answers and
            self.current_question_num in self.player.current_session.answers):

            user_answer = self.player.current_session.answers[self.current_question_num]
            selected_indices = user_answer.selected_answers

            for i, widget in enumerate(self.answer_widgets):
                if isinstance(widget, QCheckBox):
                    widget.setChecked(i in selected_indices)
                elif isinstance(widget, QRadioButton):
                    widget.setChecked(i in selected_indices)

    def on_answer_changed(self):
        """Handle answer selection changes."""
        selected_answers = []
        for i, widget in enumerate(self.answer_widgets):
            if isinstance(widget, QCheckBox) and widget.isChecked():
                selected_answers.append(i)
            elif isinstance(widget, QRadioButton) and widget.isChecked():
                selected_answers = [i]
                break

        # Record answer in player
        self.player.select_answer(self.current_question_num, selected_answers)

        # Update overview widget
        if hasattr(self, 'overview_widget'):
            self.overview_widget.update_question_status(self.current_question_num)

        # Emit signal
        self.answer_selected.emit(self.current_question_num, selected_answers)

    def next_question(self):
        """Move to the next question."""
        if self.current_question_num < len(self.player.question_order):
            self.current_question_num += 1
            self.load_question(self.current_question_num)
            self.next_question_requested.emit()
        else:
            # Exam completed
            self.complete_exam()

    def previous_question(self):
        """Move to the previous question."""
        if self.current_question_num > 1:
            self.current_question_num -= 1
            self.load_question(self.current_question_num)
            self.previous_question_requested.emit()

    def toggle_mark_question(self):
        """Toggle mark for review status."""
        is_marked = self.mark_button.isChecked()
        self.player.mark_question(self.current_question_num)
        self.mark_question_requested.emit(self.current_question_num)

    def update_navigation_buttons(self):
        """Update navigation button states."""
        self.prev_button.setEnabled(self.current_question_num > 1)
        self.next_button.setText("✓ Finish Exam" if self.current_question_num == len(self.player.question_order) else "Next →")

    def update_mark_button(self):
        """Update mark button state."""
        if (self.player.current_session and
            self.player.current_session.answers and
            self.current_question_num in self.player.current_session.answers):
            user_answer = self.player.current_session.answers[self.current_question_num]
            self.mark_button.setChecked(user_answer.is_marked)
        else:
            self.mark_button.setChecked(False)

    def complete_exam(self):
        """Complete the exam and show results."""
        result = self.player.end_session()

        # Show completion message
        score = result.get('score', 0)
        passed = result.get('passed', False)

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Exam Completed")
        status_icon = "✓" if passed else "✗"
        msg_box.setText(f"{status_icon} Exam completed!")
        msg_box.setInformativeText(
            f"Final Score: {score}%\n"
            f"Status: {'PASSED' if passed else 'FAILED'}\n"
            f"Session saved successfully."
        )
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()

        self.exam_completed.emit()

    def get_progress_info(self) -> dict:
        """Get current progress information."""
        return self.player.show_progress()

    def show_jump_dialog(self):
        """Show dialog to jump to a specific question."""
        from PyQt6.QtWidgets import QInputDialog
        
        total_questions = len(self.player.question_order)
        
        question_num, ok = QInputDialog.getInt(
            self,
            "Jump to Question",
            f"Enter question number (1-{total_questions}):",
            value=self.current_question_num,
            min=1,
            max=total_questions
        )
        
        if ok and question_num != self.current_question_num:
            self.jump_to_question(question_num)
