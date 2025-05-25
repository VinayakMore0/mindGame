#!/usr/bin/env python3
"""
Debug script to help identify errors in the Cipher Clash game.
"""
import os
import sys
import traceback

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def run_with_exception_handling():
    try:
        # Import and run the launcher with detailed exception handling
        print("Starting Cipher Clash game through the launcher...")
        from mind_games_project.launcher import main
        main()
    except Exception as e:
        print(f"\n\n===== DETAILED ERROR INFORMATION =====")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nTraceback:")
        traceback.print_exc()
        print("\nThis information might help identify where the error is occurring.")
        print("===== END OF ERROR INFORMATION =====\n")
        
        input("Press Enter to exit...")

if __name__ == "__main__":
    run_with_exception_handling()
