#!/usr/bin/env python3
import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.abspath(__file__))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from mind_games_project.games.cipher_clash.main import main
    print("Successfully imported the main function from cipher_clash!")
except Exception as e:
    print(f"Error importing cipher_clash: {e}")
    import traceback
    traceback.print_exc()

