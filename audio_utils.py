# audio_utils.py
import os
import subprocess
import pyaudio
import wave
import numpy as np
from alive_progress import alive_bar

from progress import get_progress_bar

def convert_audio_files(files, output_folder):
    """Converts audio files to mono PCM format using ffmpeg."""
    os.makedirs(output_folder, exist_ok=True)
    with alive_bar(len(files), bar='filling', spinner='dots_waves') as bar:
        for f in files:
            output_file = os.path.join(output_folder, os.path.basename(f))
            convert_audio(f, output_file)
            bar()
    print("\n")

def convert_audio(input_file, output_file):
    """Converts audio file to mono PCM format using ffmpeg."""
    output_folder = os.path.dirname(output_file)
    os.makedirs(output_folder, exist_ok=True)
    parent_folder = os.path.basename(os.path.dirname(input_file))
    if not os.path.exists(output_file):
        command = ["ffmpeg", "-y", "-i", input_file, "-ac", "1", "-ar", "44100", "-acodec", "pcm_s16le", output_file]
        # print just the fine name
        print("\033[92m" + f"{'+ ' + parent_folder + '/' + os.path.basename(input_file)}" + "\033[0m")
        subprocess.run(command, check=True)
    else: 
        # print just the file name
        print(f"{parent_folder + '/' + os.path.basename(input_file)}")

def play_audio(folder, files, temp_folder, stop_event, pause_event, fastforward_event, rewind_event, track_change_event):
    """Plays multiple audio files with PyAudio, allows pausing, fast-forwarding, and rewinding."""
    converted_files = []

    for f in files:
        file_name = os.path.basename(f)
        output_subfolder = os.path.join(temp_folder, os.path.basename(folder))
        converted_file = os.path.join(output_subfolder, file_name)
        converted_files.append(converted_file)
        convert_audio(f, converted_file)


    waves = [wave.open(f, 'rb') for f in converted_files]
    frame_rate = waves[0].getframerate()

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=8, rate=frame_rate, output=True)

    frames_per_buffer = 1024
    total_frames = min(wf.getnframes() for wf in waves)
    percentage_progress = 0
    frames_read = 0

    # Speed multipliers
    normal_speed = 1
    fast_speed = 10  # Adjust as needed
    rewind_speed = 2  # Adjust as needed

    try:
        while any(waves) and not stop_event.is_set():
            if not pause_event.is_set():
                arrays = []

                for index in range(8):
                    wave_file = waves[index] if index < len(waves) else None
                    if wave_file:
                        if fastforward_event.is_set():
                            target_position = min(wave_file.tell() + frames_per_buffer * fast_speed, total_frames)
                            current_position = wave_file.tell()
                            step = (target_position - current_position) / frames_per_buffer
                            data = b""
                            for _ in range(frames_per_buffer):
                                data += wave_file.readframes(1)
                                wave_file.setpos(int(current_position))
                                current_position += step
                        elif rewind_event.is_set():
                            target_position = max(wave_file.tell() - frames_per_buffer * rewind_speed, 0)
                            current_position = wave_file.tell()
                            step = (target_position - current_position) / frames_per_buffer
                            data = b""
                            for _ in range(frames_per_buffer):
                                data += wave_file.readframes(1)
                                wave_file.setpos(int(current_position))
                                current_position += step
                        else:
                            data = wave_file.readframes(frames_per_buffer)

                        # Calculate percentage progress
                        current_frame = wave_file.tell()
                        percentage_progress = (current_frame / total_frames) * 100

                        print (f"\033[92m{get_progress_bar(percentage_progress)} {percentage_progress:.1f}%\033[0m", end="\r")
                        
                        # Check for progress and change track if necessary
                        if percentage_progress >= 99.5:
                            if not stop_event.is_set():
                                print("\033[94mEnd of Track - Next track\033[0m")
                                stop_event.set()
                                track_change_event.set()

                    else:
                        data = None

                    arrays.append(np.frombuffer(data, dtype=np.int16) if data else np.zeros(frames_per_buffer, dtype=np.int16))

                interleaved_signal = np.column_stack(arrays).ravel().astype(np.int16)
                stream.write(interleaved_signal.tobytes())

                # After writing the buffer, check if track change is needed
                if track_change_event.is_set():
                    break

    finally:
        stream.stop_stream()
        stream.close()
        for wf in waves:
            if wf:
                wf.close()
        p.terminate()
