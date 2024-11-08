import os
import subprocess

from convertToGrayscale import grayscale_folder

# Define the folder containing images and their corresponding text files
training_folder = "./training_images"
grayscale_folder = "./grayscale_images"
contrast_folder = "./contrast_images"


base_name = "G"
image_name = base_name + ".png"
image_path = os.path.join(training_folder, image_name)
gs_image_path = os.path.join(grayscale_folder, image_name)
ct_image_path = os.path.join(contrast_folder, image_name)

# Run tesseract in training mode to generate .box file
subprocess.run(["tesseract", image_path, os.path.join(training_folder, base_name), "--psm", "7", "nobatch", "box.train"])
subprocess.run(["tesseract", gs_image_path, os.path.join(grayscale_folder, base_name), "--psm", "7", "nobatch", "box.train"])
subprocess.run(["tesseract", ct_image_path, os.path.join(contrast_folder, base_name), "--psm", "7", "nobatch", "box.train"])

print("Training data generation completed.")
