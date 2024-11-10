import os
import subprocess

from fileSetup import binary_folder, grayscale_folder, contrast_folder, training_folder

base_name = "0"
image_name = base_name + ".png"
image_path = os.path.join(training_folder, image_name)
gs_image_path = os.path.join(grayscale_folder, image_name)
ct_image_path = os.path.join(contrast_folder, image_name)
bn_image_path = os.path.join(binary_folder, image_name)

def generate_training_file(path, folder):
    subprocess.run(
        ["tesseract", path, os.path.join(folder, base_name), "--psm", "10", "nobatch", "box.train"]
    )

# Run tesseract in training mode to generate .box file
print("Base Image Training")
generate_training_file(image_path, training_folder)

print("Grayscale Image Training")
generate_training_file(gs_image_path, grayscale_folder)

print("Contrast Image Training")
generate_training_file(ct_image_path, contrast_folder)

print("Binary Image Training")
generate_training_file(bn_image_path, binary_folder)

print("Training data generation completed.")

# Need more Gs for Quality

