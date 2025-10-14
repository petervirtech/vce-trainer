#!/usr/bin/env python3
"""
Interactive command-line interface for VCE Exam Player
Provides a user-friendly way to take VCE exams with navigation and progress tracking.
"""

import os
import sys
from typing import List, Optional
from pathlib import Path

from exam_player import ExamPlayer


class ExamInterface:
    """Interactive command-line interface for exam taking."""

    def __init__(self, vce_file_path: str):
        """Initialize the exam interface."""
        self.player = ExamPlayer(vce_file_path)
        self.current_mode = "menu"  # menu, exam, review

    def run(self):
        """Run the main interface loop."""
        print("Welcome to VCE Exam Player!")
        print("=" * 50)

        while True:
            try:
                if self.current_mode == "menu":
                    self.show_main_menu()
                elif self.current_mode == "exam":
                    self.run_exam_mode()
                elif self.current_mode == "review":
                    self.run_review_mode()
                else:
                    break
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                input("Press Enter to continue...")

    def show_main_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 50)
        print("VCE EXAM PLAYER - MAIN MENU")
        print("=" * 50)
        print("1. Start New Exam")
        print("2. Resume Exam Session")
        print("3. Review Completed Session")
        print("4. Show Available Sessions")
        print("5. Exit")
        print("=" * 50)

        choice = input("Select option (1-5): ").strip()

        if choice == "1":
            self.start_new_exam()
        elif choice == "2":
            self.resume_exam()
        elif choice == "3":
            self.review_completed_session()
        elif choice == "4":
            self.show_sessions()
        elif choice == "5":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

    def start_new_exam(self):
        """Start a new exam session."""
        session_id = self.player.start_new_session()
        if session_id:
            self.current_mode = "exam"
            self.run_exam_session()

    def resume_exam(self):
        """Resume an existing exam session."""
        sessions = list(self.player.session_dir.glob("session_*.json"))
        if not sessions:
            print("No saved sessions found.")
            return

        print("\nAvailable sessions:")
        for i, session_file in enumerate(sessions, 1):
            session_id = session_file.stem
            print(f"{i}. {session_id}")

        try:
            choice = int(input("Select session: ")) - 1
            if 0 <= choice < len(sessions):
                session_file = sessions[choice]
                session_id = session_file.stem

                # Load session data
                import json
                with open(session_file, 'r') as f:
                    session_data = json.load(f)

                self.player.current_session = self.player.ExamSession(**session_data)
                print(f"Resumed session: {session_id}")
                self.current_mode = "exam"
                self.run_exam_session()
        except (ValueError, IndexError):
            print("Invalid selection.")

    def review_completed_session(self):
        """Review a completed exam session."""
        sessions = list(self.player.session_dir.glob("session_*.json"))
        completed_sessions = []

        for session_file in sessions:
            try:
                import json
                with open(session_file, 'r') as f:
                    data = json.load(f)
                if data.get('status') == 'completed':
                    completed_sessions.append((session_file, data))
            except:
                continue

        if not completed_sessions:
            print("No completed sessions found.")
            return

        print("\nCompleted sessions:")
        for i, (session_file, data) in enumerate(completed_sessions, 1):
            score = data.get('score', 'N/A')
            print(f"{i}. {session_file.stem} - Score: {score}%")

        try:
            choice = int(input("Select session to review: ")) - 1
            if 0 <= choice < len(completed_sessions):
                session_file, session_data = completed_sessions[choice]

                self.player.current_session = self.player.ExamSession(**session_data)
                self.player.current_session.status = "reviewed"
                print(f"Loaded session for review: {session_file.stem}")
                self.current_mode = "review"
        except (ValueError, IndexError):
            print("Invalid selection.")

    def show_sessions(self):
        """Show all available sessions."""
        sessions = list(self.player.session_dir.glob("session_*.json"))
        if not sessions:
            print("No sessions found.")
            return

        print("\nAll Sessions:")
        print("-" * 60)
        for session_file in sessions:
            try:
                import json
                with open(session_file, 'r') as f:
                    data = json.load(f)

                session_id = session_file.stem
                status = data.get('status', 'unknown')
                score = data.get('score', 'N/A')
                print(f"{session_id} - Status: {status}, Score: {score}%")
            except Exception as e:
                print(f"{session_file.stem} - Error reading session")
        print("-" * 60)
        input("Press Enter to continue...")

    def run_exam_session(self):
        """Run the exam taking session."""
        if not self.player.current_session:
            print("No active session.")
            self.current_mode = "menu"
            return

        print(f"\nStarting exam: {self.player.exam.title}")
        print(f"Total questions: {len(self.player.exam.questions)}")

        while True:
            # Display the current question
            current_q = self.player.current_session.current_question
            question = self.player.display_question(current_q)

            if not question:
                print("Error: Could not display question.")
                self.current_mode = "menu"
                break

            # Show the exam menu
            self.show_exam_menu()

            choice = input("Choice: ").strip().lower()

            if choice == "q":
                print("Returning to main menu...")
                self.current_mode = "menu"
                break
            elif choice == "n" or choice == "":
                self.next_question()
            elif choice == "p":
                self.previous_question()
            elif choice == "j":
                self.jump_to_question()
            elif choice == "a":
                self.select_answer()
            elif choice == "m":
                self.mark_question()
            elif choice == "s":
                self.show_progress()
            elif choice == "e":
                if self.confirm_end_exam():
                    self.end_exam()
                    break
            else:
                print("Invalid choice. Try again.")

    def run_review_mode(self):
        """Run the review mode for completed exams."""
        if not self.player.current_session:
            print("No session loaded for review.")
            self.current_mode = "menu"
            return

        print(f"\nReviewing session: {self.player.current_session.session_id}")
        print(f"Score: {self.player.current_session.score}%")
        print(f"Status: {'PASSED' if self.player.current_session.passed else 'FAILED'}")

        question_num = 1
        while True:
            question = self.player.display_question(question_num)
            if not question:
                break

            # Show if question was answered correctly
            if question_num in self.player.current_session.answers:
                user_answer = self.player.current_session.answers[question_num]
                status = "CORRECT" if user_answer.is_correct else "INCORRECT"
                print(f"Your answer: {status}")
                if hasattr(user_answer, 'selected_answers') and user_answer.selected_answers:
                    selected = [chr(65 + i) for i in user_answer.selected_answers]
                    print(f"You selected: {', '.join(selected)}")

            print("\nReview Menu:")
            print("n - Next question")
            print("p - Previous question")
            print("j - Jump to question")
            print("q - Back to main menu")

            choice = input("Choice: ").strip().lower()

            if choice == "q":
                self.current_mode = "menu"
                break
            elif choice == "n" or choice == "":
                if question_num < len(self.player.exam.questions):
                    question_num += 1
                else:
                    print("Already at last question.")
            elif choice == "p":
                if question_num > 1:
                    question_num -= 1
                else:
                    print("Already at first question.")
            elif choice == "j":
                try:
                    q_num = int(input(f"Jump to question (1-{len(self.player.exam.questions)}): "))
                    if 1 <= q_num <= len(self.player.exam.questions):
                        question_num = q_num
                    else:
                        print("Invalid question number.")
                except ValueError:
                    print("Invalid input.")
            else:
                print("Invalid choice.")

    def show_exam_menu(self):
        """Show the exam mode menu."""
        if not self.player.current_session:
            return

        current = self.player.current_session.current_question
        total = len(self.player.exam.questions)
        progress = self.player.show_progress()

        print(f"\nQuestion {current} of {total}")
        if progress.get('percentage'):
            print(f"Progress: {progress['percentage']}% complete ({progress['answered']} answered)")

        print("\nCommands:")
        print("n - Next question")
        print("p - Previous question")
        print("j - Jump to question")
        print("a - Select answer")
        print("m - Mark for review")
        print("s - Show progress")
        print("e - End exam")
        print("q - Quit to main menu")

    def next_question(self):
        """Move to next question."""
        if not self.player.current_session:
            return

        next_q = self.player.next_question()
        if next_q != self.player.current_session.current_question:
            print(f"Moved to question {next_q}")
        else:
            print("Already at last question.")

    def previous_question(self):
        """Move to previous question."""
        if not self.player.current_session:
            return

        prev_q = self.player.previous_question()
        if prev_q != self.player.current_session.current_question:
            print(f"Moved to question {prev_q}")
        else:
            print("Already at first question.")

    def jump_to_question(self):
        """Jump to a specific question."""
        if not self.player.current_session:
            return

        try:
            q_num = int(input(f"Jump to question (1-{len(self.player.exam.questions)}): "))
            if self.player.jump_to_question(q_num):
                print(f"Jumped to question {q_num}")
            else:
                print("Invalid question number.")
        except ValueError:
            print("Invalid input.")

    def select_answer(self):
        """Select answer for current question."""
        if not self.player.current_session:
            return

        current_q = self.player.current_session.current_question
        question = self.player.exam.questions[current_q - 1]

        print(f"\nSelecting answer for Question {current_q}")
        print("Available options:")
        for i in range(len(question.answers)):
            print(f"{i + 1}. {chr(65 + i)}")

        try:
            if question.type.upper() == "MULTIPLE":
                print("Enter answer numbers separated by commas (e.g., 1,3):")
                answer_input = input("Answer(s): ").strip()
                indices = [int(x.strip()) - 1 for x in answer_input.split(",") if x.strip().isdigit()]
            else:
                print("Enter answer number:")
                answer_num = int(input("Answer: ").strip())
                indices = [answer_num - 1]

            if all(0 <= i < len(question.answers) for i in indices):
                if self.player.select_answer(current_q, indices):
                    print("Answer recorded.")
                else:
                    print("Failed to record answer.")
            else:
                print("Invalid answer number(s).")

        except (ValueError, IndexError):
            print("Invalid input.")

    def mark_question(self):
        """Mark current question for review."""
        if not self.player.current_session:
            return

        current_q = self.player.current_session.current_question
        if self.player.mark_question(current_q):
            print(f"Question {current_q} marked for review.")
        else:
            print("Failed to mark question.")

    def show_progress(self):
        """Show exam progress."""
        progress = self.player.show_progress()
        if progress:
            print("\nProgress:")
            print(f"Answered: {progress['answered']}/{progress['total']} ({progress['percentage']}%)")
            print(f"Marked for review: {progress['marked']}")
            print(f"Current question: {progress['current_question']}")
        else:
            print("No active session.")

    def confirm_end_exam(self) -> bool:
        """Confirm ending the exam."""
        print("\nAre you sure you want to end the exam?")
        print("This will calculate your final score.")
        confirm = input("Type 'yes' to confirm: ").strip().lower()
        return confirm == "yes"

    def end_exam(self):
        """End the exam and show results."""
        if not self.player.current_session:
            return

        self.player.end_session()
        print("\nReturning to main menu...")
        self.current_mode = "menu"


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python exam_interface.py <vce_file_path>")
        sys.exit(1)

    vce_file = sys.argv[1]
    if not Path(vce_file).exists():
        print(f"VCE file not found: {vce_file}")
        sys.exit(1)

    interface = ExamInterface(vce_file)
    interface.run()


if __name__ == "__main__":
    main()
