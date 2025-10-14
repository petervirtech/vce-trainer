"""
Timer Widget - Countdown timer with visual progress for exam time limits.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont


class TimerWidget(QWidget):
    """Countdown timer widget with visual progress indication."""
    
    # Signals
    time_warning = pyqtSignal(int)  # minutes remaining
    time_expired = pyqtSignal()
    
    def __init__(self, time_limit_minutes: int = 0, parent=None):
        super().__init__(parent)
        self.time_limit_minutes = time_limit_minutes
        self.time_remaining_seconds = time_limit_minutes * 60
        self.total_seconds = self.time_remaining_seconds
        self.is_running = False
        
        # Timer object
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        
        self.setup_ui()
        self.update_display()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Timer label
        self.time_label = QLabel("No Time Limit")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #FB8C00;
                background-color: #1F1B16;
                border: 1px solid #9C8978;
                border-radius: 8px;
                padding: 8px;
                min-width: 120px;
            }
        """)
        layout.addWidget(self.time_label)
        
        # Progress bar (only show if time limit is set)
        if self.time_limit_minutes > 0:
            self.progress_bar = QProgressBar()
            self.progress_bar.setMaximum(self.total_seconds)
            self.progress_bar.setValue(self.time_remaining_seconds)
            self.progress_bar.setTextVisible(False)
            self.progress_bar.setMaximumHeight(8)
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 4px;
                    background-color: #51453A;
                }
                QProgressBar::chunk {
                    background-color: #FB8C00;
                    border-radius: 4px;
                }
            """)
            layout.addWidget(self.progress_bar)
        else:
            self.progress_bar = None
    
    def start_timer(self):
        """Start the countdown timer."""
        if self.time_limit_minutes > 0:
            self.is_running = True
            self.timer.start(1000)  # Update every second
    
    def pause_timer(self):
        """Pause the countdown timer."""
        self.is_running = False
        self.timer.stop()
    
    def resume_timer(self):
        """Resume the countdown timer."""
        if self.time_limit_minutes > 0 and self.time_remaining_seconds > 0:
            self.is_running = True
            self.timer.start(1000)
    
    def stop_timer(self):
        """Stop and reset the timer."""
        self.is_running = False
        self.timer.stop()
        self.time_remaining_seconds = self.total_seconds
        self.update_display()
    
    def update_timer(self):
        """Update the timer countdown."""
        if not self.is_running or self.time_remaining_seconds <= 0:
            return
        
        self.time_remaining_seconds -= 1
        self.update_display()
        
        # Check for warnings
        minutes_remaining = self.time_remaining_seconds // 60
        
        # Emit warnings at specific intervals
        if minutes_remaining in [30, 15, 10, 5, 1] and self.time_remaining_seconds % 60 == 0:
            self.time_warning.emit(minutes_remaining)
        
        # Check if time expired
        if self.time_remaining_seconds <= 0:
            self.timer.stop()
            self.is_running = False
            self.time_expired.emit()
    
    def update_display(self):
        """Update the timer display."""
        if self.time_limit_minutes <= 0:
            self.time_label.setText("No Time Limit")
            return
        
        # Format time as HH:MM:SS or MM:SS
        hours = self.time_remaining_seconds // 3600
        minutes = (self.time_remaining_seconds % 3600) // 60
        seconds = self.time_remaining_seconds % 60
        
        if hours > 0:
            time_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            time_text = f"{minutes:02d}:{seconds:02d}"
        
        self.time_label.setText(time_text)
        
        # Update progress bar
        if self.progress_bar:
            self.progress_bar.setValue(self.time_remaining_seconds)
        
        # Change color based on time remaining
        if self.time_remaining_seconds <= 300:  # Last 5 minutes
            color = "#F44336"  # Red
        elif self.time_remaining_seconds <= 900:  # Last 15 minutes
            color = "#FF9800"  # Orange
        else:
            color = "#FB8C00"  # Normal orange
        
        self.time_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {color};
                background-color: #1F1B16;
                border: 1px solid #9C8978;
                border-radius: 8px;
                padding: 8px;
                min-width: 120px;
            }}
        """)
    
    def get_elapsed_time_seconds(self) -> int:
        """Get the elapsed time in seconds."""
        return self.total_seconds - self.time_remaining_seconds
    
    def get_remaining_time_seconds(self) -> int:
        """Get the remaining time in seconds."""
        return self.time_remaining_seconds
    
    def set_time_limit(self, minutes: int):
        """Set a new time limit."""
        self.time_limit_minutes = minutes
        self.time_remaining_seconds = minutes * 60
        self.total_seconds = self.time_remaining_seconds
        
        # Recreate UI if needed
        if minutes > 0 and not self.progress_bar:
            self.setup_ui()
        elif minutes <= 0 and self.progress_bar:
            self.progress_bar.setVisible(False)
        
        self.update_display()