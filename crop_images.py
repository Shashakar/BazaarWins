import os

import cv2

base_path = os.path.join(".", "training_images", "game_examples")

# Paths to the images
image_paths = [
 #  "6winsbronzevictory_raidus.png",
 #   "10winsgoldvictoryemez.png",
    "10winsperfectvictoryjohn.png"
]

# Cropping areas defined as percentages of a 1920x1080 image
crop_areas_percent = {
    "title_username": (0.0, 0.185, 0.0, 0.208),       # Grand Founder and Username area (Top Left)
    "wins": (0.093, 0.278, 0.260, 0.625),             # Number of Wins and Victory Type (Top Middle)
    "items": (0.278, 0.556, 0.339, 0.990),            # Item Square Images (Upper Middle Right)
    "stats": (0.556, 0.625, 0.339, 0.938),            # Stats (Center Middle Right)
    "skills": (0.625, 0.856, 0.339, 0.938)            # Skill Circular Images (Lower Bottom Right)
}

def crop_and_save_images(image_path, crop_areas_percent):
    image_path_full = os.path.join(base_path, image_path)
    # Load the image
    image = cv2.imread(image_path_full)

    # Ensure the image was loaded successfully
    if image is None:
        print(f"Error: Unable to load image '{image_path_full}'")
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

        # Save the cropped image
        output_path = f"{image_path.split('.')[0]}_{area_name}.png"
        cv2.imwrite(output_path, cropped_image)
        print(f"Saved cropped image: {output_path}")

# Process each image
for image_path in image_paths:
    crop_and_save_images(image_path, crop_areas_percent)