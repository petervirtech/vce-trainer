"""
VCE Exam Player - Interactive exam taking application
Supports taking practice exams from VCE files with progress tracking and review.
"""

import time
import json
import random
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import os

from vce_parser import Exam, Question, parse_vce_file


@dataclass
class UserAnswer:
    """Represents a user's answer to a question."""
    question_id: int
    selected_answers: List[int]  # indices of selected answers
    time_spent: int  # seconds spent on this question
    timestamp: str
    is_correct: Optional[bool] = None
    is_marked: bool = False


@dataclass
class ExamSession:
    """Represents a complete exam session."""
    session_id: str
    exam_title: str
    start_time: str
    end_time: Optional[str] = None
    total_time_spent: int = 0  # seconds
    status: str = "in_progress"  # in_progress, completed, reviewed
    answers: Optional[Dict[int, UserAnswer]] = None
    current_question: int = 1
    score: Optional[int] = None
    passed: Optional[bool] = None

    def __post_init__(self):
        if self.answers is None:
            self.answers = {}

    def get_answers(self) -> Dict[int, UserAnswer]:
        """Safely get the answers dictionary."""
        if self.answers is None:
            self.answers = {}
        return self.answers


class ExamPlayer:
    """Main exam player class that manages exam sessions and interactions."""

    def __init__(self, vce_file_path: str, session_dir: str = "sessions"):
        """Initialize the exam player with a VCE file."""
        self.vce_file_path = vce_file_path
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)

        # Load exam data
        self.exam = parse_vce_file(vce_file_path)
        self.current_session: Optional[ExamSession] = None
        self.question_order: List[int] = []  # Will be set when starting session

        print(f"Loaded exam: {self.exam.title}")
        print(f"Total questions: {self.exam.total_questions}")
        print(f"Author: {self.exam.author}")

    def start_new_session(self, randomize_questions: bool = False, max_questions: int = 0) -> str:
        # Ensure consistent question ordering for review purposes
        randomize_questions = False
        """Start a new exam session."""
        session_id = f"session_{int(time.time())}"
        timestamp = datetime.now().isoformat()

        # Set up question order
        self.question_order = list(range(len(self.exam.questions)))
        if max_questions > 0 and max_questions < len(self.question_order):
            # Limit to max_questions
            if randomize_questions:
                # Randomly select max_questions
                self.question_order = random.sample(self.question_order, max_questions)
            else:
                # Take first max_questions
                self.question_order = self.question_order[:max_questions]
        elif randomize_questions:
            random.shuffle(self.question_order)

        # Update exam total questions to reflect the limited set
        self.exam.total_questions = len(self.question_order)

        self.current_session = ExamSession(
            session_id=session_id,
            exam_title=self.exam.title,
            start_time=timestamp,
            current_question=1
        )

        print(f"\n{'='*50}")
        print("NEW EXAM SESSION STARTED")
        print(f"Session ID: {session_id}")
        print(f"Exam: {self.exam.title}")
        print(f"Total Questions: {self.exam.total_questions}")
        if self.exam.time_limit:
            print(f"Time Limit: {self.exam.time_limit} minutes")
        print(f"Passing Score: {self.exam.passing_score}%")
        print(f"{'='*50}\n")

        return session_id

    def display_question(self, question_num: int) -> Optional[Question]:
        """Display a specific question (question_num is the display order 1-based)."""
        if 1 <= question_num <= len(self.question_order):
            actual_index = self.question_order[question_num - 1]
            question = self.exam.questions[actual_index]

            print(f"\n{'-'*60}")
            print(f"Question {question_num} of {len(self.exam.questions)}")
            print(f"{'-'*60}")
            print(f"Type: {question.type.upper()}")

            # Display question text (cleaned up)
            question_text = self._clean_text(question.question_text)
            print(f"\n{question_text}\n")

            # Display answers
            for i, answer in enumerate(question.answers):
                marker = "□"  # Unchecked checkbox
                if (self.current_session and
                    self.current_session.answers and
                    question_num in self.current_session.answers):
                    user_answer = self.current_session.answers[question_num]
                    if i in user_answer.selected_answers:
                        marker = "✓"  # Checked checkbox

                answer_text = self._clean_text(answer)
                print(f"{marker} {chr(65 + i)}. {answer_text}")

            print(f"{'-'*60}")

            return question
        return None

    def select_answer(self, question_num: int, answer_indices: List[int]) -> bool:
        """Record user's answer for a question."""
        if not self.current_session:
            print("No active session. Please start a new session first.")
            return False

        if not self.current_session.answers:
            self.current_session.answers = {}

        if question_num not in self.current_session.answers:
            # First time answering this question
            self.current_session.answers[question_num] = UserAnswer(
                question_id=question_num,
                selected_answers=answer_indices,
                time_spent=0,  # Will be updated when moving to next question
                timestamp=datetime.now().isoformat()
            )
        else:
            # Update existing answer
            self.current_session.answers[question_num].selected_answers = answer_indices
            self.current_session.answers[question_num].timestamp = datetime.now().isoformat()

        print(f"Answer recorded for question {question_num}")
        return True

    def mark_question(self, question_num: int) -> bool:
        """Mark a question for review."""
        if not self.current_session or not self.current_session.answers:
            return False

        if question_num not in self.current_session.answers:
            return False

        self.current_session.answers[question_num].is_marked = True
        print(f"Question {question_num} marked for review")
        return True

    def next_question(self) -> int:
        """Move to the next question."""
        if not self.current_session:
            return 1

        if self.current_session.current_question < len(self.question_order):
            self.current_session.current_question += 1
        return self.current_session.current_question

    def previous_question(self) -> int:
        """Move to the previous question."""
        if not self.current_session:
            return 1

        if self.current_session.current_question > 1:
            self.current_session.current_question -= 1
        return self.current_session.current_question

    def jump_to_question(self, question_num: int) -> bool:
        """Jump to a specific question (display order)."""
        if 1 <= question_num <= len(self.question_order):
            if self.current_session:
                self.current_session.current_question = question_num
            return True
        return False

    def calculate_score(self) -> Tuple[int, bool]:
        """Calculate the exam score and pass/fail status."""
        if not self.current_session:
            return 0, False

        correct_answers = 0
        total_questions = len(self.question_order)

        if not self.current_session.answers:
            return 0, False

        for question in self.exam.questions:
            if question.id in self.current_session.answers:
                user_answer = self.current_session.answers[question.id]
                # Check if user's selected answers match correct answers
                if set(user_answer.selected_answers) == set(question.correct_answers):
                    correct_answers += 1
                    user_answer.is_correct = True
                else:
                    user_answer.is_correct = False

        score = int((correct_answers / total_questions) * 100)
        passed = score >= self.exam.passing_score

        self.current_session.score = score
        self.current_session.passed = passed

        return score, passed

    def end_session(self) -> Dict[str, Any]:
        """End the current session and save results."""
        if not self.current_session:
            return {}

        # Calculate final score
        score, passed = self.calculate_score()

        # Update session end time and total time
        self.current_session.end_time = datetime.now().isoformat()
        if self.current_session.start_time:
            start_time = datetime.fromisoformat(self.current_session.start_time.replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(self.current_session.end_time.replace('Z', '+00:00'))
            self.current_session.total_time_spent = int((end_time - start_time).total_seconds())

        self.current_session.status = "completed"

        # Save session to file
        session_file = self.session_dir / f"{self.current_session.session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(asdict(self.current_session), f, indent=2)

        print(f"\n{'='*60}")
        print("EXAM COMPLETED!")
        print(f"Final Score: {score}%")
        print(f"Status: {'PASSED' if passed else 'FAILED'}")
        minutes = self.current_session.total_time_spent // 60
        seconds = self.current_session.total_time_spent % 60
        print(f"Total Time: {minutes}:{seconds:02d}")
        print(f"Session saved to: {session_file}")
        print(f"{'='*60}\n")

        return asdict(self.current_session)

    def show_progress(self) -> Dict[str, Any]:
        """Show current progress statistics."""
        if not self.current_session or not self.current_session.answers:
            return {}

        answered = len(self.current_session.answers)
        total = len(self.question_order)
        percentage = (answered / total) * 100

        marked = sum(1 for ans in self.current_session.answers.values() if ans.is_marked)

        return {
            "answered": answered,
            "total": total,
            "percentage": round(percentage, 1),
            "marked": marked,
            "current_question": self.current_session.current_question
        }

    def review_session(self, session_id: str) -> bool:
        """Load a completed session for review."""
        session_file = self.session_dir / f"{session_id}.json"
        if not session_file.exists():
            print(f"Session file not found: {session_file}")
            return False

        with open(session_file, 'r') as f:
            session_data = json.load(f)

        self.current_session = ExamSession(**session_data)
        self.current_session.status = "reviewed"

        print(f"\nLoaded session for review: {session_id}")
        print(f"Exam: {self.current_session.exam_title}")
        print(f"Score: {self.current_session.score}%")
        print(f"Status: {'PASSED' if self.current_session.passed else 'FAILED'}")

        return True

    def _clean_text(self, text: str) -> str:
        """Clean up text extracted from VCE file."""
        if not text:
            return ""

        # Remove null bytes and control characters
        cleaned = text.replace('\x00', '').replace('\x01', '').replace('\x02', '')
        cleaned = ''.join(char for char in cleaned if ord(char) >= 32 or char in '\n\r\t')

        # Try to decode if it's bytes-like
        if isinstance(cleaned, bytes):
            try:
                cleaned = cleaned.decode('utf-8', errors='ignore')
            except:
                cleaned = cleaned.decode('latin-1')

        return cleaned.strip()


def main():
    """Main function for command-line exam player."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python exam_player.py <vce_file_path> [session_id]")
        print("\nCommands:")
        print("  start    - Start a new exam session")
        print("  resume   - Resume an existing session")
        print("  review   - Review a completed session")
        sys.exit(1)

    vce_file = sys.argv[1]
    if not Path(vce_file).exists():
        print(f"VCE file not found: {vce_file}")
        sys.exit(1)

    player = ExamPlayer(vce_file)

    if len(sys.argv) >= 3:
        command = sys.argv[2]
    else:
        print("\nAvailable commands:")
        print("1. start  - Start new exam")
        print("2. resume - Resume existing session")
        print("3. review - Review completed session")
        command = input("Choose command: ").strip().lower()

    if command == "start":
        player.start_new_session()
        return player

    elif command == "resume":
        sessions = list(player.session_dir.glob("session_*.json"))
        if not sessions:
            print("No saved sessions found.")
            return None

        print("\nAvailable sessions:")
        for i, session_file in enumerate(sessions, 1):
            session_id = session_file.stem
            print(f"{i}. {session_id}")

        try:
            choice = int(input("Select session: ")) - 1
            if 0 <= choice < len(sessions):
                session_id = sessions[choice].stem
                # Load session data
                with open(sessions[choice], 'r') as f:
                    session_data = json.load(f)
                player.current_session = ExamSession(**session_data)
                print(f"Resumed session: {session_id}")
        except (ValueError, IndexError):
            print("Invalid selection.")

    elif command == "review":
        sessions = list(player.session_dir.glob("session_*.json"))
        if not sessions:
            print("No saved sessions found.")
            return None

        print("\nCompleted sessions:")
        completed_sessions = []
        for session_file in sessions:
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)
                if data.get('status') == 'completed':
                    completed_sessions.append((session_file, data))
                    print(f"{len(completed_sessions)}. {session_file.stem} - Score: {data.get('score', 'N/A')}%")
            except:
                continue

        if not completed_sessions:
            print("No completed sessions found.")
            return None

        try:
            choice = int(input("Select session to review: ")) - 1
            if 0 <= choice < len(completed_sessions):
                session_file, session_data = completed_sessions[choice]
                player.current_session = ExamSession(**session_data)
                player.current_session.status = "reviewed"
                print(f"Loaded session for review: {session_file.stem}")
        except (ValueError, IndexError):
            print("Invalid selection.")

    return player


if __name__ == "__main__":
    player = main()
    if player:
        print("Exam player initialized successfully!")
