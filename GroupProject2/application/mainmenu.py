import os
import sys
import tkinter as tk
import subprocess

# Determine the path to the "wordle.py" script based on the executable's location
if getattr(sys, 'frozen', False):
    # Running as a PyInstaller executable
    script_dir = os.path.dirname(sys.executable)
else:
    # Running as a script
    script_dir = os.path.dirname(__file__)

wordle_path = os.path.join(script_dir, "wordle.py")

def run_wordle():
    subprocess.run([sys.executable, wordle_path])

root = tk.Tk()
root.title("Wordle Runner")
root.geometry("400x400")

button = tk.Button(root, text="Run Wordle", command=run_wordle)
button.pack(padx=20, pady=20)

root.mainloop()
