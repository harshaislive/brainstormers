#!/usr/bin/env python3
"""
Web-compatible version of Brainstormers for deployment
Uses the terminal interface as the main entry point
"""

import os
from brainstorm_crew import main

if __name__ == "__main__":
    # For web deployment, run the terminal version
    print("🌐 Running Brainstormers in web mode...")
    print("Note: This runs the terminal interface. For GUI, run locally with 'python brainstorm_gui.py'")
    main()