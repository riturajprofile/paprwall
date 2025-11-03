"""
Modern Desktop Wallpaper Manager GUI Application
Features: URL/Local image setting, history with thumbnails, cross-platform support
"""

import os
import sys
import json
import platform
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import requests


class WallpaperManagerGUI:
    """Main GUI application for wallpaper management."""
    
    def __init__(self, root):
        """Initialize the wallpaper manager GUI."""
        self.root = root
        self.root.title("Wallpaper Manager")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Setup data directory
        self.data_dir = Path.home() / ".paprwall"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.data_dir / "history.json"
        self.wallpapers_dir = self.data_dir / "wallpapers"
        self.wallpapers_dir.mkdir(exist_ok=True)
        
        # Load history
        self.history = self.load_history()
        
        # Track current preview
        self.preview_image_path = None
        self.preview_photo = None
        
        # Setup UI
        self.setup_ui()
        
        # Load current wallpaper
        self.refresh_display()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🖼️ Wallpaper Manager", 
            font=("Helvetica", 20, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # === Input Section ===
        input_frame = ttk.LabelFrame(main_frame, text="Set Wallpaper", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # URL input
        ttk.Label(input_frame, text="Image URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(input_frame, width=50)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.url_entry.bind('<Return>', lambda e: self.fetch_from_url())
        
        ttk.Button(
            input_frame, 
            text="Fetch & Preview", 
            command=self.fetch_from_url
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Local file input
        ttk.Label(input_frame, text="Local File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.file_entry = ttk.Entry(input_frame, width=50)
        self.file_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Button(
            input_frame, 
            text="Browse", 
            command=self.browse_file
        ).grid(row=1, column=2, padx=5, pady=5)
        
        # === Preview Section ===
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(
            preview_frame, 
            bg="#2c3e50", 
            height=300,
            highlightthickness=1,
            highlightbackground="#34495e"
        )
        self.preview_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Preview info label
        self.preview_info = ttk.Label(
            preview_frame, 
            text="No image loaded", 
            foreground="gray"
        )
        self.preview_info.grid(row=1, column=0, pady=(5, 0))
        
        # Action buttons
        button_frame = ttk.Frame(preview_frame)
        button_frame.grid(row=2, column=0, pady=(10, 0))
        
        self.set_button = ttk.Button(
            button_frame,
            text="✓ Set as Wallpaper",
            command=self.set_wallpaper,
            state=tk.DISABLED
        )
        self.set_button.pack(side=tk.LEFT, padx=5)
        
        # Progress bar (hidden by default)
        self.progress = ttk.Progressbar(
            preview_frame, 
            mode='indeterminate', 
            length=200
        )
        
        # === History Section ===
        history_frame = ttk.LabelFrame(main_frame, text="Recent Wallpapers", padding="10")
        history_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        history_frame.columnconfigure(0, weight=1)
        
        # History buttons
        history_button_frame = ttk.Frame(history_frame)
        history_button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(
            history_button_frame,
            text="🔄 Refresh",
            command=self.refresh_display
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            history_button_frame,
            text="🗑️ Clear History",
            command=self.clear_history
        ).pack(side=tk.LEFT, padx=5)
        
        # History thumbnails container
        self.history_container = ttk.Frame(history_frame)
        self.history_container.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # === Current Wallpaper Section ===
        current_frame = ttk.LabelFrame(main_frame, text="Current Wallpaper", padding="10")
        current_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))
        
        self.current_label = ttk.Label(
            current_frame, 
            text="Loading...", 
            wraplength=800
        )
        self.current_label.pack()
        
        # Status bar
        self.status_bar = ttk.Label(
            main_frame, 
            text="Ready", 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def load_history(self):
        """Load wallpaper history from JSON file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")
                return []
        return []
    
    def save_history(self):
        """Save wallpaper history to JSON file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def update_status(self, message):
        """Update the status bar."""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def fetch_from_url(self):
        """Fetch image from URL with progress indicator."""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("Input Required", "Please enter an image URL")
            return
        
        # Validate URL format
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ValueError("Invalid URL format")
        except Exception:
            messagebox.showerror("Invalid URL", "Please enter a valid URL")
            return
        
        # Show progress
        self.progress.grid(row=3, column=0, pady=10)
        self.progress.start()
        self.update_status("Downloading image...")
        
        # Download in thread to keep GUI responsive
        def download():
            try:
                response = requests.get(url, timeout=30, stream=True)
                response.raise_for_status()
                
                # Check if it's an image
                content_type = response.headers.get('content-type', '')
                if 'image' not in content_type.lower():
                    raise ValueError("URL does not point to an image")
                
                # Save to wallpapers directory
                filename = f"wallpaper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                temp_path = self.wallpapers_dir / filename
                
                with open(temp_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Update UI in main thread
                self.root.after(0, lambda: self.on_download_complete(str(temp_path), url))
                
            except requests.exceptions.RequestException as e:
                self.root.after(0, lambda: self.on_download_error(f"Download failed: {str(e)}"))
            except Exception as e:
                self.root.after(0, lambda: self.on_download_error(f"Error: {str(e)}"))
        
        threading.Thread(target=download, daemon=True).start()
    
    def on_download_complete(self, image_path, source_url):
        """Handle successful download."""
        self.progress.stop()
        self.progress.grid_remove()
        self.preview_image_path = image_path
        self.display_preview(image_path, f"From URL: {source_url}")
        self.update_status("Image downloaded successfully")
    
    def on_download_error(self, error_message):
        """Handle download error."""
        self.progress.stop()
        self.progress.grid_remove()
        messagebox.showerror("Download Error", error_message)
        self.update_status("Download failed")
    
    def browse_file(self):
        """Browse for local image file."""
        filetypes = (
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("All files", "*.*")
        )
        
        filename = filedialog.askopenfilename(
            title="Select Wallpaper Image",
            filetypes=filetypes
        )
        
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
            self.preview_image_path = filename
            self.display_preview(filename, f"Local file: {os.path.basename(filename)}")
    
    def display_preview(self, image_path, info_text):
        """Display image preview in canvas."""
        try:
            # Open and resize image
            img = Image.open(image_path)
            
            # Calculate size to fit in canvas (maintain aspect ratio)
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            # Use default size if canvas not yet rendered
            if canvas_width <= 1:
                canvas_width = 800
            if canvas_height <= 1:
                canvas_height = 300
            
            img.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.preview_photo = ImageTk.PhotoImage(img)
            
            # Clear canvas and display image
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                image=self.preview_photo,
                anchor=tk.CENTER
            )
            
            # Update info
            self.preview_info.config(
                text=f"{info_text}\nSize: {img.width}x{img.height}",
                foreground="black"
            )
            
            # Enable set button
            self.set_button.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Preview Error", f"Could not load image: {str(e)}")
    
    def set_wallpaper(self):
        """Set the previewed image as wallpaper."""
        if not self.preview_image_path:
            messagebox.showwarning("No Image", "Please select an image first")
            return
        
        try:
            # Convert to absolute path
            image_path = os.path.abspath(self.preview_image_path)
            
            # Set wallpaper based on platform
            success = self.set_wallpaper_platform(image_path)
            
            if success:
                # Add to history
                self.add_to_history(image_path)
                
                # Refresh display
                self.refresh_display()
                
                messagebox.showinfo("Success", "Wallpaper set successfully!")
                self.update_status(f"Wallpaper set: {os.path.basename(image_path)}")
            else:
                messagebox.showerror("Error", "Failed to set wallpaper")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set wallpaper: {str(e)}")
    
    def set_wallpaper_platform(self, image_path):
        """Set wallpaper based on platform."""
        system = platform.system()
        
        try:
            if system == "Windows":
                import ctypes
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
                return True
                
            elif system == "Darwin":  # macOS
                script = f'''
                tell application "System Events"
                    tell every desktop
                        set picture to "{image_path}"
                    end tell
                end tell
                '''
                subprocess.run(["osascript", "-e", script], check=True)
                return True
                
            elif system == "Linux":
                # Try different Linux desktop environments
                desktop = os.environ.get('DESKTOP_SESSION', '').lower()
                success = False
                
                # Try gsettings first (GNOME/Unity/others)
                try:
                    subprocess.run([
                        "gsettings", "set",
                        "org.gnome.desktop.background", "picture-uri",
                        f"file://{image_path}"
                    ], check=True, capture_output=True)
                    subprocess.run([
                        "gsettings", "set",
                        "org.gnome.desktop.background", "picture-uri-dark",
                        f"file://{image_path}"
                    ], check=True, capture_output=True)
                    success = True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass
                
                # If gsettings worked, return success
                if success:
                    return True
                
                # GNOME (fallback)
                if 'gnome' in desktop or os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                    subprocess.run([
                        "gsettings", "set",
                        "org.gnome.desktop.background", "picture-uri",
                        f"file://{image_path}"
                    ], check=True)
                    subprocess.run([
                        "gsettings", "set",
                        "org.gnome.desktop.background", "picture-uri-dark",
                        f"file://{image_path}"
                    ], check=True)
                    return True
                
                # KDE Plasma
                elif 'kde' in desktop or 'plasma' in desktop:
                    script = f'''
                    qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript '
                        var allDesktops = desktops();
                        for (i=0;i<allDesktops.length;i++) {{
                            d = allDesktops[i];
                            d.wallpaperPlugin = "org.kde.image";
                            d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                            d.writeConfig("Image", "file://{image_path}");
                        }}
                    '
                    '''
                    subprocess.run(script, shell=True, check=True)
                    return True
                
                # XFCE
                elif 'xfce' in desktop:
                    subprocess.run([
                        "xfconf-query", "-c", "xfce4-desktop",
                        "-p", "/backdrop/screen0/monitor0/workspace0/last-image",
                        "-s", image_path
                    ], check=True)
                    return True
                
                # Fallback: try feh (works for many window managers)
                else:
                    subprocess.run(["feh", "--bg-scale", image_path], check=True)
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error setting wallpaper: {e}")
            return False
    
    def add_to_history(self, image_path):
        """Add image to history."""
        entry = {
            "path": image_path,
            "timestamp": datetime.now().isoformat(),
            "filename": os.path.basename(image_path)
        }
        
        # Remove if already in history
        self.history = [h for h in self.history if h.get("path") != image_path]
        
        # Add to front
        self.history.insert(0, entry)
        
        # Keep only last 5
        self.history = self.history[:5]
        
        # Save
        self.save_history()
    
    def refresh_display(self):
        """Refresh the history and current wallpaper display."""
        self.load_history()
        self.display_history()
        self.display_current_wallpaper()
    
    def display_history(self):
        """Display history thumbnails."""
        # Clear existing thumbnails
        for widget in self.history_container.winfo_children():
            widget.destroy()
        
        if not self.history:
            ttk.Label(
                self.history_container,
                text="No history yet",
                foreground="gray"
            ).pack()
            return
        
        # Create thumbnail frame for each history item
        for idx, item in enumerate(self.history):
            self.create_history_thumbnail(item, idx)
    
    def create_history_thumbnail(self, item, index):
        """Create a thumbnail widget for a history item."""
        frame = ttk.Frame(self.history_container, relief=tk.RIDGE, borderwidth=1)
        frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        try:
            # Load and create thumbnail
            img = Image.open(item["path"])
            img.thumbnail((120, 80), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # Keep reference to prevent garbage collection
            label = ttk.Label(frame, image=photo)
            label.image = photo
            label.pack()
            
            # Make clickable
            label.bind("<Button-1>", lambda e, path=item["path"]: self.set_from_history(path))
            label.bind("<Enter>", lambda e: label.config(cursor="hand2"))
            
            # Info label
            info = f"#{index + 1}\n{item['filename'][:15]}..."
            info_label = ttk.Label(frame, text=info, font=("Helvetica", 8))
            info_label.pack()
            
        except Exception as e:
            ttk.Label(
                frame,
                text=f"Error\nloading\n#{index + 1}",
                foreground="red"
            ).pack()
    
    def set_from_history(self, image_path):
        """Set wallpaper from history."""
        if os.path.exists(image_path):
            self.preview_image_path = image_path
            self.display_preview(image_path, f"From history: {os.path.basename(image_path)}")
            self.set_wallpaper()
        else:
            messagebox.showerror("Error", f"Image file not found:\n{image_path}")
    
    def display_current_wallpaper(self):
        """Display current wallpaper info."""
        if self.history:
            current = self.history[0]
            text = f"📁 {current['filename']}\n🕒 {current['timestamp'][:19]}\n📍 {current['path']}"
            self.current_label.config(text=text)
        else:
            self.current_label.config(text="No wallpaper set yet")
    
    def clear_history(self):
        """Clear wallpaper history."""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the history?"):
            self.history = []
            self.save_history()
            self.refresh_display()
            self.update_status("History cleared")


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = WallpaperManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
