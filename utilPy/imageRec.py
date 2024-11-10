from PIL import Image, ImageEnhance, ImageOps
import pytesseract

# Load the image
image_path = '../training_images/game_examples/10winsvictory.png'  # Update with the actual path

# Load the original image
image = Image.open(image_path)

# Step 1: Convert to Grayscale
gray_image = image.convert('L')

# Step 2: Apply Thresholding (keep it as a grayscale image after thresholding)
bw_image = gray_image.point(lambda x: 0 if x < 150 else 255, 'L')  # 'L' mode keeps it grayscale, not binary

# Step 3: Resize the Image to Enhance OCR Accuracy
large_image = bw_image.resize((image.width * 2, image.height * 2), Image.LANCZOS)

# Step 4: Crop to Top Half of the Image
width, height = large_image.size
top_half = large_image.crop((0, 0, width, height // 2))

# Step 5: Enhance Contrast and Sharpen the Image
# Note: We are now enhancing the grayscale 'L' image (not binary)
enhancer = ImageEnhance.Contrast(top_half)
top_half_contrasted = enhancer.enhance(2)  # Increase contrast

enhancer = ImageEnhance.Sharpness(top_half_contrasted)
top_half_sharpened = enhancer.enhance(2)  # Sharpen image

# Optional Step: Crop a Smaller Region around "10 Wins" Text
small_roi = top_half_sharpened.crop((0, height // 12, width // 2, height // 4))

# Step 6: Try Inverting the Image for Better OCR (if text is lighter than background)
inverted_image = ImageOps.invert(small_roi.convert("L"))

inverted_image.show()
# Step 7: Run OCR with Tesseract on Processed Image
custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
text = pytesseract.image_to_string(inverted_image, config=custom_config)

# Print extracted text to verify
print("Extracted Text:", text)

# Search for the number of wins (e.g., "10 WINS" in the text)
import re
matches = re.search(r'(\d+)\s+WINS', text, re.IGNORECASE)
if matches:
    wins = matches.group(1)
    print("Number of Wins:", wins)
else:
    print("Number of Wins not found")