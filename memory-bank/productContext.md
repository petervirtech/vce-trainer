# Product Context

## Overview
VCE Exam Player is a comprehensive exam simulation application designed to read and play VCE (Visual CertExam) files for training and testing purposes. The application supports interactive exam taking, session management, progress tracking, and review functionality.

## Core Features
- VCE File Parsing: Reads and parses .vce and .vcex exam files
- Interactive Exam Interface: Command-line interface for taking exams (with GUI development in progress)
- Session Management: Save and resume exam sessions
- Progress Tracking: Track answered questions and exam progress
- Scoring System: Automatic scoring with pass/fail determination
- Review Mode: Review completed exams with correct/incorrect indicators
- Question Navigation: Jump between questions, mark for review
- Multiple Question Types: Support for single and multiple choice questions

## Architecture
- **Backend**: Python-based with modular design (vce_parser.py, exam_player.py, exam_interface.py)
- **Frontend**: Currently CLI-based, transitioning to PyQt6 GUI
- **Data Storage**: JSON-based session files for persistence
- **Supported Formats**: Proprietary VCE binary format with fallback mechanisms

## Target Users
- IT certification candidates (particularly Microsoft Azure certifications)
- Training organizations
- Educational institutions
- Individuals preparing for certification exams

## Technology Stack
- **Core**: Python 3.8+
- **GUI**: PyQt6 for desktop application
- **Data**: JSON for session storage, custom VCE parsing
- **Platform**: Cross-platform (macOS, Windows, Linux)

## Business Value
- Provides legitimate educational tool for exam preparation
- Supports multiple exam providers and formats
- Enables practice and review without live exam pressure
- Includes progress tracking and performance analysis

## Current Development Focus
Transitioning from CLI to modern GUI interface using PyQt6, maintaining all existing functionality while improving user experience.

---

*Initial context established: 2025-10-07T11:00:00Z*
