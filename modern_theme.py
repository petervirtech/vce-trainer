"""
Modern Theme for VCE Exam Player - Contemporary UI Design
Qt-compatible modern styling with clean design and professional appearance.
"""

from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtWidgets import QApplication


def apply_modern_theme(app: QApplication):
    """Apply modern, contemporary theme to the application."""
    
    # Set modern font stack - prioritize system fonts by platform
    import platform
    from PyQt6.QtGui import QFontDatabase
    
    system = platform.system()
    font = None
    
    # Get available font families for better matching
    available_families = QFontDatabase.families()
    
    def find_font(font_names):
        """Find the first available font from a list."""
        for font_name in font_names:
            if font_name in available_families:
                test_font = QFont(font_name, 13)
                if test_font.exactMatch() or font_name in available_families:
                    return test_font
        return None
    
    if system == "Darwin":  # macOS
        # Try macOS system fonts in order of preference
        font = find_font(["Helvetica Neue", "SF Pro Text", "SF Pro Display", "Helvetica", "Lucida Grande"])
    elif system == "Windows":  # Windows
        # Try Windows system fonts in order of preference
        font = find_font(["Segoe UI", "Segoe UI Variable", "Tahoma", "Microsoft Sans Serif"])
    elif system == "Linux":  # Linux
        # Try Linux system fonts in order of preference
        font = find_font(["Ubuntu", "Noto Sans", "DejaVu Sans", "Liberation Sans", "Cantarell"])
    
    # Universal fallback if no system font found
    if not font:
        font = find_font(["Arial", "Liberation Sans", "DejaVu Sans"])
    
    # Final fallback - use Qt's default system font
    if not font:
        font = QFont()  # Use Qt's default font
        font.setPointSize(13)
    
    # Ensure we have a valid font size
    if font.pointSize() <= 0:
        font.setPointSize(13)
    
    app.setFont(font)
    
    # Modern color palette - Dark theme with blue accent
    palette = QPalette()
    
    # Background colors - Modern dark theme
    palette.setColor(QPalette.ColorRole.Window, QColor(16, 16, 20))          # #101014 - Very dark blue-gray
    palette.setColor(QPalette.ColorRole.WindowText, QColor(248, 250, 252))   # #F8FAFC - Almost white
    
    # Surface colors
    palette.setColor(QPalette.ColorRole.Base, QColor(24, 24, 27))            # #18181B - Dark surface
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(39, 39, 42))   # #27272A - Lighter surface
    
    # Text colors
    palette.setColor(QPalette.ColorRole.Text, QColor(248, 250, 252))         # #F8FAFC - Primary text
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))   # #FFFFFF - Bright text
    
    # Button colors
    palette.setColor(QPalette.ColorRole.Button, QColor(39, 39, 42))          # #27272A - Button background
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(248, 250, 252))   # #F8FAFC - Button text
    
    # Accent colors - Modern blue
    palette.setColor(QPalette.ColorRole.Highlight, QColor(59, 130, 246))     # #3B82F6 - Blue accent
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    
    # Link colors
    palette.setColor(QPalette.ColorRole.Link, QColor(96, 165, 250))          # #60A5FA - Light blue
    
    app.setPalette(palette)
    
    # Modern stylesheet with glassmorphism and contemporary design
    modern_stylesheet = """
    /* Modern VCE Exam Player Theme */
    
    /* Main Window */
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #101014, stop:1 #18181B);
    }
    
    /* Buttons - Modern with subtle shadows and hover effects */
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #3B82F6, stop:1 #2563EB);
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 14px;
        color: white;
        min-height: 20px;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #60A5FA, stop:1 #3B82F6);
    }
    
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #2563EB, stop:1 #1D4ED8);
    }
    
    QPushButton:disabled {
        background: #374151;
        color: #9CA3AF;
    }
    
    /* Secondary buttons */
    QPushButton[class="secondary"] {
        background: rgba(55, 65, 81, 0.8);
        border: 1px solid #4B5563;
        color: #F3F4F6;
    }
    
    QPushButton[class="secondary"]:hover {
        background: rgba(75, 85, 99, 0.9);
        border: 1px solid #6B7280;
    }
    
    /* Text inputs with modern glassmorphism */
    QTextEdit, QLineEdit, QSpinBox, QComboBox {
        background: rgba(39, 39, 42, 0.7);
        border: 1px solid rgba(75, 85, 99, 0.3);
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 14px;
        color: #F8FAFC;
    }
    
    QTextEdit:focus, QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
        border: 2px solid #3B82F6;
        background: rgba(39, 39, 42, 0.9);
        outline: none;
    }
    
    QTextEdit:hover, QLineEdit:hover, QSpinBox:hover, QComboBox:hover {
        border: 1px solid rgba(96, 165, 250, 0.5);
    }
    
    /* Cards and containers */
    QFrame {
        background: rgba(24, 24, 27, 0.8);
        border: 1px solid rgba(39, 39, 42, 0.5);
        border-radius: 16px;
    }
    
    QFrame[class="card"] {
        background: rgba(24, 24, 27, 0.9);
        border: 1px solid rgba(63, 63, 70, 0.3);
        border-radius: 20px;
        padding: 24px;
    }
    
    /* Group boxes with modern styling */
    QGroupBox {
        font-size: 16px;
        font-weight: 600;
        color: #F3F4F6;
        border: 1px solid rgba(75, 85, 99, 0.3);
        border-radius: 16px;
        margin-top: 16px;
        padding-top: 16px;
        background: rgba(24, 24, 27, 0.5);
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 20px;
        padding: 0 12px;
        background: rgba(16, 16, 20, 0.9);
        border-radius: 8px;
    }
    
    /* Modern checkboxes and radio buttons */
    QCheckBox, QRadioButton {
        spacing: 12px;
        font-size: 14px;
        color: #F3F4F6;
    }
    
    QCheckBox::indicator, QRadioButton::indicator {
        width: 20px;
        height: 20px;
        border: 2px solid #4B5563;
        border-radius: 6px;
        background: rgba(24, 24, 27, 0.8);
    }
    
    QCheckBox::indicator:checked, QRadioButton::indicator:checked {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #3B82F6, stop:1 #1D4ED8);
        border: 2px solid #3B82F6;
    }
    
    QCheckBox::indicator:hover, QRadioButton::indicator:hover {
        border: 2px solid #60A5FA;
    }
    
    QRadioButton::indicator {
        border-radius: 10px;
    }
    
    /* Modern scrollbars */
    QScrollBar:vertical {
        background: rgba(24, 24, 27, 0.5);
        width: 12px;
        border-radius: 6px;
        margin: 0;
    }
    
    QScrollBar::handle:vertical {
        background: rgba(75, 85, 99, 0.8);
        border-radius: 6px;
        min-height: 30px;
        margin: 2px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: rgba(107, 114, 128, 0.9);
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    
    QScrollBar:horizontal {
        background: rgba(24, 24, 27, 0.5);
        height: 12px;
        border-radius: 6px;
        margin: 0;
    }
    
    QScrollBar::handle:horizontal {
        background: rgba(75, 85, 99, 0.8);
        border-radius: 6px;
        min-width: 30px;
        margin: 2px;
    }
    
    /* Progress bars with modern gradient */
    QProgressBar {
        border: none;
        border-radius: 8px;
        text-align: center;
        background: rgba(39, 39, 42, 0.8);
        color: #F3F4F6;
        font-weight: 600;
        height: 16px;
    }
    
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #3B82F6, stop:0.5 #60A5FA, stop:1 #93C5FD);
        border-radius: 8px;
    }
    
    /* Lists with modern styling */
    QListWidget {
        background: rgba(24, 24, 27, 0.8);
        border: 1px solid rgba(63, 63, 70, 0.3);
        border-radius: 12px;
        outline: none;
        padding: 8px;
    }
    
    QListWidget::item {
        background: rgba(39, 39, 42, 0.6);
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 2px 0;
        color: #F3F4F6;
    }
    
    QListWidget::item:selected {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #3B82F6, stop:1 #2563EB);
        color: white;
    }
    
    QListWidget::item:hover {
        background: rgba(59, 130, 246, 0.2);
    }
    
    /* Tabs with modern design */
    QTabWidget::pane {
        border: 1px solid rgba(63, 63, 70, 0.3);
        border-radius: 12px;
        background: rgba(24, 24, 27, 0.8);
        top: -1px;
    }
    
    QTabBar::tab {
        background: rgba(39, 39, 42, 0.6);
        color: #9CA3AF;
        padding: 12px 24px;
        margin-right: 4px;
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
        font-weight: 500;
    }
    
    QTabBar::tab:selected {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #3B82F6, stop:1 #2563EB);
        color: white;
    }
    
    QTabBar::tab:hover:!selected {
        background: rgba(59, 130, 246, 0.2);
        color: #F3F4F6;
    }
    
    /* Menu bar and menus */
    QMenuBar {
        background: rgba(16, 16, 20, 0.95);
        color: #F3F4F6;
        border: none;
        padding: 4px;
    }
    
    QMenuBar::item {
        background: transparent;
        padding: 8px 16px;
        border-radius: 8px;
    }
    
    QMenuBar::item:selected {
        background: rgba(59, 130, 246, 0.2);
    }
    
    QMenu {
        background: rgba(24, 24, 27, 0.95);
        border: 1px solid rgba(63, 63, 70, 0.5);
        border-radius: 12px;
        padding: 8px;
    }
    
    QMenu::item {
        padding: 10px 20px;
        border-radius: 8px;
        color: #F3F4F6;
    }
    
    QMenu::item:selected {
        background: rgba(59, 130, 246, 0.2);
    }
    
    /* Status bar */
    QStatusBar {
        background: rgba(16, 16, 20, 0.9);
        color: #9CA3AF;
        border-top: 1px solid rgba(63, 63, 70, 0.3);
    }
    
    /* Labels with modern typography */
    QLabel {
        color: #F3F4F6;
    }
    
    QLabel[class="title"] {
        font-size: 28px;
        font-weight: 700;
        color: #F8FAFC;
    }
    
    QLabel[class="subtitle"] {
        font-size: 18px;
        font-weight: 600;
        color: #E5E7EB;
    }
    
    QLabel[class="caption"] {
        font-size: 12px;
        color: #9CA3AF;
    }
    
    QLabel[class="accent"] {
        color: #60A5FA;
        font-weight: 600;
    }
    
    /* Dialogs */
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #101014, stop:1 #18181B);
        border-radius: 16px;
    }
    
    /* Tooltips */
    QToolTip {
        background: rgba(24, 24, 27, 0.95);
        color: #F3F4F6;
        border: 1px solid rgba(63, 63, 70, 0.5);
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 12px;
    }
    """
    
    app.setStyleSheet(modern_stylesheet)


def get_accent_color() -> str:
    """Get the primary accent color for the theme."""
    return "#3B82F6"


def get_success_color() -> str:
    """Get the success color."""
    return "#10B981"


def get_warning_color() -> str:
    """Get the warning color."""
    return "#F59E0B"


def get_error_color() -> str:
    """Get the error color."""
    return "#EF4444"