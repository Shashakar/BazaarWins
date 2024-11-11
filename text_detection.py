import easyocr
import os

def handle_full_screenshot(path):
    # for each png in game_examples, print the detected text and confidence
    for directories in os.walk("./training_images/game_examples"):
        for file in directories[2]:
            if file[-4:] != ".png":
                continue
            result = get_text_from_image(path)
            for detection in result:
             print(f"Detected text: {detection[1]}, with confidence: {detection[2]}")

def get_text_from_image(image_path):
    reader = easyocr.Reader(['en'])  # Specify the languages to use
    result = reader.readtext(image_path)
    return result

def get_user_and_title_from_image(image_path):
    result = get_text_from_image(image_path)
    title = result[0][1]
    print("Title: ", title)
    user = result[1][1]
    print("User: ", user)
    return title, user

def get_wins_from_image(image_path):
    result = get_text_from_image(image_path)
    wins_text = result[2][1]
    return wins_text
