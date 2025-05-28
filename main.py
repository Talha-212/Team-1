import tkinter as tk
from ui import TypingSpeedApp

print("Starting main.py")

if __name__ == "__main__":
    root = tk.Tk()
    print("Tkinter root created")
    app = TypingSpeedApp(root)
    print("TypingSpeedApp instance created")
    root.mainloop()
    print("Tkinter mainloop exited")
