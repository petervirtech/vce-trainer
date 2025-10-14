#!/usr/bin/env python3
"""
Simple test script to debug VCE parser issues
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_import():
    """Test if we can import the modules."""
    try:
        from vce_parser import parse_simple_text_format, Question, Exam
        print("✓ Successfully imported parser modules")
        return True
    except Exception as e:
        print(f"✗ Failed to import parser modules: {e}")
        return False

def test_file_reading():
    """Test if we can read the sample file."""
    try:
        with open('sample_exam.vce', 'r') as f:
            content = f.read()
        print(f"✓ Successfully read sample file ({len(content)} characters)")
        print("First few lines:")
        for i, line in enumerate(content.split('\n')[:5]):
            print(f"  {i+1}: {line}")
        return content
    except Exception as e:
        print(f"✗ Failed to read sample file: {e}")
        return None

def test_simple_parsing(content):
    """Test the simple text parser."""
    if not content:
        return False

    try:
        from vce_parser import parse_simple_text_format
        exam = parse_simple_text_format('sample_exam.vce')

        print("✓ Successfully parsed exam")
        print(f"  Title: {exam.title}")
        print(f"  Author: {exam.author}")
        print(f"  Questions: {exam.total_questions}")

        if exam.questions:
            print("  Sample question:")
            q = exam.questions[0]
            print(f"    Q{q.id}: {q.question_text}")
            for i, ans in enumerate(q.answers):
                marker = ' ✓' if i in q.correct_answers else ''
                print(f"      {chr(65+i)}. {ans}{marker}")

        return True
    except Exception as e:
        print(f"✗ Failed to parse exam: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("=== VCE Parser Test ===")

    # Test imports
    if not test_basic_import():
        return

    # Test file reading
    content = test_file_reading()
    if not content:
        return

    # Test parsing
    if not test_simple_parsing(content):
        return

    print("\n✓ All tests passed! Parser is working correctly.")

if __name__ == "__main__":
    main()
