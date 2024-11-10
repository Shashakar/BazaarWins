from PIL import Image

from trainingDataGenSingle import training_folder

image_name="G"
img = Image.open(training_folder + "/characters/" + image_name + ".tif")
img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
img.save("your_image_scaled.png")