#!/usr/bin/env python3
"""
Script to fix import statements in the Cipher Clash game.
This script will recursively search through Python files in the games directory
and update import statements from 'games.cipher_clash' to 'mind_games_project.games.cipher_clash'.
"""

import os
import re
import sys

def fix_imports(directory):
    """
    Recursively search through Python files and fix import statements.
    
    Args:
        directory (str): The directory to search in
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                fix_file_imports(file_path)

def fix_file_imports(file_path):
    """
    Fix import statements in a single file.
    
    Args:
        file_path (str): Path to the Python file
    """
    print(f"Processing {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace import statements
    modified_content = re.sub(
        r'from\s+games\.cipher_clash',
        'from mind_games_project.games.cipher_clash',
        content
    )
    
    modified_content = re.sub(
        r'import\s+games\.cipher_clash',
        'import mind_games_project.games.cipher_clash',
        modified_content
    )
    
    # Write back if changes were made
    if content != modified_content:
        print(f"  - Fixed imports in {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)

if __name__ == "__main__":
    # Get the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    games_dir = os.path.join(project_dir, 'mind_games_project', 'games')
    
    print(f"Fixing imports in {games_dir}")
    fix_imports(games_dir)
    print("Done!")
