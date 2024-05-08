# player.py
import os
import sys
import threading
import keyboard
import termios
import tty
from ui_utils import clear_screen, suppress_alsa_warnings
from audio_utils import convert_audio_files, convert_audio, play_audio
from text_utils import LargeAlphabet, get_large_glyphs
from ascii_magic import AsciiArt, from_image

def main(tracks_dir):
    temp_folder = './temp'
    if not os.path.exists(tracks_dir):
        print("Tracks directory does not exist.")
        return

    track_folders = [os.path.join(tracks_dir, d) for d in os.listdir(tracks_dir) if os.path.isdir(os.path.join(tracks_dir, d))]
    track_folders.sort()

    if not track_folders:
        print("No track folders found.")
        return

    track_index = 0
    stop_event = threading.Event()
    pause_event = threading.Event()
    fastforward_event = threading.Event()
    rewind_event = threading.Event()
    track_change_event = threading.Event()
    playing = False  # Control flag to start playing

    clear_screen()  # Clear the screen initially
    print("\033[92m" + get_large_glyphs("Loading...") + "\033[0m")

    # convert all audio files and place them in the temp folder
    for track_folder in track_folders:
        files = [os.path.join(track_folder, f) for f in os.listdir(track_folder) if f.endswith('.wav')]
        files = sorted(files)[:8]  # Limit to the first 8 files
        convert_audio_files(files, temp_folder + '/' + os.path.basename(track_folder))

    print()
    print()

    print(get_large_glyphs("Octophonic", LargeAlphabet))
    print("\033[90m" + get_large_glyphs("8x Audio Player") + "\033[0m")
    print("v0.1 Alpha")
    print()

    print("\033[92mControls:\033[0m")
    print("Space: Play/Pause")
    print("N: Next track")
    print("P: Previous track")

    def handle_keys():
        nonlocal track_index, playing
        while True:
            key = keyboard.read_event()
            if key.event_type == keyboard.KEY_DOWN:
                if key.name == 'esc':
                    return  # Exit the loop and therefore the program
                elif key.name == 'n':
                    stop_event.set()
                    track_change_event.set()
                    print("\033[92mNext track\033[0m")
                elif key.name == 'p':
                    stop_event.set()
                    track_change_event.set()
                    track_index = max(0, track_index - 2)  # Move back to the previous track
                    print("\033[92mPrevious track\033[0m")
                elif key.name == 'right':
                    rewind_event.clear()
                    fastforward_event.set() if not fastforward_event.is_set() else fastforward_event.clear()
                    # print("\033[92mFast forward\033[0m" if fastforward_event.is_set() else "\033[92mPlaying\033[0m")
                elif key.name == 'left':
                    fastforward_event.clear()
                    rewind_event.set() if not rewind_event.is_set() else rewind_event.clear()
                    # print("\033[92mRewind\033[0m" if rewind_event.is_set() else "\033[92mPlaying\033[0m")
                elif key.name == 'space':
                    if not playing:
                        playing = True
                        pause_event.clear()
                        # print("\033[92mPlaying\033[0m")
                    else:
                        pause_event.set() if not pause_event.is_set() else pause_event.clear()
                        # print("\033[92mPaused\033[0m" if pause_event.is_set() else "\033[92mPlaying\033[0m")

    listener_thread = threading.Thread(target=handle_keys, daemon=True)
    listener_thread.start()

    # Disable terminal echo
    old_attr = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    try:
        while True:
            if playing:  # Only play if the user has started playback
                # try:
                    # artwork = os.path.join(track_folders[track_index], 'artwork.gif')
                    # get width of artwork
                    # artworkwidth = os.popen(f"identify -format %w {artwork}").read()
                    # my_art = AsciiArt.from_image(artwork)
                    # my_art.to_terminal(columns=50 * 2,
                    #     char='█', width_ratio=2)
                    # print()
                # except Exception as e:
                #     print()

                print("\033[91m" + get_large_glyphs(track_folders[track_index].split('/')[-1]) + "\033[0m")

                track_folder = track_folders[track_index]
                files = [os.path.join(track_folder, f) for f in os.listdir(track_folder) if f.endswith('.wav')]
                files = sorted(files)[:8]  # Limit to the first 8 files
                play_audio(track_folder, files, temp_folder, stop_event, pause_event, fastforward_event, rewind_event, track_change_event)

                if track_change_event.is_set():
                    track_change_event.clear()
                    fastforward_event.clear()
                    rewind_event.clear()
                    stop_event.clear()
                    track_index = (track_index + 1) % len(track_folders)  # Loop back to the first track after the last one

    finally:
        # Restore terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main_script.py <tracks_dir>")
        sys.exit(1)
    tracks_dir = sys.argv[1]
    main(tracks_dir)
