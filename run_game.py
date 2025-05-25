#!/usr/bin/env python3
"""
Wrapper script to run the Mind Games launcher with the correct Python path.
"""
import os
import sys

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Now import and run the launcher
from mind_games_project.launcher import main

if __name__ == "__main__":
    main()
