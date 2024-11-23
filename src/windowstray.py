import os
import time
import threading
import logging
import tkinter as tk
from tkinter import scrolledtext
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from watcher import load_template_image, watch_for_wins_screen

# Set up logging
logger = logging.getLogger('WindowsTray')
show_notifications = True
icon: Icon

def create_image():
    # Create an icon image for the system tray
    image = Image.new('RGB', (64, 64), 'white')
    dc = ImageDraw.Draw(image)
    dc.rectangle((8, 8, 56, 56), fill='white', outline='black')
    return image

def show_console():
    root = tk.Tk()
    root.title("Console Output")
    console = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
    console.pack()
    root.mainloop()

def start_watcher():
    watcher_thread = threading.Thread(target=watch_for_wins_screen)
    watcher_thread.daemon = True
    watcher_thread.start()

def on_quit(icon, item):
    icon.stop()
    os._exit(0)

def setup(icon):
    icon.visible = True
    icon.notify('Bazaar Scraper is now running in the system tray.')

def start_tray_icon():
    global show_notifications, icon
    menu = Menu(
        #MenuItem('Show Console', lambda: threading.Thread(target=show_console).start()),
        MenuItem(lambda text: f'Show Notifications: {show_notifications}', lambda: toggle_notifications()),
        MenuItem('Quit', on_quit)
    )
    icon = Icon('Bazaar Scraper', create_image(), menu=menu)
    icon.run(setup)

def toggle_notifications():
    global show_notifications
    show_notifications = not show_notifications

def notify_user(message):
    global icon
    try:
        if show_notifications:
            icon.notify(message)
    except NameError as ne:
        logger.debug(f"Error occurred while trying to notify user: {ne}")
    except Exception as e:
        logger.error(f"An error occurred while trying to notify user: {e}")


if __name__ == "__main__":
    template_path = os.path.join(".", "templates", 'windows_wins_template.png')
    template = load_template_image(template_path)

    if template is None:
        logger.error("Template image could not be loaded. Exiting program.")
    else:
        logger.info("Starting to watch for the WINS screen while 'The Bazaar' is active...")
        start_watcher()
        tray_thread = threading.Thread(target=start_tray_icon, daemon=True)
        tray_thread.start()

        # Keep the main thread alive
        while True:
            time.sleep(1)