import os
import sys
import pystray
import pyautogui
import time
import threading
import webbrowser
import random
import platform
import signal

from pystray import MenuItem as item
from PIL import Image

# Flag to keep track of whether the system is being kept awake
active = True

# Define the lock file path
lockfile_path = "/tmp/nodoze.lock"

def icon_image():
    # Use the correct path whether running as an executable or from source
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return Image.open(os.path.join(base_path, "assets/icon.ico"))

def keep_awake():
    while True:
        if active:
            # Simulate pressing the Shift key to keep the system awake
            pyautogui.press('shift')
        
        # Generate a random sleep time between 3 and 8 minutes (in seconds)
        sleep_time = random.randint(180, 480)
        
        # Sleep for the randomly generated duration
        time.sleep(sleep_time)

def toggle_status(icon, _):
    global active
    active = not active

    # Dynamically update the system tray menu to reflect the current status and toggle option
    icon.menu = pystray.Menu(
        item("Active" if active else "Inactive", lambda _: None, checked=lambda item: active),  # Use checkmark and dynamic label
        pystray.Menu.SEPARATOR,  # Separator between status and the other items
        item("Turn Off" if active else "Turn On", toggle_status),
        item('About', show_about),
        item('Exit', on_quit)
    )

def show_about(icon, item):
    # Open the NoDoze website when the "About" menu item is clicked
    webbrowser.open("https://getnodoze.com")

def on_quit(icon, item):
    # Stop the system tray icon and quit the application
    icon.stop()

def setup_system_tray():
    # Create the system tray icon using the provided icon image
    icon = pystray.Icon("NoDoze", icon_image())

    # Create the system tray menu with the status item, separator, toggle, "About," and "Exit"
    menu = pystray.Menu(
        item("Active" if active else "Inactive", lambda _: None, checked=lambda item: active),  # Use checkmark and dynamic label
        pystray.Menu.SEPARATOR,  # Separator between status and the rest
        item("Turn Off" if active else "Turn On", toggle_status),
        item('About', show_about),
        item('Exit', on_quit)
    )
    
    # Assign the menu to the system tray icon
    icon.menu = menu

    # Run the keep_awake function in a separate thread
    threading.Thread(target=keep_awake, daemon=True).start()

    # Start the system tray icon
    icon.run()

def check_single_instance():
    if os.path.exists(lockfile_path):
        # Read the PID from the lock file
        with open(lockfile_path, 'r') as f:
            pid = int(f.read())
        
        try:
            # Check if the process is still running
            os.kill(pid, 0)
            print(f"NoDoze is already running with PID {pid}. Exiting this instance.")
            sys.exit(0)
        except OSError:
            # Process does not exist, proceed with starting a new instance
            pass

    # Write the current PID to the lock file
    with open(lockfile_path, 'w') as f:
        f.write(str(os.getpid()))

def remove_lockfile():
    # Remove the lock file on exit
    if os.path.exists(lockfile_path):
        os.remove(lockfile_path)

if __name__ == "__main__":
    # Check if we are on Windows and apply mutex for single instance
    if platform.system() == "Windows":
        # Use Windows-specific mutex method
        import win32event
        import win32api
        import winerror

        # Try to create a named mutex
        handle = win32event.CreateMutex(None, False, "NoDozeMutex")

        # Check if another instance is running
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            print("NoDoze is already running. Exiting this instance.")
            sys.exit(0)  # Exit if the mutex already exists (another instance is running)
    
    # Check if we are on macOS or Linux and apply single instance lock via file
    elif platform.system() == "Darwin" or platform.system() == "Linux":
        check_single_instance()
        # Ensure lockfile is removed on exit
        signal.signal(signal.SIGTERM, lambda signum, frame: remove_lockfile())
        signal.signal(signal.SIGINT, lambda signum, frame: remove_lockfile())
        atexit.register(remove_lockfile)

    # Start the tray setup
    setup_system_tray()
