"""
Results Viewer Widget for VCE Exam Player GUI.
Displays exam results and provides detailed review functionality.
"""

from typing import Dict, List, Optional, cast

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QTextEdit, QPushButton, QFrame, QScrollArea,
    QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from exam_player import ExamPlayer, ExamSession


class ResultsViewerWidget(QWidget):
    """Widget for viewing exam results and reviewing questions."""

    # Signals
    back_to_main = pyqtSignal()
    review_completed = pyqtSignal()

    def __init__(self, exam_player: ExamPlayer):
        super().__init__()
        self.player = exam_player
        self.current_question_idx = 0

        # Ensure we have a session
        if not self.player.current_session:
            raise ValueError("No active exam session to review")

        self.session = cast(ExamSession, self.player.current_session)

        # Calculate final score if not already done
        if not self.session.score:
            self.player.calculate_score()

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)

        # Overall results header
        self.setup_results_header(layout)

        # Main content splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)

        # Question list panel
        self.setup_question_list(splitter)

        # Question detail panel
        self.setup_question_detail(splitter)

        # Navigation buttons
        self.setup_navigation(layout)

        # Load initial data
        self.load_results()
        if self.player.exam.questions:
            self.show_question_detail(0)

    def setup_results_header(self, parent_layout: QVBoxLayout):
        """Set up the results header with overall statistics."""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.Box)
        header_layout = QVBoxLayout(header_frame)

        # Title
        title = QLabel("Exam Results & Review")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #FB8C00; margin-bottom: 15px;")
        header_layout.addWidget(title)

        # Results summary
        self.results_summary = QLabel()
        self.results_summary.setStyleSheet("font-size: 16px; color: #E6E1E5; margin-bottom: 15px;")
        header_layout.addWidget(self.results_summary)

        parent_layout.addWidget(header_frame)

    def setup_question_list(self, splitter: QSplitter):
        """Set up the question list panel."""
        list_frame = QFrame()
        list_layout = QVBoxLayout(list_frame)

        # List header
        list_header = QLabel("Questions")
        list_header.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        list_layout.addWidget(list_header)

        # Question list with improved styling
        self.question_list = QListWidget()
        self.question_list.setStyleSheet("""
            QListWidget {
                background-color: rgba(24, 24, 27, 0.8);
                border: 1px solid rgba(75, 85, 99, 0.3);
                border-radius: 8px;
                outline: none;
                padding: 8px;
            }
            QListWidget::item {
                border: none;
                border-radius: 6px;
                padding: 10px 12px;
                margin: 2px 0;
                font-size: 13px;
                font-weight: 500;
            }
            QListWidget::item:selected {
                background-color: rgba(59, 130, 246, 0.3);
                border: 1px solid #3B82F6;
            }
            QListWidget::item:hover {
                background-color: rgba(75, 85, 99, 0.2);
            }
        """)
        self.question_list.itemClicked.connect(self.on_question_selected)
        list_layout.addWidget(self.question_list)

        splitter.addWidget(list_frame)
        splitter.setSizes([250, 600])  # Increased detail panel size

    def setup_question_detail(self, splitter: QSplitter):
        """Set up the question detail panel."""
        detail_frame = QFrame()
        detail_layout = QVBoxLayout(detail_frame)
        detail_layout.setSpacing(8)  # Reduce spacing between elements

        # Question header
        self.question_header = QLabel()
        self.question_header.setStyleSheet("font-weight: bold; font-size: 16px; color: #FB8C00; margin-bottom: 15px;")
        detail_layout.addWidget(self.question_header)

        # Question text
        self.question_text = QTextEdit()
        self.question_text.setReadOnly(True)
        self.question_text.setMaximumHeight(120)
        self.question_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #9C8978;
                border-radius: 4px;
                padding: 10px;
                background-color: #15120E;
                color: #EAE1D9;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 2px solid #FB8C00;
            }
        """)
        detail_layout.addWidget(self.question_text)

        # Answers section
        answers_label = QLabel("Answers:")
        answers_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        detail_layout.addWidget(answers_label)

        # Answers display with rich text support
        self.answers_display = QTextEdit()
        self.answers_display.setReadOnly(True)
        self.answers_display.setAcceptRichText(True)  # Enable rich text for color formatting
        self.answers_display.setMinimumHeight(160)  # Ensure all 4 answers are visible
        self.answers_display.setMaximumHeight(180)  # Prevent excessive height
        self.answers_display.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)  # Enable word wrapping
        self.answers_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid rgba(75, 85, 99, 0.3);
                border-radius: 8px;
                padding: 8px;
                background-color: rgba(24, 24, 27, 0.8);
                color: #F3F4F6;
                font-size: 11px;
                font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
            }
            QTextEdit:focus {
                border: 2px solid #3B82F6;
            }
        """)
        detail_layout.addWidget(self.answers_display)

        # Explanation section (for incorrect answers)
        explanation_label = QLabel("Explanation:")
        explanation_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        detail_layout.addWidget(explanation_label)

        self.explanation_text = QTextEdit()
        self.explanation_text.setReadOnly(True)
        self.explanation_text.setPlainText("Explanations are not available in the current VCE file format.\n\nTo add explanations, the VCE parser would need to be extended to extract explanation data if present in the file, or explanations could be provided separately.")
        self.explanation_text.setMinimumHeight(200)  # Increased for better readability
        self.explanation_text.setMaximumHeight(300)  # Increased to avoid scrolling
        self.explanation_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #9C8978;
                border-radius: 4px;
                padding: 10px;
                background-color: #15120E;
                color: #EAE1D9;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 2px solid #FB8C00;
            }
        """)
        detail_layout.addWidget(self.explanation_text)

        splitter.addWidget(detail_frame)

    def setup_navigation(self, parent_layout: QVBoxLayout):
        """Set up navigation buttons."""
        nav_layout = QHBoxLayout()

        # Back to main button
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.back_to_main_menu)
        nav_layout.addWidget(back_button)

        nav_layout.addStretch()

        # Export results button
        export_button = QPushButton("Export Results")
        export_button.clicked.connect(self.export_results)
        nav_layout.addWidget(export_button)

        # Finish review button
        finish_button = QPushButton("Finish Review")
        finish_button.clicked.connect(self.finish_review)
        nav_layout.addWidget(finish_button)

        parent_layout.addLayout(nav_layout)

    def load_results(self):
        """Load and display overall exam results."""
        if not self.player.current_session:
            return

        # Calculate statistics
        total_questions = len(self.player.question_order)
        correct_answers = 0
        answered_questions = 0

        for display_num in range(1, total_questions + 1):
            if display_num in self.player.current_session.answers:
                answered_questions += 1
                user_answer = self.player.current_session.answers[display_num]
                if user_answer.is_correct:
                    correct_answers += 1

        score = self.player.current_session.score or 0
        passed = self.player.current_session.passed or False

        # Update summary
        summary_text = f"""
