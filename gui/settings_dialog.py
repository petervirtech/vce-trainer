"""
Settings Dialog for VCE Exam Player GUI.
Allows users to configure exam preferences.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QCheckBox, QPushButton, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt


class SettingsDialog(QDialog):
    """Settings dialog for exam configuration."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.randomize_questions = True
        self.max_questions = 0  # 0 means all questions
        self.time_limit = 0  # 0 means no time limit

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Exam Settings")
        self.setModal(True)
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        # Exam Questions Settings
        questions_group = QGroupBox("Exam Questions")
        questions_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #FB8C00;
                border: 1px solid #9C8978;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }
        """)
        questions_layout = QFormLayout(questions_group)

        self.randomize_checkbox = QCheckBox("Randomize question order")
        self.randomize_checkbox.setChecked(self.randomize_questions)
        questions_layout.addRow(self.randomize_checkbox)

        self.max_questions_spin = QSpinBox()
        self.max_questions_spin.setRange(0, 500)
        self.max_questions_spin.setValue(self.max_questions)
        self.max_questions_spin.setSpecialValueText("All questions")
        questions_layout.addRow("Maximum questions:", self.max_questions_spin)

        layout.addWidget(questions_group)

        # Time Settings
        time_group = QGroupBox("Time Settings")
        time_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #FB8C00;
                border: 1px solid #9C8978;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }
        """)
        time_layout = QFormLayout(time_group)

        self.time_limit_spin = QSpinBox()
        self.time_limit_spin.setRange(0, 480)  # Up to 8 hours
        self.time_limit_spin.setValue(self.time_limit)
        self.time_limit_spin.setSpecialValueText("No time limit")
        self.time_limit_spin.setSuffix(" minutes")
        time_layout.addRow("Time limit:", self.time_limit_spin)

        layout.addWidget(time_group)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_button = QPushButton("✓ Save Settings")
        save_button.setStyleSheet("""
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
        """)
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("✕ Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def set_settings(self, randomize: bool, max_questions: int, time_limit: int):
        """Set current settings."""
        self.randomize_questions = randomize
        self.max_questions = max_questions
        self.time_limit = time_limit

        self.randomize_checkbox.setChecked(randomize)
        self.max_questions_spin.setValue(max_questions)
        self.time_limit_spin.setValue(time_limit)

    def get_settings(self):
        """Get current settings."""
        return {
            'randomize_questions': self.randomize_checkbox.isChecked(),
            'max_questions': self.max_questions_spin.value(),
            'time_limit': self.time_limit_spin.value()
        }
