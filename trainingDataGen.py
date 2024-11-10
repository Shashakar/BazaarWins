import os
import shutil
import subprocess
from fileSetup import grayscale_folder, training_folder, binary_folder, contrast_folder, setup_data
from combineTrainingData import combine_data, import_data
from tesseractInteraction import handle_traineddata

# generates combined training data .tr file
def generate_training_file(path, folder, base_img_name):
    try:
        subprocess.run(
            ["tesseract", path, os.path.join(folder, base_img_name), "--psm", "10", "nobatch", "box.train"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate training data for {path}: {e}")
    except FileNotFoundError:
        print("Tesseract is not installed. Please install Tesseract first.")
        exit(1)

# generates unicharset file
def generate_unicharset_file():
    # Collect all .box files in the specified folders
    box_files = []
    directories = [training_folder, grayscale_folder, contrast_folder, binary_folder]
    for directory in directories:
        for file in os.listdir(directory):
            if file.endswith(".box"):
                box_files.append(os.path.join(directory, file))

    # Run unicharset_extractor on the collected .box files
    if box_files:
        try:
            subprocess.run(
                ["unicharset_extractor", *box_files],
                check=True
            )
            print("Successfully generated unicharset file.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate unicharset file: {e}")
    else:
        print("No .box files found in the specified directories.")

# moves required files to data folder
def move_to_data_folder():
    prefix = "BazaarFont"
    root_folder = "."
    data_folder = os.path.join(root_folder, "data")

    # Ensure the data folder exists
    os.makedirs(data_folder, exist_ok=True)

    # Define the expected file extensions
    required_files = ["unicharset", "inttemp", "pffmtable", "normproto", "shapetable"]

    # Iterate through the required files, rename them with the prefix, and move them to the data folder
    for file_name in required_files:
        source_path = os.path.join(root_folder, file_name)
        if os.path.exists(source_path):
            # Add the prefix and set the new filename
            new_file_name = f"{prefix}.{file_name}"
            destination_path = os.path.join(data_folder, new_file_name)

            # Move and rename the file
            shutil.move(source_path, destination_path)
            print(f"Moved and renamed '{file_name}' to '{destination_path}'")
        else:
            print(f"Warning: File '{file_name}' not found in '{root_folder}'. Skipping.")

    print("File renaming and moving process completed.")

setup_data()

for filename in os.listdir(training_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        base_name = os.path.splitext(filename)[0]
        image_name = base_name + ".png"
        image_path = os.path.join(training_folder, filename)
        gs_image_path = os.path.join(grayscale_folder, image_name)
        ct_image_path = os.path.join(contrast_folder, image_name)
        bn_image_path = os.path.join(binary_folder, image_name)
        box_path = os.path.join(training_folder, f"{base_name}.box")

        if not os.path.exists(box_path):
            print(f"Warning: Box file {box_path} not found for {filename}. Skipping.")
            continue

        print(f"Generating .tr file for {filename}...")
        generate_training_file(image_path, training_folder, base_name)
        generate_training_file(gs_image_path, grayscale_folder, base_name)
        generate_training_file(ct_image_path, contrast_folder, base_name)
        generate_training_file(bn_image_path, binary_folder, base_name)

generate_unicharset_file()

print("Training data generation completed.")
print("Combining training data...")
combine_data()
print("Importing data to Tesseract...")
import_data()
print("Finished! Setting up the training data in Tesseract...")

# Move the required files to the data folder
move_to_data_folder()

# handle getting the data to tesseract
handle_traineddata()
