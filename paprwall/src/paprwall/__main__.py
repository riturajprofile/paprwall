import sys
from paprwall.gui.wallpaper_manager_gui import ModernWallpaperGUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = ModernWallpaperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()