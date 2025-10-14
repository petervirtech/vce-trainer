"""
Question Overview Widget - Grid view of all questions with status indicators.
"""

from typing import Dict, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPalette

from exam_player import ExamPlayer


class QuestionButton(QPushButton):
    """Individual question button with status indication."""
    
    def __init__(self, question_num: int, parent=None):
        super().__init__(str(question_num), parent)
        self.question_num = question_num
        self.setFixedSize(40, 40)
        self.setCheckable(False)
        self.update_status("unanswered")
    
    def update_status(self, status: str):
        """Update button appearance based on status."""
        styles = {
            "unanswered": """
                QPushButton {
                    background-color: #51453A;
                    color: #D5C4B5;
                    border: 1px solid #9C8978;
                    border-radius: 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #6B5B4F;
                }
            """,
            "answered": """
                QPushButton {
                    background-color: #2E7D32;
                    color: white;
                    border: 1px solid #4CAF50;
                    border-radius: 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #388E3C;
                }
            """,
            "marked": """
                QPushButton {
                    background-color: #F57C00;
                    color: white;
                    border: 1px solid #FF9800;
                    border-radius: 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #FB8C00;
                }
            """,
            "current": """
                QPushButton {
                    background-color: #FB8C00;
                    color: white;
                    border: 2px solid #FFB74D;
                    border-radius: 20px;
                    font-weight: bold;
                }
            """,
            "correct": """
                QPushButton {
                    background-color: #2E7D32;
                    color: white;
                    border: 2px solid #4CAF50;
                    border-radius: 20px;
                    font-weight: bold;
                }
            """,
            "incorrect": """
                QPushButton {
                    background-color: #C62828;
                    color: white;
                    border: 2px solid #F44336;
                    border-radius: 20px;
                    font-weight: bold;
                }
            """
        }
        
        self.setStyleSheet(styles.get(status, styles["unanswered"]))


class QuestionOverviewWidget(QWidget):
    """Grid view of all questions with status indicators."""
    
    # Signals
    question_selected = pyqtSignal(int)  # question number
    
    def __init__(self, exam_player: ExamPlayer, parent=None):
        super().__init__(parent)
        self.player = exam_player
        self.question_buttons: Dict[int, QuestionButton] = {}
        self.current_question = 1
        
        self.setup_ui()
        self.update_all_statuses()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Question Overview")
        header.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #FB8C00;
            margin-bottom: 15px;
        """)
        layout.addWidget(header)
        
        # Legend
        legend_layout = QHBoxLayout()
        
        legend_items = [
            ("Unanswered", "#51453A"),
            ("Answered", "#2E7D32"),
            ("Marked", "#F57C00"),
            ("Current", "#FB8C00")
        ]
        
        for label_text, color in legend_items:
            legend_item = QFrame()
            legend_item.setFixedSize(15, 15)
            legend_item.setStyleSheet(f"""
                background-color: {color};
                border: 1px solid #9C8978;
                border-radius: 7px;
            """)
            
            label = QLabel(label_text)
            label.setStyleSheet("color: #D5C4B5; font-size: 12px; margin-left: 5px;")
            
            item_layout = QHBoxLayout()
            item_layout.addWidget(legend_item)
            item_layout.addWidget(label)
            item_layout.addStretch()
            
            legend_layout.addLayout(item_layout)
        
        legend_layout.addStretch()
        layout.addLayout(legend_layout)
        
        # Scroll area for question grid
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        self.grid_layout = QGridLayout(scroll_widget)
        
        # Create question buttons
        total_questions = len(self.player.question_order)
        cols = 10  # 10 questions per row
        
        for i in range(total_questions):
            question_num = i + 1
            button = QuestionButton(question_num)
            button.clicked.connect(lambda checked, num=question_num: self.on_question_clicked(num))
            
            row = i // cols
            col = i % cols
            self.grid_layout.addWidget(button, row, col)
            self.question_buttons[question_num] = button
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(200)
        layout.addWidget(scroll_area)
        
        # Statistics
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("""
            color: #D5C4B5;
            font-size: 14px;
            margin-top: 10px;
            padding: 10px;
            background-color: #1F1B16;
            border-radius: 8px;
        """)
        layout.addWidget(self.stats_label)
        
        self.update_statistics()
    
    def on_question_clicked(self, question_num: int):
        """Handle question button click."""
        self.question_selected.emit(question_num)
    
    def set_current_question(self, question_num: int):
        """Update which question is currently active."""
        # Reset previous current question
        if self.current_question in self.question_buttons:
            self.update_question_status(self.current_question)
        
        # Set new current question
        self.current_question = question_num
        if question_num in self.question_buttons:
            self.question_buttons[question_num].update_status("current")
    
    def update_question_status(self, question_num: int):
        """Update the status of a specific question."""
        if question_num not in self.question_buttons:
            return
        
        button = self.question_buttons[question_num]
        
        # Determine status based on exam state
        if (self.player.current_session and 
            self.player.current_session.answers and 
            question_num in self.player.current_session.answers):
            
            user_answer = self.player.current_session.answers[question_num]
            
            if user_answer.is_marked:
                status = "marked"
            elif user_answer.is_correct is not None:
                # In review mode
                status = "correct" if user_answer.is_correct else "incorrect"
            else:
                status = "answered"
        else:
            status = "unanswered"
        
        button.update_status(status)
    
    def update_all_statuses(self):
        """Update status for all question buttons."""
        for question_num in self.question_buttons:
            if question_num != self.current_question:
                self.update_question_status(question_num)
        
        self.update_statistics()
    
    def update_statistics(self):
        """Update the statistics display."""
        if not self.player.current_session:
            return
        
        total = len(self.player.question_order)
        answered = 0
        marked = 0
        
        if self.player.current_session.answers:
            for question_num in range(1, total + 1):
                if question_num in self.player.current_session.answers:
                    answered += 1
                    user_answer = self.player.current_session.answers[question_num]
                    if user_answer.is_marked:
                        marked += 1
        
        unanswered = total - answered
        percentage = (answered / total * 100) if total > 0 else 0
        
        stats_text = f"""
Progress: {answered}/{total} questions answered ({percentage:.1f}%)
Marked for review: {marked}
Remaining: {unanswered}
        """.strip()
        
        self.stats_label.setText(stats_text)