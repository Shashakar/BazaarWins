import os
import subprocess
from fileSetup import training_folder, contrast_folder, grayscale_folder, binary_folder

output_tr_file = "./combined_training_data.tr"
unicharset_output = "unicharset"

def combine_data():
    # Specify directories containing .tr files
    directories = [training_folder, contrast_folder, grayscale_folder, binary_folder]

    # Define the output combined .tr file


    # Open the output file in binary mode to write combined contents
    with open(output_tr_file, "wb") as output_file:
        for directory in directories:
            # Get all .tr files in the current directory
            for tr_file in os.listdir(directory):
                if tr_file.endswith(".tr"):
                    tr_file_path = os.path.join(directory, tr_file)
                    # Skip blank .tr files
                    if os.path.getsize(tr_file_path) == 0:
                        print(f"Skipping blank file: {tr_file_path}")
                        continue
                    # Read and write each .tr file's content to the combined output file
                    with open(tr_file_path, "rb") as file:
                        output_file.write(file.read())

    print(f"All .tr files combined into {output_tr_file}")

def import_data():
    # Run mftraining
    try:
        subprocess.run(
            ["mftraining", "-U", unicharset_output, "-O", unicharset_output, output_tr_file],
            check=True
        )
        print("mftraining completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"mftraining failed with error: {e}")

    # Run cntraining
    try:
        subprocess.run(
            ["cntraining", output_tr_file],
            check=True
        )
        print("cntraining completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"cntraining failed with error: {e}")