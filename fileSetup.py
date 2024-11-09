from PIL import Image, ImageEnhance
import os
import shutil

training_folder = "./training_images"
grayscale_folder = "./grayscale_images"
contrast_folder = "./contrast_images"
binary_folder = "./binary_images"

def convert_to_grayscale(path, base_name):
    img = Image.open(path).convert("L")
    img.save(grayscale_folder + "/" + base_name + ".png", icc_profile=None)
    return img

def convert_to_contrast(gs_image, base_name):
    enhancer = ImageEnhance.Contrast(gs_image)
    img_contrast = enhancer.enhance(2)  # Increase contrast factor
    img_contrast.save(contrast_folder + "/" + base_name + ".png", icc_profile=None)
    return img_contrast

def convert_to_binary(gs_image, base_name):
    binary_img = gs_image.point(lambda x: 0 if x < 128 else 255, '1')
    binary_img.save(binary_folder + "/" + base_name + ".png", icc_profile=None)
    return binary_img

def setup_data():
    # Iterate through each file in the folder
    for filename in os.listdir(training_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            # Get the base name of the file (e.g., "image1" from "image1.png")
            base_name = os.path.splitext(filename)[0]
            image_path = os.path.join(training_folder, filename)
            text_path = os.path.join(training_folder, f"{base_name}.txt")

            gs_image = convert_to_grayscale(image_path, base_name)
            ct_image = convert_to_contrast(gs_image, base_name)
            bn_image = convert_to_binary(gs_image, base_name)

        if filename.endswith(".box"):
            # Copy the box file over to the appropriate folders
            shutil.copy(training_folder + "/" + filename, grayscale_folder)
            shutil.copy(training_folder + "/" + filename, contrast_folder)
            shutil.copy(training_folder + "/" + filename, binary_folder)

