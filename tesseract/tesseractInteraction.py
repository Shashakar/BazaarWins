import shutil
import subprocess
import os
from fileSetup import tessdata_folder_windows, tessdata_folder_mac

data_folder = "data"
output_file = "BazaarFont.traineddata"

def get_tessdata_path():
    # If Windows
    if os.name == "nt":
        return tessdata_folder_windows
    # If Mac
    elif os.name == "posix":
        return tessdata_folder_mac
    else:
        print("Operating system not supported.")
        return None

# Function to run the combine_tessdata command to create the .traineddata file
def combine_traineddata_files(data_folder, output_file):
    try:
        # Path to the combine_tessdata executable
        combine_tessdata_executable = "combine_tessdata"

        # Check if combine_tessdata is available in the system PATH
        if not shutil.which(combine_tessdata_executable):
            print("Error: 'combine_tessdata' not found in PATH.")
            return

        # Run the combine_tessdata command
        subprocess.run(
            [combine_tessdata_executable, os.path.join(data_folder, "BazaarFont.")],
            check=True
        )
        print(f"Combined files into {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error combining tessdata files: {e}")

# Function to move the .traineddata file into the Tesseract tessdata directory
def move_traineddata_into_tesseract():
    tessdata_path = get_tessdata_path()
    if tessdata_path:
        traineddata_path = os.path.join("..", data_folder, output_file)
        destination_path = os.path.join(tessdata_path, output_file)
        try:
            # Use shutil.move to move the traineddata file
            shutil.move(traineddata_path, destination_path)
            print(f"{output_file} moved to Tesseract tessdata directory: {tessdata_path}")
        except Exception as e:
            print(f"Error occurred while moving traineddata file: {e}")

# Function to handle the complete traineddata creation and moving process
def handle_traineddata():
    combine_traineddata_files(data_folder, output_file)
    move_traineddata_into_tesseract()
    print("Finished!")

if __name__ == "__main__":
    handle_traineddata()