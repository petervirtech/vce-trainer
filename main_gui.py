#!/usr/bin/env python3
"""
VCE Exam Player - GUI Application
Main entry point for the graphical user interface version.
"""

import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor

from gui.main_window import MainWindow
from modern_theme import apply_modern_theme


def setup_application_style(app: QApplication):
    """Configure the application theme and styling."""
    # Set application-wide font for better readability
    font = QFont("Arial", 14)  # Modern, readable font at larger size
    app.setFont(font)

    # Set Fusion style for modern cross-platform appearance
    app.setStyle("Fusion")

    # Create Material Design 3 dark theme palette
    palette = QPalette()

    # Material Design 3 dark orange theme colors
    # Primary: #FB8C00 (orange)
    # Background: #1F1B16
    # Surface: #15120E
    # On Surface: #EAE1D9
    # Surface Variant: #51453A
    # On Surface Variant: #D5C4B5
    # Outline: #9C8978

    # Window colors - background
    palette.setColor(QPalette.ColorRole.Window, QColor(31, 27, 22))  # #1F1B16
    palette.setColor(QPalette.ColorRole.WindowText, QColor(234, 225, 217))  # #EAE1D9

    # Base colors (for input fields, etc.) - surface
    palette.setColor(QPalette.ColorRole.Base, QColor(21, 18, 14))  # #15120E
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(81, 69, 58))  # #51453A

    # Text colors
    palette.setColor(QPalette.ColorRole.Text, QColor(234, 225, 217))  # #EAE1D9
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))

    # Button colors - surface variant
    palette.setColor(QPalette.ColorRole.Button, QColor(81, 69, 58))  # #51453A
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(234, 225, 217))  # #EAE1D9

    # Highlight colors (for selections) - primary
    palette.setColor(QPalette.ColorRole.Highlight, QColor(251, 140, 0))  # #FB8C00
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

    # Link colors - primary
    palette.setColor(QPalette.ColorRole.Link, QColor(251, 140, 0))  # #FB8C00

    app.setPalette(palette)

    # Apply Material Design 3 orange stylesheet
    md3_stylesheet = """
    /* Material Design 3 orange theme styling */

    /* Buttons */
    QPushButton {
        border-radius: 20px;  /* MD3 full rounded */
        padding: 12px 24px;
        font-weight: 500;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: rgba(251, 140, 0, 0.08);
    }

    QPushButton:pressed {
        background-color: rgba(251, 140, 0, 0.12);
    }

    /* Text Edit fields */
    QTextEdit, QLineEdit, QSpinBox, QComboBox {
        border: 1px solid #9C8978;
        border-radius: 4px;
        padding: 8px 12px;
        background-color: #15120E;
        color: #EAE1D9;
    }

    QTextEdit:focus, QLineEdit:focus {
        border: 2px solid #FB8C00;
        border-radius: 4px;
    }

    /* Group boxes */
    QGroupBox {
        font-size: 14px;
        font-weight: 500;
        border: 1px solid #9C8978;
        border-radius: 12px;
        margin-top: 12px;
        padding-top: 12px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 8px;
        color: #D5C4B5;
    }

    /* Checkboxes and Radio buttons */
    QCheckBox, QRadioButton {
        spacing: 8px;
        font-size: 14px;
    }

    QCheckBox::indicator, QRadioButton::indicator {
        width: 20px;
        height: 20px;
        border-radius: 2px;
        border: 2px solid #9C8978;
        background-color: #15120E;
    }

    QCheckBox::indicator:checked, QRadioButton::indicator:checked {
        background-color: #FB8C00;
        border: 2px solid #FB8C00;
    }

    QRadioButton::indicator {
        border-radius: 10px;
    }

    QRadioButton::indicator:checked {
        border-radius: 10px;
    }

    /* Scroll bars */
    QScrollBar:vertical {
        background: #1F1B16;
        width: 12px;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical {
        background: #9C8978;
        border-radius: 6px;
        min-height: 30px;
    }

    QScrollBar::handle:vertical:hover {
        background: #D5C4B5;
    }

    /* Progress bar */
    QProgressBar {
        border: none;
        border-radius: 4px;
        text-align: center;
        background-color: #51453A;
    }

    QProgressBar::chunk {
        background-color: #FB8C00;
        border-radius: 4px;
    }
    """

    app.setStyleSheet(md3_stylesheet)


def main():
    """Main application entry point."""
    try:
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("VCE Exam Player")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("VCE Trainer")

        # Configure high DPI scaling (PyQt6 compatible)
        try:
            app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
            app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        except AttributeError:
            # Fallback for older PyQt6 versions
            pass

        # Apply modern theme
        apply_modern_theme(app)

        # Create and show main window
        window = MainWindow()
        window.show()

        # Start event loop
        return app.exec()

    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
