import cv2

image_name = "6winsbronzevictory_raidus"

# Load the image in grayscale
image = cv2.imread(f"./training_images/{image_name}.png", cv2.IMREAD_GRAYSCALE)

# Apply thresholding to binarize the image
_, thresh = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

# Find contours, which will give us the bounding boxes
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw bounding boxes and print coordinates
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    print(f"Character bounding box: X={x}, Y={y}, Width={w}, Height={h}")
    # Draw rectangle on the original image (optional, for visualization)
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1)

# Save or display the image with bounding boxes for verification
cv2.imwrite("output_with_bounding_boxes.png", image)