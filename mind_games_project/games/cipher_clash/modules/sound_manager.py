"""
Sound Manager module for Cipher Clash game.
Handles the integration of audio with game events and states.
"""

import os
import time
import threading
from mind_games_project.games.cipher_clash.modules.audio import (
    init_audio, play_sound, play_music, stop_music,
    start_adaptive_ticking, stop_adaptive_ticking,
    start_morse_code_background, stop_morse_code,
    adapt_soundtrack, cleanup
)

class SoundManager:
    """Manages sound effects and music for the game."""
    
    def __init__(self):
        """Initialize the sound manager."""
        self.audio_enabled = False
        self.music_enabled = False
        self.sfx_enabled = False
        self.ticking_enabled = False
        self.morse_enabled = False
        self.time_limit = 0
        self.time_update_thread = None
        self.running = False
        
    def initialize(self):
        """Initialize audio system."""
        success = init_audio()
        if success:
            self.audio_enabled = True
            self.music_enabled = True
            self.sfx_enabled = True
            self.ticking_enabled = True
            self.morse_enabled = True
            return True
        return False
        
    def play_game_sound(self, sound_name):
        """
        Play a game sound effect.
        
        Args:
            sound_name (str): Name of the sound to play
        """
        if self.sfx_enabled:
            play_sound(sound_name)
            
    def start_game_music(self):
        """Start the game background music."""
        if self.music_enabled:
            play_music("ambient_normal")
            
    def stop_game_music(self):
        """Stop the game background music."""
        if self.music_enabled:
            stop_music()
            
    def start_game_ticking(self, time_limit):
        """
        Start the adaptive ticking sound based on time limit.
        
        Args:
            time_limit (float): Time limit in seconds
        """
        if self.ticking_enabled:
            self.time_limit = time_limit
            start_adaptive_ticking(time_limit)
            
    def stop_game_ticking(self):
        """Stop the adaptive ticking sound."""
        if self.ticking_enabled:
            stop_adaptive_ticking()
            
    def start_morse_message(self, message):
        """
        Start playing a message in Morse code.
        
        Args:
            message (str): Message to play in Morse code
        """
        if self.morse_enabled:
            start_morse_code_background(message, 0.1)
            
    def stop_morse_message(self):
        """Stop the Morse code message."""
        if self.morse_enabled:
            stop_morse_code()
            
    def update_soundtrack(self, time_remaining):
        """
        Update the soundtrack based on remaining time.
        
        Args:
            time_remaining (float): Remaining time in seconds
        """
        if self.music_enabled:
            adapt_soundtrack(time_remaining, self.time_limit)
            
    def start_time_update_thread(self, get_time_remaining_func):
        """
        Start a thread to update sounds based on remaining time.
        
        Args:
            get_time_remaining_func: Function that returns remaining time
        """
        self.running = True
        self.time_update_thread = threading.Thread(
            target=self._time_update_loop,
            args=(get_time_remaining_func,)
        )
        self.time_update_thread.daemon = True
        self.time_update_thread.start()
        
    def _time_update_loop(self, get_time_remaining_func):
        """
        Thread function to update sounds based on time.
        
        Args:
            get_time_remaining_func: Function that returns remaining time
        """
        while self.running:
            time_remaining = get_time_remaining_func()
            self.update_soundtrack(time_remaining)
            time.sleep(1)  # Update every second
            
    def stop_time_update_thread(self):
        """Stop the time update thread."""
        self.running = False
        if self.time_update_thread and self.time_update_thread.is_alive():
            self.time_update_thread.join(1)
            
    def play_game_event(self, event_name):
        """
        Play sounds for specific game events.
        
        Args:
            event_name (str): Name of the game event
        """
        if not self.audio_enabled:
            return
            
        if event_name == "game_start":
            self.start_game_music()
            self.play_game_sound("menu_select")
            
        elif event_name == "game_over":
            self.stop_game_ticking()
            self.stop_morse_message()
            self.play_game_sound("game_over")
            
        elif event_name == "correct_solution":
            self.play_game_sound("correct")
            
        elif event_name == "incorrect_solution":
            self.play_game_sound("incorrect")
            
        elif event_name == "hint_used":
            self.play_game_sound("hint")
            
        elif event_name == "low_time":
            # Start Morse code SOS when time is running low
            self.start_morse_message("SOS")
            
        elif event_name == "typing":
            self.play_game_sound("typing")
            
    def toggle_music(self):
        """Toggle music on/off."""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            stop_music()
        else:
            self.start_game_music()
        return self.music_enabled
        
    def toggle_sfx(self):
        """Toggle sound effects on/off."""
        self.sfx_enabled = not self.sfx_enabled
        return self.sfx_enabled
        
    def toggle_ticking(self):
        """Toggle ticking sounds on/off."""
        self.ticking_enabled = not self.ticking_enabled
        if not self.ticking_enabled:
            stop_adaptive_ticking()
        return self.ticking_enabled
        
    def toggle_morse(self):
        """Toggle Morse code sounds on/off."""
        self.morse_enabled = not self.morse_enabled
        if not self.morse_enabled:
            stop_morse_code()
        return self.morse_enabled
        
    def cleanup(self):
        """Clean up audio resources."""
        self.stop_time_update_thread()
        cleanup()

# Create a global instance
sound_manager = SoundManager()
