# progress.py
# take a value between 0 and 100 and return a progress bar string. The progress bar should be 80 characters long and should be made up of the following characters: █ for completed progress, ░ for incomplete progress, and ▏ for the last character if the progress is not a multiple of 1.25. The progress bar should be enclosed in square brackets. For example, if the progress is 50, the progress bar should look like this: [████████

def get_progress_bar(progress):
    progress_bar = "█" * int(progress / 1.25) + "░" * (95 - int(progress / 1.25))
    if progress % 1.25 != 0:
        progress_bar = progress_bar[:-1] + ""
    return f"{progress_bar}"
