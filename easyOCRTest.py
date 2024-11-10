import easyocr

path = "./training_images/game_examples/6winsbronzevictory_raidus.png"
reader = easyocr.Reader(['en'])  # Specify the languages to use
result = reader.readtext(path)

for detection in result:
    print(f"Detected text: {detection[1]}, with confidence: {detection[2]}")