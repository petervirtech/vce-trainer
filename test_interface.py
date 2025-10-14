#!/usr/bin/env python3
"""
Test script to debug exam_interface issues
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_exam_player_import():
    """Test if ExamPlayer can be imported and initialized."""
    try:
        from exam_player import ExamPlayer
        print("✓ Successfully imported ExamPlayer")
        return ExamPlayer
    except Exception as e:
        print(f"✗ Failed to import ExamPlayer: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_exam_player_init(player_class):
    """Test if ExamPlayer can be initialized."""
    if not player_class:
        return None

    try:
        player = player_class('sample_exam.vce')
        print("✓ Successfully initialized ExamPlayer")
        return player
    except Exception as e:
        print(f"✗ Failed to initialize ExamPlayer: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_exam_interface_import():
    """Test if ExamInterface can be imported."""
    try:
        from exam_interface import ExamInterface
        print("✓ Successfully imported ExamInterface")
        return ExamInterface
    except Exception as e:
        print(f"✗ Failed to import ExamInterface: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_exam_interface_init(interface_class):
    """Test if ExamInterface can be initialized."""
    if not interface_class:
        return None

    try:
        interface = interface_class('sample_exam.vce')
        print("✓ Successfully initialized ExamInterface")
        return interface
    except Exception as e:
        print(f"✗ Failed to initialize ExamInterface: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_interface_methods(interface):
    """Test basic interface methods."""
    if not interface:
        return False

    try:
        # Test if player is properly initialized
        if not hasattr(interface, 'player') or not interface.player:
            print("✗ Interface player not initialized")
            return False

        # Test if exam is loaded
        if not hasattr(interface.player, 'exam') or not interface.player.exam:
            print("✗ Exam not loaded in player")
            return False

        exam = interface.player.exam
        print("✓ Exam loaded successfully")
        print(f"  Title: {exam.title}")
        print(f"  Questions: {exam.total_questions}")

        if exam.questions:
            q = exam.questions[0]
            print(f"  First question: {q.question_text[:50]}...")

        return True
    except Exception as e:
        print(f"✗ Error testing interface methods: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("=== Exam Interface Debug Test ===")

    # Test ExamPlayer
    player_class = test_exam_player_import()
    if not player_class:
        print("Cannot continue without ExamPlayer")
        return

    player = test_exam_player_init(player_class)
    if not player:
        print("Cannot continue without ExamPlayer instance")
        return

    # Test ExamInterface
    interface_class = test_exam_interface_import()
    if not interface_class:
        print("ExamInterface import failed, but ExamPlayer works")
        print("You can use ExamPlayer directly for basic functionality")
        return

    interface = test_exam_interface_init(interface_class)
    if not interface:
        print("ExamInterface initialization failed")
        return

    # Test interface methods
    if not test_interface_methods(interface):
        print("Interface method tests failed")
        return

    print("\n✓ All interface tests passed!")
    print("The exam interface should be working correctly.")

if __name__ == "__main__":
    main()
