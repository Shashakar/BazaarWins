import os
import subprocess

from convertToGrayscale import grayscale_folder

# Define the folder containing images and their corresponding text files
training_folder = "./training_images"
grayscale_folder = "./grayscale_images"
contrast_folder = "./contrast_images"

# Iterate through each file in the folder
for filename in os.listdir(training_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        # Get the base name of the file (e.g., "image1" from "image1.png")
        base_name = os.path.splitext(filename)[0]
        image_path = os.path.join(training_folder, filename)
        grayscale_path = os.path.join(grayscale_folder, filename)
        text_path = os.path.join(training_folder, f"{base_name}.txt")

        # Check if the corresponding .txt file exists
        if not os.path.exists(text_path):
            print(f"Warning: Text file {text_path} not found for {filename}. Skipping.")
            continue

        # Run tesseract to create the .box file
#        print(f"Generating .tr file for {filename}...")
        #subprocess.run(["tesseract", image_path, os.path.join(training_folder, base_name), "batch.nochop", "makebox"])

        # Run tesseract in training mode to generate .box file
        print(f"Generating .tr file for {filename}...")
        subprocess.run(["tesseract", image_path, os.path.join(training_folder, base_name), "--psm", "7", "nobatch", "box.train"])
        subprocess.run(["tesseract", image_path, os.path.join(grayscale_folder, base_name), "nobatch", "box.train"])
        subprocess.run(["tesseract", image_path, os.path.join(contrast_folder, base_name), "nobatch", "box.train"])

        # Run tesseract to create the .tr file
#        print(f"Generating .tr file for {filename}...")
 #       subprocess.run(["tesseract", image_path, os.path.join(training_folder, base_name), "makebox"])

print("Training data generation completed.")
