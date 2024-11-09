import os
import subprocess

from fileSetup import grayscale_folder, training_folder, binary_folder, contrast_folder, setup_data
from combineTrainingData import combine_data, import_data

def generate_training_file(path, folder, base_img_name):
    subprocess.run(
        ["tesseract", path, os.path.join(folder, base_img_name), "--psm", "10", "nobatch", "box.train"]
    )

setup_data()

# Iterate through each file in the folder
for filename in os.listdir(training_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        # Get the base name of the file (e.g., "image1" from "image1.png")
        base_name = os.path.splitext(filename)[0]
        image_name = base_name + ".png"
        image_path = os.path.join(training_folder, filename)
        gs_image_path = os.path.join(grayscale_folder, image_name)
        ct_image_path = os.path.join(contrast_folder, image_name)
        bn_image_path = os.path.join(binary_folder, image_name)
        box_path = os.path.join(training_folder, f"{base_name}.box")

        # Check if the corresponding .txt file exists
        if not os.path.exists(box_path):
            print(f"Warning: Box file {box_path} not found for {filename}. Skipping.")
            continue

        # Run tesseract in training mode to generate .box file
        print(f"Generating .tr file for {filename}...")
        # Run tesseract in training mode to generate .box file
        print("Base Image Training")
        generate_training_file(image_path, training_folder, base_name)

        print("Grayscale Image Training")
        generate_training_file(gs_image_path, grayscale_folder, base_name)

        print("Contrast Image Training")
        generate_training_file(ct_image_path, contrast_folder, base_name)

        print("Binary Image Training")
        generate_training_file(bn_image_path, binary_folder, base_name)

print("Training data generation completed.")
print("Combining training data")
combine_data()
print("Importing data to Tesseract")
import_data()
print("Finished!")