import threading
import time
import tkinter as tk
import queue
from queue import Empty
import pygetwindow as gw

def show_overlay(queue):
    # Get the Bazaar window
    bazaar_window = gw.getWindowsWithTitle('The Bazaar')[0]

    overlay = tk.Tk()
    overlay.title("Overlay")
    overlay.attributes("-alpha", 0.85)  # Set transparency level
    overlay.configure(bg='gray')

    label = tk.Label(overlay, text="Grabbing stats, please wait", font=("Helvetica", 16), bg='gray', fg='white')
    label.pack(expand=True)

    close_button = tk.Button(overlay, text="X", command=overlay.destroy, bg='red', fg='white')
    close_button.place(relx=1.0, rely=0.0, anchor='ne')

    overlay.overrideredirect(True)  # Remove window decorations
    overlay.lift()  # Bring the window to the front
    overlay.attributes("-topmost", True)  # Keep the window on top

    def update_position():
        overlay.deiconify()
        x, y, width, height = bazaar_window.left, bazaar_window.top, bazaar_window.width, bazaar_window.height
        overlay_height = height // 7
        overlay_y = y + (height - overlay_height)
        overlay.geometry(f"{width}x{overlay_height}+{x}+{overlay_y}")
        overlay.after(100, update_position)

    def check_queue():
        try:
            if queue.get_nowait() == "close":
                overlay.destroy()
        except Empty:
            overlay.after(100, check_queue)

    overlay.after(100, update_position)
    overlay.after(100, check_queue)
    overlay.mainloop()

def hide_overlay(queue):
    queue.put("close")

def start_overlay_thread():
    q = queue.Queue()
    o_thread = threading.Thread(target=show_overlay, args=(q,), daemon=True)
    o_thread.start()

    return q

if __name__ == "__main__":
    q = start_overlay_thread()

    # Simulate grabbing stats
    time.sleep(5)
    hide_overlay(q)