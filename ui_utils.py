# ui_utils.py
import os
import time

def clear_screen():
    os.system('clear')

def spinner_animation(duration=5):
    spinner = ['-', '\\', '|', '/']
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in spinner:
            print(f'\r{frame}', end='')
            time.sleep(0.1)

# Suppress ALSA warnings by redirecting stderr to null
def suppress_alsa_warnings():
    if os.name != 'nt':  # Only apply on Unix-like systems
        null = open('/dev/null', 'w')
        os.dup2(null.fileno(), 2)
