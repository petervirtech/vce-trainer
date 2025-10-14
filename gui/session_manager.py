"""
Session Manager for VCE Exam Player GUI.
Handles session persistence, auto-save, and recovery.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtWidgets import QMessageBox

from exam_player import ExamPlayer, ExamSession


class SessionManager(QObject):
    """Manages exam sessions with auto-save and recovery features."""
    
    # Signals
    session_saved = pyqtSignal(str)  # session_id
    session_loaded = pyqtSignal(str)  # session_id
    auto_save_completed = pyqtSignal()
    
    def __init__(self, session_dir: str = "sessions", parent=None):
        super().__init__(parent)
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)
        
        # Auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_interval = 30000  # 30 seconds
        
        self.current_player: Optional[ExamPlayer] = None
        self.auto_save_enabled = True
    
    def set_exam_player(self, player: ExamPlayer):
        """Set the current exam player for auto-save."""
        self.current_player = player
        if self.auto_save_enabled:
            self.start_auto_save()
    
    def start_auto_save(self):
        """Start the auto-save timer."""
        if not self.auto_save_timer.isActive():
            self.auto_save_timer.start(self.auto_save_interval)
    
    def stop_auto_save(self):
        """Stop the auto-save timer."""
        self.auto_save_timer.stop()
    
    def auto_save(self):
        """Perform automatic session save."""
        if (self.current_player and 
            self.current_player.current_session and 
            self.current_player.current_session.status == "in_progress"):
            
            try:
                self.save_session(self.current_player.current_session)
                self.auto_save_completed.emit()
            except Exception as e:
                print(f"Auto-save failed: {e}")
    
    def save_session(self, session: ExamSession) -> bool:
        """Save a session to file."""
        try:
            session_file = self.session_dir / f"{session.session_id}.json"
            
            # Update timestamp
            session.end_time = datetime.now().isoformat()
            
            # Convert to dict for JSON serialization
            session_data = self._session_to_dict(session)
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            self.session_saved.emit(session.session_id)
            return True
            
        except Exception as e:
            print(f"Failed to save session: {e}")
            return False
    
    def load_session(self, session_id: str) -> Optional[ExamSession]:
        """Load a session from file."""
        try:
            session_file = self.session_dir / f"{session_id}.json"
            
            if not session_file.exists():
                return None
            
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            session = self._dict_to_session(session_data)
            self.session_loaded.emit(session_id)
            return session
            
        except Exception as e:
            print(f"Failed to load session: {e}")
            return None
    
    def list_sessions(self) -> List[Dict]:
        """List all available sessions with metadata."""
        sessions = []
        
        for session_file in self.session_dir.glob("session_*.json"):
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)
                
                # Extract metadata
                session_info = {
                    'session_id': data.get('session_id', session_file.stem),
                    'exam_title': data.get('exam_title', 'Unknown Exam'),
                    'start_time': data.get('start_time', ''),
                    'status': data.get('status', 'unknown'),
                    'score': data.get('score'),
                    'total_questions': len(data.get('answers', {})),
                    'file_path': str(session_file)
                }
                
                sessions.append(session_info)
                
            except Exception as e:
                print(f"Error reading session file {session_file}: {e}")
                continue
        
        # Sort by start time (newest first)
        sessions.sort(key=lambda x: x['start_time'], reverse=True)
        return sessions
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session file."""
        try:
            session_file = self.session_dir / f"{session_id}.json"
            if session_file.exists():
                session_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"Failed to delete session: {e}")
            return False
    
    def get_resumable_sessions(self) -> List[Dict]:
        """Get sessions that can be resumed (in_progress status)."""
        all_sessions = self.list_sessions()
        return [s for s in all_sessions if s['status'] == 'in_progress']
    
    def get_completed_sessions(self) -> List[Dict]:
        """Get completed sessions for review."""
        all_sessions = self.list_sessions()
        return [s for s in all_sessions if s['status'] == 'completed']
    
    def cleanup_old_sessions(self, days_old: int = 30):
        """Clean up sessions older than specified days."""
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        cleaned_count = 0
        
        for session_file in self.session_dir.glob("session_*.json"):
            try:
                if session_file.stat().st_mtime < cutoff_time:
                    session_file.unlink()
                    cleaned_count += 1
            except Exception as e:
                print(f"Error cleaning up {session_file}: {e}")
        
        return cleaned_count
    
    def _session_to_dict(self, session: ExamSession) -> Dict:
        """Convert ExamSession to dictionary for JSON serialization."""
        from dataclasses import asdict
        return asdict(session)
    
    def _dict_to_session(self, data: Dict) -> ExamSession:
        """Convert dictionary to ExamSession object."""
        from exam_player import UserAnswer
        
        # Convert answers dict if present
        if 'answers' in data and data['answers']:
            converted_answers = {}
            for key, answer_data in data['answers'].items():
                if isinstance(answer_data, dict):
                    converted_answers[int(key)] = UserAnswer(**answer_data)
                else:
                    # Handle old format
                    converted_answers[int(key)] = answer_data
            data['answers'] = converted_answers
        
        return ExamSession(**data)
    
    def export_session_summary(self, session_id: str, export_path: str) -> bool:
        """Export session summary to text file."""
        try:
            session = self.load_session(session_id)
            if not session:
                return False
            
            with open(export_path, 'w') as f:
                f.write(f"VCE Exam Player - Session Summary\n")
                f.write(f"=" * 50 + "\n\n")
                f.write(f"Session ID: {session.session_id}\n")
                f.write(f"Exam: {session.exam_title}\n")
                f.write(f"Start Time: {session.start_time}\n")
                f.write(f"End Time: {session.end_time}\n")
                f.write(f"Status: {session.status}\n")
                f.write(f"Score: {session.score}%\n")
                f.write(f"Passed: {'Yes' if session.passed else 'No'}\n")
                f.write(f"Total Time: {session.total_time_spent // 60}:{session.total_time_spent % 60:02d}\n")
                f.write(f"\nQuestions Answered: {len(session.answers) if session.answers else 0}\n")
                
                if session.answers:
                    correct_count = sum(1 for ans in session.answers.values() 
                                      if ans.is_correct)
                    f.write(f"Correct Answers: {correct_count}\n")
                    f.write(f"Accuracy: {correct_count / len(session.answers) * 100:.1f}%\n")
            
            return True
            
        except Exception as e:
            print(f"Failed to export session summary: {e}")
            return False