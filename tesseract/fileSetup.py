from PIL import Image, ImageEnhance
import os
import shutil

training_folder = os.path.join("..", "training_images")
grayscale_folder = os.path.join("..", "grayscale_images")
contrast_folder = os.path.join("..", "contrast_images")
binary_folder = os.path.join("..", "binary_images")
tessdata_folder_windows = os.path.join("C:", "Program Files", "Tesseract-OCR", "tessdata")
tessdata_folder_mac = os.path.join("/", "usr", "local", "share", "tessdata")

def save_image(image, folder, base_name):
    os.makedirs(folder, exist_ok=True)
    image_path = os.path.join(folder, base_name) + ".png"
    image.save(image_path, icc_profile=None)

def convert_to_grayscale(path, base_name):
    img = Image.open(path).convert("L")
    save_image(img, grayscale_folder, base_name)
    return img

def convert_to_contrast(gs_image, base_name):
    enhancer = ImageEnhance.Contrast(gs_image)
    img_contrast = enhancer.enhance(2)  # Increase contrast factor
    save_image(img_contrast, contrast_folder, base_name)
    return img_contrast

def convert_to_binary(gs_image, base_name):
    binary_img = gs_image.point(lambda x: 0 if x < 128 else 255, '1')
    save_image(binary_img, binary_folder, base_name)
    return binary_img

def setup_data():
    os.makedirs(grayscale_folder, exist_ok=True)
    os.makedirs(contrast_folder, exist_ok=True)
    os.makedirs(binary_folder, exist_ok=True)

    for filename in os.listdir(training_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            base_name = os.path.splitext(filename)[0]
            image_path = os.path.join(training_folder, filename)

            gs_image = convert_to_grayscale(image_path, base_name)
            convert_to_contrast(gs_image, base_name)
            convert_to_binary(gs_image, base_name)

        if filename.endswith(".box") or filename == "font_properties":
            original_file = os.path.join(training_folder, filename)
            shutil.copy(original_file, grayscale_folder)
            shutil.copy(original_file, contrast_folder)
            shutil.copy(original_file, binary_folder)
