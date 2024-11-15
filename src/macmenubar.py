import rumps
import threading

# Import your workflow or scraping logic
from bazaar_scraper import looper

def start_mac_menu_bar():
    class BazaarApp(rumps.App):
        def __init__(self):
            super(BazaarApp, self).__init__("Bazaar Scraper")
            self.menu = ["Start Watching", "Stop Watching"]

        @rumps.clicked("Start Watching")
        def start_watching(self, _):
            rumps.notification("Bazaar Scraper", "Status", "Started Watching Wins Screen", sound=True)
            self.scraper_thread = threading.Thread(target=looper, daemon=True)
            self.scraper_thread.start()

        @rumps.clicked("Stop Watching")
        def stop_watching(self, _):
            rumps.notification("Bazaar Scraper", "Status", "Stopping Watching Wins Screen", sound=True)
            # You can add logic to stop the workflow if needed

    BazaarApp().run()