Exam: {self.player.exam.title}
Score: {score}% ({'PASSED' if passed else 'FAILED'})
Questions Answered: {answered_questions}/{total_questions}
Correct Answers: {correct_answers}/{answered_questions}
        """.strip()

        self.results_summary.setText(summary_text)

        # Load question list - only questions that were in the exam
        self.question_list.clear()
        for i, question_idx in enumerate(self.player.question_order):
            question = self.player.exam.questions[question_idx]
            display_num = i + 1
            
            # Determine status and styling
            status_text = "Not Answered"
            item_style = "background-color: rgba(75, 85, 99, 0.5); color: #9CA3AF;"  # Gray for unanswered
            
            if self.session.answers and display_num in self.session.answers:
                user_answer = self.session.answers[display_num]
                if user_answer.is_correct:
                    status_text = "✓ Correct"
                    item_style = "background-color: rgba(16, 185, 129, 0.2); color: #10B981; font-weight: 600;"  # Green
                else:
                    status_text = "✗ Incorrect"
                    item_style = "background-color: rgba(239, 68, 68, 0.2); color: #EF4444; font-weight: 600;"  # Red
            
            item = QListWidgetItem(f"Question {display_num} - {status_text}")
            
            # Apply styling using Qt's color system
            if self.session.answers and display_num in self.session.answers:
                user_answer = self.session.answers[display_num]
                if user_answer.is_correct:
                    item.setBackground(QColor(16, 185, 129, 50))  # Green with transparency
                    item.setForeground(QColor(16, 185, 129))  # Green text
                else:
                    item.setBackground(QColor(239, 68, 68, 50))  # Red with transparency
                    item.setForeground(QColor(239, 68, 68))  # Red text
            else:
                item.setBackground(QColor(75, 85, 99, 50))  # Gray
                item.setForeground(QColor(156, 163, 175))  # Gray text

            self.question_list.addItem(item)

    def on_question_selected(self, item: QListWidgetItem):
        """Handle question selection from the list."""
        row = self.question_list.row(item)
        self.show_question_detail(row)

    def show_question_detail(self, display_idx: int):
        """Show detailed view of a specific question."""
        if not (0 <= display_idx < len(self.player.question_order)):
            return

        self.current_question_idx = display_idx
        question_idx = self.player.question_order[display_idx]
        question = self.player.exam.questions[question_idx]

        # Update question header
        status = "Not Answered"
        display_num = display_idx + 1
        if self.session.answers and display_num in self.session.answers:
            user_answer = self.session.answers[display_num]
            status = "Correct" if user_answer.is_correct else "Incorrect"

        self.question_header.setText(f"Question {display_num} - {status}")

        # Question text
        self.question_text.setPlainText(question.question_text)

        # Answers display with rich formatting
        answers_html = self.format_answers_display_html(question, display_idx)
        self.answers_display.setHtml(answers_html)

        # Explanation
        if self.session.answers and display_num in self.session.answers:
            user_answer = self.session.answers[display_num]
            if not user_answer.is_correct:
                # Show question explanation if available
                if question.explanation:
                    # Check if it's a Perplexity link
                    if question.explanation.startswith("[Get AI explanation]"):
                        # Extract the URL from markdown link format
                        import re
                        url_match = re.search(r'\((https://[^)]+)\)', question.explanation)
                        if url_match:
                            url = url_match.group(1)
                            explanation_text = (
                                "The correct answer(s) are highlighted above in the list.\n\n"
                                "Explanation:\n"
                                f"{question.explanation}\n\n"
                                "Why this is correct:\n"
                                "• The highlighted answer(s) are the officially correct response(s) for this question\n"
                                "💡 Tip: Click the Perplexity link above to get AI-generated explanation with full context!"
                            )
                        else:
                            explanation_text = (
                              
                                "Explanation:\n"
                                f"{question.explanation}\n\n"
                                "Why this is correct:\n"
                                "• The highlighted answer(s) are the officially correct response(s) for this question\n"
                                "• Your selected answer(s) are marked with ✗"
                            )
                    else:
                        explanation_text = (
                           
                            "Explanation:\n"
                            f"{question.explanation}\n\n"
                            "Why this is correct:\n"
                            "• The highlighted answer(s) are the officially correct response(s) for this question\n"
                            "• Your selected answer(s) are marked with ✗"
                        )
                    self.explanation_text.setPlainText(explanation_text)
                else:
                    self.explanation_text.setPlainText(
                        "Why this is correct:\n"
                        "• The highlighted answer(s) are the officially correct response(s) for this question\n"
                        "• Your selected answer(s) are marked with ✗\n\n"
                        "Note: Detailed explanation not available for this question.\n"
                        "For learning purposes, you may want to:\n"
                        "• Research the topic in Microsoft documentation\n"
                        "• Review related exam objectives\n"
                        "• Consult study guides or training materials"
                    )
            else:
                # For correct answers, still show explanation if available
                if question.explanation:
                    if question.explanation.startswith("[Get AI explanation]"):
                        self.explanation_text.setPlainText(
                            "This question was answered correctly! ✅\n\n"
                            f"Explanation:\n{question.explanation}\n\n"
                            "💡 The Perplexity link provides additional learning context."
                        )
                    else:
                        self.explanation_text.setPlainText(
                            "This question was answered correctly! ✅\n\n"
                            f"Explanation:\n{question.explanation}"
                        )
                else:
                    self.explanation_text.setPlainText("This question was answered correctly!")
        else:
            self.explanation_text.setPlainText("This question was not answered.")

    def format_answers_display(self, question, display_idx: int) -> str:
        """Format the answers display with user's selection and correct answers."""
        lines = []

        display_num = display_idx + 1
        user_selected: List[int] = []
        if self.session.answers and display_num in self.session.answers:
            user_answer = self.session.answers[display_num]
            user_selected = user_answer.selected_answers

        for i, answer_text in enumerate(question.answers):
            prefix = chr(65 + i)  # A, B, C, D
            
            # Determine the status and formatting
            if i in question.correct_answers and i in user_selected:
                # User selected correct answer
                marker = "✓"
                status = "[CORRECT - Your Answer]"
                lines.append(f"{marker} {prefix}. {answer_text} {status}")
            elif i in question.correct_answers:
                # Correct answer not selected by user
                marker = "✓"
                status = "[CORRECT ANSWER]"
                lines.append(f"{marker} {prefix}. {answer_text} {status}")
            elif i in user_selected:
                # User selected incorrect answer
                marker = "✗"
                status = "[INCORRECT - Your Answer]"
                lines.append(f"{marker} {prefix}. {answer_text} {status}")
            else:
                # Not selected, not correct
                marker = "○"
                lines.append(f"{marker} {prefix}. {answer_text}")

        return "\n".join(lines)

    def format_answers_display_html(self, question, display_idx: int) -> str:
        """Format the answers display with HTML for rich color formatting."""
        lines = []
        
        display_num = display_idx + 1
        user_selected: List[int] = []
        if self.session.answers and display_num in self.session.answers:
            user_answer = self.session.answers[display_num]
            user_selected = user_answer.selected_answers

        # HTML styling
        correct_style = 'color: #10B981; font-weight: bold;'  # Green
        incorrect_style = 'color: #EF4444; font-weight: bold;'  # Red
        neutral_style = 'color: #9CA3AF;'  # Gray
        user_correct_style = 'color: #10B981; font-weight: bold; background-color: rgba(16, 185, 129, 0.1); border-radius: 4px;'
        user_incorrect_style = 'color: #EF4444; font-weight: bold; background-color: rgba(239, 68, 68, 0.1); border-radius: 4px;'

        for i, answer_text in enumerate(question.answers):
            prefix = chr(65 + i)  # A, B, C, D
            escaped_text = answer_text.replace('<', '&lt;').replace('>', '&gt;')  # Escape HTML
            
            # Determine the status and formatting
            if i in question.correct_answers and i in user_selected:
                # User selected correct answer - highlight in green
                lines.append(f'<div style="{user_correct_style}">✓ {prefix}. {escaped_text} <strong>[CORRECT - Your Answer]</strong></div>')
            elif i in question.correct_answers:
                # Correct answer not selected by user - show in green
                lines.append(f'<div style="{correct_style}">✓ {prefix}. {escaped_text} <strong>[CORRECT ANSWER]</strong></div>')
            elif i in user_selected:
                # User selected incorrect answer - highlight in red
                lines.append(f'<div style="{user_incorrect_style}">✗ {prefix}. {escaped_text} <strong>[INCORRECT - Your Answer]</strong></div>')
            else:
                # Not selected, not correct - neutral
                lines.append(f'<div style="{neutral_style}">○ {prefix}. {escaped_text}</div>')

        # Add CSS for better spacing and layout
        html_content = f"""
        <style>
        div {{
            margin: 1px 0;
            padding: 1px;
            line-height: 1.4;
            word-wrap: break-word;
        }}
        </style>
        {'<br>'.join(lines)}
        """
        return html_content

    def back_to_main_menu(self):
        """Return to the main menu."""
        reply = QMessageBox.question(
            self,
            'Back to Main Menu',
            'Are you sure you want to return to the main menu?\n'
            'The current session will remain available for review.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.back_to_main.emit()

    def finish_review(self):
        """Finish the review session."""
        QMessageBox.information(
            self,
            "Review Completed",
            "Review session completed.\n"
            "You can return to this session later for further review."
        )
        self.review_completed.emit()

    def export_results(self):
        """Export exam results to a file."""
        from PyQt6.QtWidgets import QFileDialog
        
        if not self.player.current_session:
            QMessageBox.warning(self, "No Session", "No session data to export.")
            return
        
        # Get export file path
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Results",
            f"exam_results_{self.player.current_session.session_id}.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                # Use session manager to export
                from gui.main_window import MainWindow
                main_window = self.parent()
                while main_window and not isinstance(main_window, MainWindow):
                    main_window = main_window.parent()
                
                if main_window and hasattr(main_window, 'session_manager'):
                    success = main_window.session_manager.export_session_summary(
                        self.player.current_session.session_id,
                        file_path
                    )
                    
                    if success:
                        QMessageBox.information(
                            self,
                            "Export Successful",
                            f"Results exported to:\\n{file_path}"
                        )
                    else:
                        QMessageBox.critical(
                            self,
                            "Export Failed",
                            "Failed to export results. Please try again."
                        )
                else:
                    QMessageBox.critical(
                        self,
                        "Export Error",
                        "Session manager not available for export."
                    )
                    
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Failed to export results:\\n{str(e)}"
                )
