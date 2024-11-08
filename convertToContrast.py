from PIL import Image, ImageEnhance
import os

training_folder = "./training_images"
grayscale_folder = "./grayscale_images"
contrast_folder = "./contrast_images"

# Iterate through each file in the folder
for filename in os.listdir(training_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        # Get the base name of the file (e.g., "image1" from "image1.png")
        base_name = os.path.splitext(filename)[0]
        image_path = os.path.join(training_folder, filename)
        text_path = os.path.join(training_folder, f"{base_name}.txt")

        img = Image.open(image_path).convert("L")  # Converts to grayscale
        enhancer = ImageEnhance.Contrast(img)
        img_contrast = enhancer.enhance(2)  # Increase contrast factor
        img_contrast.save(contrast_folder + "/" + base_name + ".png", icc_profile=None)