"""
Session Selection Dialog for VCE Exam Player GUI.
Allows users to select from available sessions for resume or review.
"""

from typing import List, Dict, Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QTextEdit, QSplitter
)
from PyQt6.QtCore import Qt
from datetime import datetime


class SessionSelectionDialog(QDialog):
    """Dialog for selecting a session to resume or review."""
    
    def __init__(self, sessions: List[Dict], title: str, parent=None):
        super().__init__(parent)
        self.sessions = sessions
        self.selected_session = None
        
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(800, 500)
        
        self.setup_ui()
        self.populate_sessions()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Header
        header_label = QLabel("Select a session:")
        header_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #FB8C00;
            margin-bottom: 10px;
        """)
        layout.addWidget(header_label)
        
        # Main content with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Session list
        self.session_list = QListWidget()
        self.session_list.setMinimumWidth(300)
        self.session_list.itemSelectionChanged.connect(self.on_session_selected)
        self.session_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #9C8978;
                border-radius: 4px;
                background-color: #15120E;
                color: #EAE1D9;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #51453A;
            }
            QListWidget::item:selected {
                background-color: #FB8C00;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #6B5B4F;
            }
        """)
        splitter.addWidget(self.session_list)
        
        # Session details
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMinimumWidth(400)
        self.details_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #9C8978;
                border-radius: 4px;
                background-color: #15120E;
                color: #EAE1D9;
                font-size: 14px;
                padding: 10px;
            }
        """)
        splitter.addWidget(self.details_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.select_button = QPushButton("Select")
        self.select_button.setEnabled(False)
        self.select_button.clicked.connect(self.accept)
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #FB8C00;
                color: white;
                border: none;
                padding: 10px 24px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #FC9D26;
            }
            QPushButton:disabled {
                background-color: #51453A;
                color: #9C8978;
            }
        """)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #51453A;
                color: #D5C4B5;
                border: 1px solid #9C8978;
                padding: 10px 24px;
                border-radius: 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6B5B4F;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.select_button)
        
        layout.addLayout(button_layout)
    
    def populate_sessions(self):
        """Populate the session list."""
        for session in self.sessions:
            # Format session display text
            session_id = session.get('session_id', 'Unknown')
            exam_title = session.get('exam_title', 'Unknown Exam')
            start_time = session.get('start_time', '')
            status = session.get('status', 'unknown')
            score = session.get('score')
            
            # Format date
            try:
                if start_time:
                    dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    date_str = dt.strftime('%Y-%m-%d %H:%M')
                else:
                    date_str = 'Unknown Date'
            except:
                date_str = 'Unknown Date'
            
            # Create display text
            if status == 'completed' and score is not None:
                display_text = f"{exam_title[:40]}...\n{date_str} - Score: {score}%"
            else:
                display_text = f"{exam_title[:40]}...\n{date_str} - {status.title()}"
            
            # Create list item
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, session)
            
            # Color code by status
            if status == 'completed':
                if score and score >= 70:
                    item.setBackground(Qt.GlobalColor.darkGreen)
                else:
                    item.setBackground(Qt.GlobalColor.darkRed)
            else:
                item.setBackground(Qt.GlobalColor.darkBlue)
            
            self.session_list.addItem(item)
    
    def on_session_selected(self):
        """Handle session selection."""
        current_item = self.session_list.currentItem()
        if current_item:
            session = current_item.data(Qt.ItemDataRole.UserRole)
            self.selected_session = session
            self.select_button.setEnabled(True)
            
            # Show session details
            self.show_session_details(session)
        else:
            self.selected_session = None
            self.select_button.setEnabled(False)
            self.details_text.clear()
    
    def show_session_details(self, session: Dict):
        """Show detailed information about the selected session."""
        details = []
        
        # Basic info
        details.append(f"Session ID: {session.get('session_id', 'Unknown')}")
        details.append(f"Exam: {session.get('exam_title', 'Unknown')}")
        details.append(f"Status: {session.get('status', 'unknown').title()}")
        
        # Timing info
        start_time = session.get('start_time', '')
        if start_time:
            try:
                dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                details.append(f"Started: {dt.strftime('%Y-%m-%d at %H:%M:%S')}")
            except:
                details.append(f"Started: {start_time}")
        
        # Progress info
        total_questions = session.get('total_questions', 0)
        if total_questions:
            details.append(f"Total Questions: {total_questions}")
        
        # Score info (for completed sessions)
        if session.get('status') == 'completed':
            score = session.get('score')
            if score is not None:
                passed = session.get('passed', False)
                status_text = "PASSED" if passed else "FAILED"
                details.append(f"Final Score: {score}% ({status_text})")
            
            # Time spent
            total_time = session.get('total_time_spent', 0)
            if total_time:
                minutes = total_time // 60
                seconds = total_time % 60
                details.append(f"Time Spent: {minutes}:{seconds:02d}")
        
        # File info
        file_path = session.get('file_path', '')
        if file_path:
            details.append(f"File: {file_path}")
        
        # Join details
        details_text = "\\n".join(details)
        
        # Add instructions based on status
        if session.get('status') == 'in_progress':
            details_text += "\\n\\nThis session can be resumed to continue where you left off."
        elif session.get('status') == 'completed':
            details_text += "\\n\\nThis completed session can be reviewed to see your answers and explanations."
        
        self.details_text.setPlainText(details_text)
    
    def get_selected_session(self) -> Optional[Dict]:
        """Get the selected session."""
        return self.selected_session