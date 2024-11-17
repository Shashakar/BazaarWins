import os
import cv2
import logging
from logging_bazaar import setup_logging

# Set up logging
logger = setup_logging(logging.DEBUG, "ImageCropper")

# Cropping areas defined as percentages of a 1920x1080 image
# y, y, x, x
data_folder = os.path.join(".", "data")


def crop_and_save_images(image_path, crop_areas_percent):
    image_path_full = os.path.join(image_path)

    # Load the image
    image = cv2.imread(image_path_full)

    # Ensure the image was loaded successfully
    if image is None:
        logger.error(f"Error: Unable to load image '{image_path_full}'")
        return

    # Get image dimensions
    img_height, img_width, _ = image.shape

    # Loop through each area to crop and save
    for area_name, (y_start_percent, y_end_percent, x_start_percent, x_end_percent) in crop_areas_percent.items():
        # Calculate cropping coordinates based on image dimensions
        y_start = int(y_start_percent * img_height)
        y_end = int(y_end_percent * img_height)
        x_start = int(x_start_percent * img_width)
        x_end = int(x_end_percent * img_width)

        # Ensure cropping coordinates are within image boundaries
        y_start = max(0, y_start)
        y_end = min(img_height, y_end)
        x_start = max(0, x_start)
        x_end = min(img_width, x_end)

        # Crop the image
        cropped_image = image[y_start:y_end, x_start:x_end]
        upscale_factor = 2  # You can adjust this as needed
        cropped_image = cv2.resize(cropped_image, None, fx=upscale_factor, fy=upscale_factor,
                                   interpolation=cv2.INTER_CUBIC)

        # Save the cropped image
        output_path = f"{image_path.split('.')[0]}_{area_name}.png"

        # If data folder doesn't exist, create it
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        output_path = os.path.join(data_folder, output_path)
        cv2.imwrite(output_path, cropped_image)
        logger.info(f"Saved cropped image: {output_path}")


if __name__ == "__main__":
    # Example usage
    example_image_path = "example_screenshot.png"
    example_crop_areas = {
        "area1": (0.1, 0.3, 0.1, 0.3),
        "area2": (0.4, 0.6, 0.4, 0.6)
    }
    crop_and_save_images(example_image_path, example_crop_areas)
