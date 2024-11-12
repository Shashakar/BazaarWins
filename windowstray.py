from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading

def create_image():
    # Create an icon image for the system tray
    image = Image.new('RGB', (64, 64), color1 := 'white')
    dc = ImageDraw.Draw(image)
    dc.rectangle((8, 8, 56, 56), fill=color1, outline='black')
    return image

def setup(icon):
    # Logic for what happens when the tray icon is set up
    icon.visible = True

def on_quit(icon, item):
    # Logic for quitting the script
    icon.stop()  # Stops the icon and subsequently exits the script

def start_tray_icon():
    # Create the menu and the tray icon
    menu = Menu(MenuItem('Quit', on_quit))
    icon = Icon('Bazaar Scraper', create_image(), menu=menu)
    icon.run(setup)

# Run the tray icon in a separate thread
tray_thread = threading.Thread(target=start_tray_icon, daemon=True)
tray_thread.start()
