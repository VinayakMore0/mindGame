"""
Audio module for Cipher Clash game.
Handles sound effects and adaptive soundtrack based on game state.
"""

import os
import time
import threading
import random
from pygame import mixer

# Initialize the mixer
mixer.init()

# Audio channels
CHANNEL_MUSIC = 0
CHANNEL_SFX = 1
CHANNEL_TICKING = 2
CHANNEL_MORSE = 3

# Volume settings
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7
TICKING_VOLUME = 0.4
MORSE_VOLUME = 0.3

# Paths
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "sounds")

# Sound files
SOUND_FILES = {
    # Sound effects
    "correct": "correct.wav",
    "incorrect": "incorrect.wav",
    "hint": "hint.wav",
    "game_over": "game_over.wav",
    "menu_select": "menu_select.wav",
    "typing": "typing.wav",
    
    # Ticking sounds
    "tick_normal": "tick_normal.wav",
    "tick_fast": "tick_fast.wav",
    "tick_urgent": "tick_urgent.wav",
    
    # Morse code sounds
    "morse_dot": "morse_dot.wav",
    "morse_dash": "morse_dash.wav",
    
    # Music tracks
    "ambient_normal": "ambient_normal.mp3",
    "ambient_intense": "ambient_intense.mp3"
}

# Morse code patterns for letters
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
}

# Sound objects
sounds = {}
current_music = None
ticking_thread = None
morse_thread = None
is_running = False

def init_audio():
    """Initialize audio system and load sound files."""
    global sounds
    
    # Create mixer channels
    mixer.set_num_channels(8)
    
    # Check if audio directory exists
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)
        print(f"Created audio directory: {AUDIO_DIR}")
        print("Note: You'll need to add sound files to this directory.")
        return False
    
    # Load available sound files
    for sound_name, filename in SOUND_FILES.items():
        file_path = os.path.join(AUDIO_DIR, filename)
        if os.path.exists(file_path):
            try:
                sounds[sound_name] = mixer.Sound(file_path)
                print(f"Loaded sound: {sound_name}")
            except Exception as e:
                print(f"Error loading sound {sound_name}: {e}")
        else:
            print(f"Sound file not found: {file_path}")
    
    return len(sounds) > 0

def play_sound(sound_name):
    """
    Play a sound effect once.
    
    Args:
        sound_name (str): Name of the sound to play
    """
    if sound_name in sounds:
        channel = mixer.Channel(CHANNEL_SFX)
        channel.set_volume(SFX_VOLUME)
        channel.play(sounds[sound_name])

def play_music(music_name, loop=True):
    """
    Play background music.
    
    Args:
        music_name (str): Name of the music track to play
        loop (bool): Whether to loop the music
    """
    global current_music
    
    if music_name in sounds:
        channel = mixer.Channel(CHANNEL_MUSIC)
        channel.set_volume(MUSIC_VOLUME)
        channel.play(sounds[music_name], loops=-1 if loop else 0)
        current_music = music_name

def stop_music():
    """Stop the currently playing music."""
    mixer.Channel(CHANNEL_MUSIC).stop()
    global current_music
    current_music = None

def play_morse_code(text, speed=0.1):
    """
    Play text as Morse code.
    
    Args:
        text (str): Text to convert to Morse code
        speed (float): Speed factor (lower is faster)
    """
    if 'morse_dot' not in sounds or 'morse_dash' not in sounds:
        return
    
    text = text.upper()
    morse_sequence = []
    
    # Convert text to Morse code sequence
    for char in text:
        if char in MORSE_CODE:
            for symbol in MORSE_CODE[char]:
                morse_sequence.append(symbol)
            morse_sequence.append(' ')  # Space between letters
    
    # Play the Morse code
    channel = mixer.Channel(CHANNEL_MORSE)
    channel.set_volume(MORSE_VOLUME)
    
    for symbol in morse_sequence:
        if symbol == '.':
            channel.play(sounds['morse_dot'])
            time.sleep(speed)
        elif symbol == '-':
            channel.play(sounds['morse_dash'])
            time.sleep(speed * 3)
        elif symbol == ' ':
            time.sleep(speed * 3)  # Space between letters

def morse_code_thread(message, speed=0.1):
    """
    Thread function to play Morse code in the background.
    
    Args:
        message (str): Message to play as Morse code
        speed (float): Speed factor
    """
    global is_running
    
    while is_running:
        play_morse_code(message, speed)
        time.sleep(2)  # Pause between repetitions

