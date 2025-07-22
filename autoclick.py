import tkinter as tk
from tkinter import messagebox
import pyautogui
import threading
import time
import keyboard

clicking = False
click_thread = None

def click_loop(interval):
    global clicking
    while clicking:
        pyautogui.click()
        time.sleep(interval)

def start_clicking():
    global clicking, click_thread

    try:
        interval_ms = int(interval_entry.get())
        interval = interval_ms / 1000.0
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number for interval (ms).")
        return

    if not clicking:
        clicking = True
        click_thread = threading.Thread(target=click_loop, args=(interval,), daemon=True)
        click_thread.start()

def stop_clicking():
    global clicking
    clicking = False

def toggle_clicking():
    if clicking:
        stop_clicking()
    else:
        start_clicking()

def on_close():
    stop_clicking()
    root.destroy()

# GUI setup
root = tk.Tk()
root.title("Autoclicker")
root.geometry("250x180")
root.resizable(False, False)

interval_label = tk.Label(root, text="Click interval (ms):")
interval_label.pack(pady=(10, 0))

interval_entry = tk.Entry(root)
interval_entry.insert(0, "100")
interval_entry.pack(pady=(0, 10))

start_button = tk.Button(root, text="Start", bg="green", fg="white", command=start_clicking)
start_button.pack(pady=(0, 5))

stop_button = tk.Button(root, text="Stop", bg="red", fg="white", command=stop_clicking)
stop_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=on_close)
exit_button.pack(pady=(5, 10))

hotkey_label = tk.Label(root, text="Press F6 to Start/Stop", fg="black")
hotkey_label.pack()

# Register F6 hotkey
def listen_hotkey():
    keyboard.add_hotkey('F6', toggle_clicking)
    keyboard.wait('esc')  # keep thread alive until Esc is pressed

hotkey_thread = threading.Thread(target=listen_hotkey, daemon=True)
hotkey_thread.start()

# Safe closing
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
