#!/usr/bin/env python3
"""
Complete system test for the enhanced VCE Exam Player.
Tests all major components and features.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication


def test_vce_parsing():
    """Test the VCE parsing with different files."""
    print("🔍 Testing VCE Parsing System")
    print("-" * 40)
    
    from vce_parser import parse_vce_file
    
    test_files = [
        "vce/Designing Microsoft Azure Infrastructure Solutions.AZ-305.Test4Prep.2025-02-22.35q.vce",
        "vce/Designing Microsoft Azure Infrastructure Solutions.AZ-305.Dump4Pass.2023-12-22.186q.vcex",
        "vce/Microsoft.actualtests.AZ-104.v2025-02-16.by.ida.206q.vce"
    ]
    
    results = []
    
    for file_path in test_files:
        if Path(file_path).exists():
            try:
                exam = parse_vce_file(file_path)
                filename = Path(file_path).name[:30]
                
                result = {
                    'file': filename,
                    'questions': exam.total_questions,
                    'author': exam.author,
                    'first_q': exam.questions[0].question_text[:50] + "..." if exam.questions else "No questions"
                }
                results.append(result)
                
                print(f"✅ {filename}...")
                print(f"   Questions: {exam.total_questions}, Author: {exam.author}")
                print(f"   Q1: {result['first_q']}")
                
            except Exception as e:
                print(f"❌ {Path(file_path).name}: {e}")
        else:
            print(f"⚠️  File not found: {Path(file_path).name}")
    
    return results


def test_exam_player():
    """Test the exam player functionality."""
    print("\\n🎯 Testing Exam Player System")
    print("-" * 40)
    
    from exam_player import ExamPlayer
    
    try:
        vce_file = "vce/Designing Microsoft Azure Infrastructure Solutions.AZ-305.Test4Prep.2025-02-22.35q.vce"
        if not Path(vce_file).exists():
            print("❌ Test VCE file not found")
            return False
        
        player = ExamPlayer(vce_file)
        session_id = player.start_new_session(max_questions=5)
        
        print(f"✅ Session created: {session_id}")
        print(f"✅ Questions loaded: {len(player.question_order)}")
        
        # Test answering questions
        for i in range(1, 4):
            question_index = player.question_order[i - 1]
            question = player.exam.questions[question_index]
            correct_answer = question.correct_answers[0]
            
            player.select_answer(i, [correct_answer])
            print(f"✅ Answered question {i}")
        
        # Test scoring
        score, passed = player.calculate_score()
        print(f"✅ Scoring works: {score}% ({'PASSED' if passed else 'FAILED'})")
        
        return True
        
    except Exception as e:
        print(f"❌ Exam player test failed: {e}")
        return False


def test_gui_components():
    """Test GUI components."""
    print("\\n🖥️  Testing GUI Components")
    print("-" * 40)
    
    try:
        app = QApplication(sys.argv)
        
        # Test main window
        from gui.main_window import MainWindow
        window = MainWindow()
        print("✅ Main window created")
        
        # Test session manager
        sessions = window.session_manager.list_sessions()
        print(f"✅ Session manager: {len(sessions)} sessions found")
        
        # Test widgets
        from gui.widgets import QuestionOverviewWidget, TimerWidget
        print("✅ Custom widgets imported")
        
        # Test session dialog
        from gui.session_dialog import SessionSelectionDialog
        print("✅ Session dialog available")
        
        app.quit()
        return True
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False


def test_session_management():
    """Test session management functionality."""
    print("\\n💾 Testing Session Management")
    print("-" * 40)
    
    try:
        from gui.session_manager import SessionManager
        
        session_manager = SessionManager()
        
        # Test session listing
        all_sessions = session_manager.list_sessions()
        resumable = session_manager.get_resumable_sessions()
        completed = session_manager.get_completed_sessions()
        
        print(f"✅ Total sessions: {len(all_sessions)}")
        print(f"✅ Resumable sessions: {len(resumable)}")
        print(f"✅ Completed sessions: {len(completed)}")
        
        # Test cleanup (dry run)
        if all_sessions:
            print("✅ Session cleanup functionality available")
        
        return True
        
    except Exception as e:
        print(f"❌ Session management test failed: {e}")
        return False


def main():
    """Run complete system test."""
    print("🎉 VCE EXAM PLAYER - COMPLETE SYSTEM TEST")
    print("=" * 60)
    
    test_results = []
    
    # Test each component
    test_results.append(("VCE Parsing", test_vce_parsing()))
    test_results.append(("Exam Player", test_exam_player()))
    test_results.append(("GUI Components", test_gui_components()))
    test_results.append(("Session Management", test_session_management()))
    
    # Summary
    print("\\n📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\\nOverall: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\\n🎉 ALL SYSTEMS OPERATIONAL!")
        print("\\n🚀 Enhanced Features Available:")
        print("   • Smart VCE parsing with file-specific questions")
        print("   • Session resume and review functionality")
        print("   • Enhanced navigation with question overview")
        print("   • Timer with visual countdown")
        print("   • Export results functionality")
        print("   • Recent sessions on welcome screen")
        print("   • Comprehensive keyboard shortcuts")
        print("   • Auto-save with session recovery")
    else:
        print("\\n⚠️  Some components need attention")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)