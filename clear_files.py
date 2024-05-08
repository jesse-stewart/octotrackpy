import os
import shutil
from alive_progress import alive_bar

def clear_temp_files(directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist. No action needed.")
        return
    
    # List all files and directories in the directory
    files_and_directories = os.listdir(directory)
    if not files_and_directories:
        print("The directory is already empty.")
        return
    
    # Setting up the progress bar with the total number of items to process
    total_items = len(files_and_directories)
    with alive_bar(total_items, title='Deleting items') as bar:
        # Delete each file and directory in the directory
        for item in files_and_directories:
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Deleted file: {item}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted directory and its contents: {item}")
            bar()  # Update the progress bar after processing each item
    
    print("All files and directories have been deleted.")

if __name__ == "__main__":
    temp_directory = '/home/jesse/temp'
    clear_temp_files(temp_directory)