def start_morse_code_background(message, speed=0.1):
    """
    Start playing Morse code in the background.
    
    Args:
        message (str): Message to play as Morse code
        speed (float): Speed factor
    """
    global morse_thread, is_running
    
    if morse_thread is not None and morse_thread.is_alive():
        stop_morse_code()
    
    is_running = True
    morse_thread = threading.Thread(target=morse_code_thread, args=(message, speed))
    morse_thread.daemon = True
    morse_thread.start()

def stop_morse_code():
    """Stop the background Morse code."""
    global is_running
    is_running = False
    mixer.Channel(CHANNEL_MORSE).stop()

def adaptive_ticking(time_remaining, time_limit):
    """
    Play ticking sounds that adapt to remaining time.
    
    Args:
        time_remaining (float): Remaining time in seconds
        time_limit (float): Total time limit in seconds
    """
    # Calculate time percentage
    time_percent = time_remaining / time_limit
    
    # Select appropriate ticking sound based on time remaining
    if time_percent > 0.5:
        tick_sound = 'tick_normal'
        delay = 1.0  # Normal ticking (once per second)
    elif time_percent > 0.25:
        tick_sound = 'tick_normal'
        delay = 0.5  # Faster ticking (twice per second)
    else:
        tick_sound = 'tick_urgent'
        delay = 0.25  # Urgent ticking (four times per second)
    
    # Adjust volume based on time remaining (gets louder as time runs out)
    volume = TICKING_VOLUME * (1.0 + (1.0 - time_percent) * 0.5)
    volume = min(1.0, volume)  # Cap at maximum volume
    
    # Play the tick if available
    if tick_sound in sounds:
        channel = mixer.Channel(CHANNEL_TICKING)
        channel.set_volume(volume)
        channel.play(sounds[tick_sound])
    
    return delay

def ticking_thread_function(time_limit):
    """
    Thread function for adaptive ticking.
    
    Args:
        time_limit (float): Total time limit in seconds
    """
    global is_running
    start_time = time.time()
    
    while is_running:
        elapsed = time.time() - start_time
        remaining = max(0, time_limit - elapsed)
        
        if remaining <= 0:
            break
            
        delay = adaptive_ticking(remaining, time_limit)
        time.sleep(delay)

def start_adaptive_ticking(time_limit):
    """
    Start adaptive ticking based on time limit.
    
    Args:
        time_limit (float): Total time limit in seconds
    """
    global ticking_thread, is_running
    
    if ticking_thread is not None and ticking_thread.is_alive():
        stop_adaptive_ticking()
    
    is_running = True
    ticking_thread = threading.Thread(target=ticking_thread_function, args=(time_limit,))
    ticking_thread.daemon = True
    ticking_thread.start()

def stop_adaptive_ticking():
    """Stop the adaptive ticking."""
    global is_running
    is_running = False
    mixer.Channel(CHANNEL_TICKING).stop()

def adapt_soundtrack(time_remaining, time_limit):
    """
    Adapt the soundtrack based on remaining time.
    
    Args:
        time_remaining (float): Remaining time in seconds
        time_limit (float): Total time limit in seconds
    """
    global current_music
    
    # Calculate time percentage
    time_percent = time_remaining / time_limit
    
    # Switch music tracks based on time pressure
    if time_percent < 0.3 and current_music != 'ambient_intense' and 'ambient_intense' in sounds:
        play_music('ambient_intense')
    elif time_percent >= 0.3 and current_music != 'ambient_normal' and 'ambient_normal' in sounds:
        play_music('ambient_normal')

def cleanup():
    """Clean up audio resources."""
    stop_adaptive_ticking()
    stop_morse_code()
    stop_music()
    mixer.quit()

# Test function
def test_audio():
    """Test audio functionality."""
    if init_audio():
        print("Playing test sounds...")
        
        # Test sound effects
        play_sound("correct")
        time.sleep(1)
        
        # Test music
        play_music("ambient_normal")
        time.sleep(2)
        
        # Test Morse code
        print("Playing Morse code for 'SOS'...")
        play_morse_code("SOS")
        time.sleep(2)
        
        # Test adaptive ticking
        print("Testing adaptive ticking...")
        start_adaptive_ticking(10)
        
        # Wait and clean up
        time.sleep(5)
        cleanup()
        print("Audio test complete.")
    else:
        print("Audio initialization failed.")

if __name__ == "__main__":
    test_audio()
