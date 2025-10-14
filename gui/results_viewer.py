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

        # Question list
        self.question_list = QListWidget()
        self.question_list.itemClicked.connect(self.on_question_selected)
        list_layout.addWidget(self.question_list)

        splitter.addWidget(list_frame)
        splitter.setSizes([200, 400])  # Initial sizes

    def setup_question_detail(self, splitter: QSplitter):
        """Set up the question detail panel."""
        detail_frame = QFrame()
        detail_layout = QVBoxLayout(detail_frame)

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

        # Answers display
        self.answers_display = QTextEdit()
        self.answers_display.setReadOnly(True)
        self.answers_display.setStyleSheet("""
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
        detail_layout.addWidget(self.answers_display)

        # Explanation section (for incorrect answers)
        explanation_label = QLabel("Explanation:")
        explanation_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        detail_layout.addWidget(explanation_label)

        self.explanation_text = QTextEdit()
        self.explanation_text.setReadOnly(True)
        self.explanation_text.setPlainText("Explanations are not available in the current VCE file format.\n\nTo add explanations, the VCE parser would need to be extended to extract explanation data if present in the file, or explanations could be provided separately.")
        self.explanation_text.setMinimumHeight(150)
        self.explanation_text.setMaximumHeight(250)
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
            item = QListWidgetItem(f"Question {i+1}")

            # Set color based on correctness
            if self.session.answers and (i+1) in self.session.answers:  # i+1 is display number
                user_answer = self.session.answers[i+1]
                if user_answer.is_correct:
                    item.setBackground(QColor(0, 100, 0))  # Dark green for dark theme
                else:
                    item.setBackground(QColor(100, 0, 0))  # Dark red
            else:
                item.setBackground(QColor(50, 50, 50))  # Dark gray

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

        # Answers display
        answers_text = self.format_answers_display(question, question_idx)
        self.answers_display.setPlainText(answers_text)

        # Explanation
        if self.session.answers and question.id in self.session.answers:
            user_answer = self.session.answers[question.id]
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
                                "• Your selected answer(s) are marked with ✗\n\n"
                                "💡 Tip: Click the Perplexity link above to get AI-generated explanation with full context!"
                            )
                        else:
                            explanation_text = (
                                "The correct answer(s) are highlighted above in the list.\n\n"
                                "Explanation:\n"
                                f"{question.explanation}\n\n"
                                "Why this is correct:\n"
                                "• The highlighted answer(s) are the officially correct response(s) for this question\n"
                                "• Your selected answer(s) are marked with ✗"
                            )
                    else:
                        explanation_text = (
                            "The correct answer(s) are highlighted above in the list.\n\n"
                            "Explanation:\n"
                            f"{question.explanation}\n\n"
                            "Why this is correct:\n"
                            "• The highlighted answer(s) are the officially correct response(s) for this question\n"
                            "• Your selected answer(s) are marked with ✗"
                        )
                    self.explanation_text.setPlainText(explanation_text)
                else:
                    self.explanation_text.setPlainText(
                        "The correct answer(s) are highlighted above in the list.\n\n"
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
            marker = "□"  # Unchecked

            # Mark correct answers
            if i in question.correct_answers:
                marker = "✓"  # Correct
            elif i in user_selected:
                marker = "✗"  # User's incorrect choice

            lines.append(f"{marker} {chr(65 + i)}. {answer_text}")

        return "\n".join(lines)

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
