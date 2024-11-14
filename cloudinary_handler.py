import cloudinary
import cloudinary.uploader
import cloudinary.api
import psycopg2
import logging
from logging_bazaar import setup_logging

baz_cloud_sec = "yviIqpj0xQzlqw3uS5c8UNZxN-g"
baz_cloud_key = "229145455462343"
baz_cloud_name = "dv1frpfty"
baz_cloud_env = "CLOUDINARY_URL=cloudinary://229145455462343:yviIqpj0xQzlqw3uS5c8UNZxN-g@dv1frpfty"


# Set up logging
logger = setup_logging(logging.DEBUG, "CloudinaryUploader")

# Configure Cloudinary with your credentials
cloudinary.config(
    cloud_name=baz_cloud_name,
    api_key=baz_cloud_key,
    api_secret=baz_cloud_sec
)

# Function to upload image to Cloudinary
def upload_image_to_cloudinary(image_path):
    try:
        response = cloudinary.uploader.upload(image_path)
        # The response contains the URL of the uploaded image
        image_url = response.get('secure_url')
        if image_url:
            logger.info(f"Image uploaded successfully. URL: {image_url}")
            return image_url
        else:
            logger.error("Failed to upload image to Cloudinary.")
            return None
    except Exception as e:
        logger.error(f"An error occurred while uploading to Cloudinary: {str(e)}")
        return None


# Example usage
if __name__ == "__main__":
    image_path = "example_image.png"  # Replace with the path to your image
    image_name = "example_image"  # Replace with a unique identifier for the image

    # Upload image to Cloudinary and store the URL in the PostgreSQL database
    image_url = upload_image_to_cloudinary(image_path)