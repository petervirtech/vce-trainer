#!/usr/bin/env python3
"""
Simple test application to verify PyQt6 installation and basic functionality.
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Window properties
        self.setWindowTitle('VCE Exam Player - GUI Test')
        self.setGeometry(300, 300, 400, 200)

        # Layout
        layout = QVBoxLayout()

        # Title label
        title = QLabel('VCE Exam Player GUI')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet('font-size: 18px; font-weight: bold; color: #0078D4;')
        layout.addWidget(title)

        # Status label
        status = QLabel('PyQt6 is working correctly!')
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status.setStyleSheet('font-size: 14px; color: #107C10;')
        layout.addWidget(status)

        # Test button
        button = QPushButton('Click to test interaction')
        button.clicked.connect(self.on_button_click)
        button.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
            QPushButton:pressed {
                background-color: #005A9E;
            }
        """)
        layout.addWidget(button)

        # Result label
        self.result_label = QLabel('')
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet('font-size: 12px; color: #666;')
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def on_button_click(self):
        self.result_label.setText('Button clicked! GUI interaction working.')


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern cross-platform style

    window = TestWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
