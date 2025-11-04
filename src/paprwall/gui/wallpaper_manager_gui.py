"""
Modern Desktop Wallpaper Manager GUI Application - Web-Inspired Design
Features: Large preview area, compact sidebar controls, countdown timer, auto-fetch
"""

import os
import sys
import json
import platform
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import requests


class WallpaperManagerGUI:
    """Main GUI application for wallpaper management with web-inspired design."""
    
    def __init__(self, root):
        """Initialize the wallpaper manager GUI."""
        self.root = root
        self.root.title("Wallpaper Manager")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        
        # Modern color scheme
        self.colors = {
            'bg': '#f5f5f5',
            'sidebar': '#ffffff',
            'preview_bg': '#1a1a1a',
            'accent': '#007bff',
            'text': '#333333',
            'border': '#e0e0e0'
        }
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
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
        
        # Timer state for auto-rotation
        self.auto_rotate_enabled = False
        self.rotation_interval_minutes = 60  # Default 60 minutes
        self.time_remaining_seconds = 0
        self.timer_thread = None
        self.stop_timer_flag = False
        
        # Setup UI
        self.setup_ui()
        
        # Load current wallpaper
        self.refresh_display()
    
    def setup_ui(self):
        """Setup the user interface with web-inspired layout."""
        # Main container - no padding for edge-to-edge design
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === TOP NAVBAR ===
        navbar = tk.Frame(main_frame, bg=self.colors['sidebar'], height=60)
        navbar.pack(side=tk.TOP, fill=tk.X)
        navbar.pack_propagate(False)
        
        # App title
        title_frame = tk.Frame(navbar, bg=self.colors['sidebar'])
        title_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(
            title_frame,
            text="🖼️",
            font=("Segoe UI", 20),
            bg=self.colors['sidebar']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            title_frame,
            text="Wallpaper Manager",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['sidebar'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Status in navbar
        self.status_label = tk.Label(
            navbar,
            text="● Ready",
            font=("Segoe UI", 10),
            bg=self.colors['sidebar'],
            fg='#28a745'
        )
        self.status_label.pack(side=tk.RIGHT, padx=20)
        
        # === CONTENT AREA ===
        content = tk.Frame(main_frame, bg=self.colors['bg'])
        content.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # === RIGHT SIDEBAR (Fixed width) ===
        sidebar = tk.Frame(content, bg=self.colors['sidebar'], width=350)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 10), pady=10)
        sidebar.pack_propagate(False)
        
        # Sidebar scrollable content
        sidebar_canvas = tk.Canvas(sidebar, bg=self.colors['sidebar'], highlightthickness=0)
        sidebar_scrollbar = ttk.Scrollbar(sidebar, orient=tk.VERTICAL, command=sidebar_canvas.yview)
        sidebar_content = tk.Frame(sidebar_canvas, bg=self.colors['sidebar'])
        
        sidebar_content.bind(
            "<Configure>",
            lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
        )
        
        sidebar_canvas.create_window((0, 0), window=sidebar_content, anchor=tk.NW)
        sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)
        
        sidebar_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        sidebar_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # === SIDEBAR SECTIONS ===
        
        # Source section
        self.create_section_header(sidebar_content, "🌐 Image Source")
        
        source_frame = tk.Frame(sidebar_content, bg=self.colors['sidebar'])
        source_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # URL input
        tk.Label(
            source_frame,
            text="URL",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['sidebar'],
            fg=self.colors['text']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        url_container = tk.Frame(source_frame, bg=self.colors['sidebar'])
        url_container.pack(fill=tk.X, pady=(0, 10))
        
        self.url_entry = tk.Entry(
            url_container,
            font=("Segoe UI", 10),
            relief=tk.SOLID,
            borderwidth=1,
            bg='white'
        )
        self.url_entry.pack(fill=tk.X, pady=(0, 8))
        self.url_entry.insert(0, "https://picsum.photos/1920/1080")
        self.url_entry.bind('<Return>', lambda e: self.fetch_from_url())
        
        self.fetch_btn = tk.Button(
            url_container,
            text="Fetch & Preview",
            command=self.fetch_from_url,
            bg=self.colors['accent'],
            fg='white',
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8
        )
        self.fetch_btn.pack(fill=tk.X)
        
        # Auto Fetch button
        self.auto_fetch_btn = tk.Button(
            url_container,
            text="🔄 Auto Fetch (Sync)",
            command=self.auto_fetch_and_set,
            bg='#28a745',
            fg='white',
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8
        )
        self.auto_fetch_btn.pack(fill=tk.X, pady=(5, 0))
        
        # Divider
        tk.Frame(source_frame, bg=self.colors['border'], height=1).pack(fill=tk.X, pady=15)
        
        # Local file
        tk.Label(
            source_frame,
            text="Local File",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['sidebar'],
            fg=self.colors['text']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        file_container = tk.Frame(source_frame, bg=self.colors['sidebar'])
        file_container.pack(fill=tk.X)
        
        self.file_entry = tk.Entry(
            file_container,
            font=("Segoe UI", 9),
            relief=tk.SOLID,
            borderwidth=1,
            bg='white'
        )
        self.file_entry.pack(fill=tk.X, pady=(0, 8))
        
        tk.Button(
            file_container,
            text="📁 Browse Files",
            command=self.browse_file,
            bg='white',
            fg=self.colors['text'],
            font=("Segoe UI", 10),
            relief=tk.SOLID,
            borderwidth=1,
            cursor="hand2",
            padx=20,
            pady=8
        ).pack(fill=tk.X)
        
        # Preview Info section
        self.create_section_header(sidebar_content, "ℹ️ Preview Info")
        
        info_frame = tk.Frame(sidebar_content, bg=self.colors['sidebar'])
        info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.preview_info_text = tk.Text(
            info_frame,
            height=4,
            font=("Segoe UI", 9),
            relief=tk.SOLID,
            borderwidth=1,
            bg='#f8f9fa',
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.preview_info_text.pack(fill=tk.X)
        self.preview_info_text.insert(1.0, "No image loaded\nUse URL or browse local files")
        self.preview_info_text.config(state=tk.DISABLED)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            info_frame,
            mode='indeterminate',
            length=200
        )
        
        # Action button
        self.set_button = tk.Button(
            sidebar_content,
            text="✓ Set as Wallpaper",
            command=self.set_wallpaper,
            state=tk.DISABLED,
            bg='#28a745',
            fg='white',
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=12
        )
        self.set_button.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Auto-Rotation section
        self.create_section_header(sidebar_content, "⏱️ Auto-Rotation")
        
        rotation_frame = tk.Frame(sidebar_content, bg=self.colors['sidebar'])
        rotation_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Timer display
        timer_display = tk.Frame(rotation_frame, bg='#f8f9fa', relief=tk.SOLID, borderwidth=1)
        timer_display.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            timer_display,
            text="Next change in:",
            font=("Segoe UI", 9),
            bg='#f8f9fa',
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=10, pady=8)
        
        self.timer_label = tk.Label(
            timer_display,
            text="--:--",
            font=("Segoe UI", 14, "bold"),
            bg='#f8f9fa',
            fg=self.colors['accent']
        )
        self.timer_label.pack(side=tk.RIGHT, padx=10, pady=8)
        
        # Auto-rotate toggle
        toggle_frame = tk.Frame(rotation_frame, bg=self.colors['sidebar'])
        toggle_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.auto_rotate_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            toggle_frame,
            text="Enable Auto-Rotate",
            variable=self.auto_rotate_var,
            command=self.toggle_auto_rotate
        ).pack(side=tk.LEFT)
        
        # Interval setting
        interval_frame = tk.Frame(rotation_frame, bg=self.colors['sidebar'])
        interval_frame.pack(fill=tk.X)
        
        tk.Label(
            interval_frame,
            text="Interval (min):",
            font=("Segoe UI", 9),
            bg=self.colors['sidebar']
        ).pack(side=tk.LEFT)
        
        self.interval_entry = tk.Entry(
            interval_frame,
            font=("Segoe UI", 9),
            width=8,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.interval_entry.insert(0, "60")
        self.interval_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            interval_frame,
            text="Apply",
            command=self.apply_interval,
            bg='white',
            fg=self.colors['text'],
            font=("Segoe UI", 9),
            relief=tk.SOLID,
            borderwidth=1,
            cursor="hand2",
            padx=10,
            pady=2
        ).pack(side=tk.LEFT)
        
        # Current Wallpaper section
        self.create_section_header(sidebar_content, "✨ Current Wallpaper")
        
        current_frame = tk.Frame(sidebar_content, bg=self.colors['sidebar'])
        current_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.current_text = tk.Text(
            current_frame,
            height=6,
            font=("Segoe UI", 9),
            relief=tk.SOLID,
            borderwidth=1,
            bg='#f8f9fa',
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.current_text.pack(fill=tk.X)
        
        # History section
        self.create_section_header(sidebar_content, "🕐 Recent History")
        
        history_header = tk.Frame(sidebar_content, bg=self.colors['sidebar'])
        history_header.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        tk.Label(
            history_header,
            text="Click to reapply",
            font=("Segoe UI", 8),
            bg=self.colors['sidebar'],
            fg='gray'
        ).pack(side=tk.LEFT)
        
        tk.Button(
            history_header,
            text="Clear",
            command=self.clear_history,
            bg='white',
            fg='#dc3545',
            font=("Segoe UI", 8),
            relief=tk.FLAT,
            cursor="hand2",
            padx=8,
            pady=2
        ).pack(side=tk.RIGHT)
        
        # History thumbnails
        self.history_container = tk.Frame(sidebar_content, bg=self.colors['sidebar'])
        self.history_container.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # === LEFT SIDE: LARGE PREVIEW AREA ===
        preview_container = tk.Frame(content, bg=self.colors['preview_bg'])
        preview_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        
        # Preview header
        preview_header = tk.Frame(preview_container, bg=self.colors['preview_bg'])
        preview_header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            preview_header,
            text="Preview",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['preview_bg'],
            fg='white'
        ).pack(side=tk.LEFT)
        
        self.preview_size_label = tk.Label(
            preview_header,
            text="",
            font=("Segoe UI", 10),
            bg=self.colors['preview_bg'],
            fg='#999999'
        )
        self.preview_size_label.pack(side=tk.RIGHT)
        
        # Canvas for image
        canvas_container = tk.Frame(preview_container, bg=self.colors['preview_bg'])
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.preview_canvas = tk.Canvas(
            canvas_container,
            bg='#2a2a2a',
            highlightthickness=0
        )
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder text
        self.placeholder_id = self.preview_canvas.create_text(
            400, 300,
            text="🖼️\n\nNo Preview\n\nEnter a URL or browse a file to preview",
            font=("Segoe UI", 16),
            fill='#666666',
            justify=tk.CENTER
        )
    
    def create_section_header(self, parent, text):
        """Create a section header in sidebar."""
        frame = tk.Frame(parent, bg=self.colors['sidebar'])
        frame.pack(fill=tk.X, padx=20, pady=(10, 10))
        
        tk.Label(
            frame,
            text=text,
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['sidebar'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT)
        
        # Separator line
        sep_frame = tk.Frame(parent, bg=self.colors['sidebar'])
        sep_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        tk.Frame(sep_frame, bg=self.colors['border'], height=2).pack(fill=tk.X)
    
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
    
    def update_status(self, message, color='#28a745'):
        """Update the status bar."""
        self.status_label.config(text=f"● {message}", fg=color)
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
        self.progress.pack(pady=10)
        self.progress.start()
        self.update_status("Downloading...", '#007bff')
        self.fetch_btn.config(state=tk.DISABLED)
        
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
        self.progress.pack_forget()
        self.fetch_btn.config(state=tk.NORMAL)
        self.preview_image_path = image_path
        self.display_preview(image_path, f"URL: {source_url}")
        self.update_status("Downloaded successfully", '#28a745')
    
    def on_download_error(self, error_message):
        """Handle download error."""
        self.progress.stop()
        self.progress.pack_forget()
        self.fetch_btn.config(state=tk.NORMAL)
        messagebox.showerror("Download Error", error_message)
        self.update_status("Download failed", '#dc3545')
    
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
            self.display_preview(filename, f"Local: {os.path.basename(filename)}")
    
    def display_preview(self, image_path, info_text):
        """Display image preview in canvas."""
        try:
            # Open and resize image
            img = Image.open(image_path)
            original_size = f"{img.width} × {img.height}"
            
            # Calculate size to fit in canvas (maintain aspect ratio)
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            # Use default size if canvas not yet rendered
            if canvas_width <= 1:
                canvas_width = 800
            if canvas_height <= 1:
                canvas_height = 700
            
            # Remove placeholder
            if self.placeholder_id:
                self.preview_canvas.delete(self.placeholder_id)
                self.placeholder_id = None
            
            img.thumbnail((canvas_width - 40, canvas_height - 40), Image.Resampling.LANCZOS)
            
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
            self.preview_info_text.config(state=tk.NORMAL)
            self.preview_info_text.delete(1.0, tk.END)
            self.preview_info_text.insert(1.0, f"{info_text}\nResolution: {original_size} px")
            self.preview_info_text.config(state=tk.DISABLED)
            
            self.preview_size_label.config(text=original_size)
            
            # Enable set button
            self.set_button.config(state=tk.NORMAL)
            self.update_status("Preview loaded", '#28a745')
            
        except Exception as e:
            messagebox.showerror("Preview Error", f"Could not load image: {str(e)}")
            self.update_status("Preview failed", '#dc3545')
    
    def set_wallpaper(self):
        """Set the previewed image as wallpaper."""
        if not self.preview_image_path:
            messagebox.showwarning("No Image", "Please select an image first")
            return
        
        try:
            # Convert to absolute path
            image_path = os.path.abspath(self.preview_image_path)
            
            self.update_status("Setting wallpaper...", '#007bff')
            
            # Set wallpaper based on platform
            success = self.set_wallpaper_platform(image_path)
            
            if success:
                # Add to history
                self.add_to_history(image_path)
                
                # Refresh display
                self.refresh_display()
                
                messagebox.showinfo("Success", "Wallpaper set successfully!")
                self.update_status("Wallpaper applied", '#28a745')
            else:
                messagebox.showerror("Error", "Failed to set wallpaper")
                self.update_status("Failed", '#dc3545')
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set wallpaper: {str(e)}")
            self.update_status("Error occurred", '#dc3545')
    
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
                desktop = os.environ.get('DESKTOP_SESSION', '').lower()
                
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
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass
                
                if 'gnome' in desktop:
                    subprocess.run([
                        "gsettings", "set",
                        "org.gnome.desktop.background", "picture-uri",
                        f"file://{image_path}"
                    ], check=True)
                    return True
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
                elif 'xfce' in desktop:
                    subprocess.run([
                        "xfconf-query", "-c", "xfce4-desktop",
                        "-p", "/backdrop/screen0/monitor0/workspace0/last-image",
                        "-s", image_path
                    ], check=True)
                    return True
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
        
        self.history = [h for h in self.history if h.get("path") != image_path]
        self.history.insert(0, entry)
        self.history = self.history[:8]
        self.save_history()
    
    def refresh_display(self):
        """Refresh the history and current wallpaper display."""
        self.history = self.load_history()
        self.display_history()
        self.display_current_wallpaper()
    
    def display_history(self):
        """Display history thumbnails."""
        for widget in self.history_container.winfo_children():
            widget.destroy()
        
        if not self.history:
            tk.Label(
                self.history_container,
                text="No history",
                font=("Segoe UI", 9),
                bg=self.colors['sidebar'],
                fg='gray'
            ).pack(pady=20)
            return
        
        for idx, item in enumerate(self.history):
            self.create_history_thumbnail(item, idx)
    
    def create_history_thumbnail(self, item, index):
        """Create a thumbnail widget for a history item."""
        frame = tk.Frame(
            self.history_container,
            bg='white',
            relief=tk.SOLID,
            borderwidth=1
        )
        frame.pack(fill=tk.X, pady=3)
        
        try:
            # Load thumbnail
            img = Image.open(item["path"])
            img.thumbnail((80, 50), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            inner = tk.Frame(frame, bg='white')
            inner.pack(fill=tk.X, padx=5, pady=5)
            
            label = tk.Label(inner, image=photo, bg='white', cursor="hand2")
            label.image = photo
            label.pack(side=tk.LEFT, padx=(0, 10))
            
            info_frame = tk.Frame(inner, bg='white')
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            tk.Label(
                info_frame,
                text=item['filename'][:25],
                font=("Segoe UI", 9, "bold"),
                bg='white',
                fg=self.colors['text'],
                anchor=tk.W
            ).pack(fill=tk.X)
            
            tk.Label(
                info_frame,
                text=item['timestamp'][:10],
                font=("Segoe UI", 7),
                bg='white',
                fg='gray',
                anchor=tk.W
            ).pack(fill=tk.X)
            
            label.bind("<Button-1>", lambda e, path=item["path"]: self.set_from_history(path))
            
            def on_enter(e):
                frame.config(bg=self.colors['accent'])
            def on_leave(e):
                frame.config(bg='white')
            
            frame.bind("<Enter>", on_enter)
            frame.bind("<Leave>", on_leave)
            label.bind("<Enter>", on_enter)
            
        except Exception:
            tk.Label(
                frame,
                text=f"Error: {item['filename'][:20]}",
                font=("Segoe UI", 8),
                bg='white',
                fg='red'
            ).pack(padx=5, pady=5)
    
    def set_from_history(self, image_path):
        """Set wallpaper from history."""
        if os.path.exists(image_path):
            self.preview_image_path = image_path
            self.display_preview(image_path, f"History: {os.path.basename(image_path)}")
            self.set_wallpaper()
        else:
            messagebox.showerror("Error", f"Image file not found:\n{image_path}")
    
    def display_current_wallpaper(self):
        """Display current wallpaper info."""
        self.current_text.config(state=tk.NORMAL)
        self.current_text.delete(1.0, tk.END)
        
        if self.history:
            current = self.history[0]
            info = f"📁 {current['filename']}\n\n"
            info += f"🕒 {current['timestamp'][:19].replace('T', ' ')}\n\n"
            info += f"📍 {current['path']}"
            self.current_text.insert(1.0, info)
        else:
            self.current_text.insert(1.0, "No wallpaper set yet")
        
        self.current_text.config(state=tk.DISABLED)
    
    def clear_history(self):
        """Clear wallpaper history."""
        if not self.history:
            return
            
        if messagebox.askyesno("Clear History", "Clear all history entries?"):
            self.history = []
            self.save_history()
            self.refresh_display()
            self.update_status("History cleared", '#28a745')
    
    def auto_fetch_and_set(self):
        """Auto fetch new wallpaper and immediately set it (sync)."""
        self.update_status("Auto-fetching wallpaper...", '#007bff')
        self.auto_fetch_btn.config(state=tk.DISABLED)
        
        def auto_fetch_task():
            try:
                # Fetch from current URL
                url = self.url_entry.get().strip() or "https://picsum.photos/1920/1080"
                
                response = requests.get(url, timeout=30, stream=True)
                response.raise_for_status()
                
                # Save image
                filename = f"wallpaper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                temp_path = self.wallpapers_dir / filename
                
                with open(temp_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Set as wallpaper immediately
                image_path = str(temp_path)
                success = self.set_wallpaper_platform(image_path)
                
                if success:
                    self.add_to_history(image_path)
                    self.root.after(0, lambda: self.on_auto_fetch_success(image_path))
                else:
                    self.root.after(0, lambda: self.on_auto_fetch_error("Failed to set wallpaper"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.on_auto_fetch_error(str(e)))
        
        threading.Thread(target=auto_fetch_task, daemon=True).start()
    
    def on_auto_fetch_success(self, image_path):
        """Handle successful auto-fetch."""
        self.auto_fetch_btn.config(state=tk.NORMAL)
        self.refresh_display()
        self.update_status(f"Auto-fetched: {os.path.basename(image_path)}", '#28a745')
        self.reset_timer()  # Reset timer after manual fetch
    
    def on_auto_fetch_error(self, error):
        """Handle auto-fetch error."""
        self.auto_fetch_btn.config(state=tk.NORMAL)
        self.update_status("Auto-fetch failed", '#dc3545')
        messagebox.showerror("Auto-Fetch Error", f"Failed to fetch wallpaper:\n{error}")
    
    def toggle_auto_rotate(self):
        """Toggle auto-rotation on/off."""
        self.auto_rotate_enabled = self.auto_rotate_var.get()
        
        if self.auto_rotate_enabled:
            self.start_auto_rotate()
        else:
            self.stop_auto_rotate()
    
    def apply_interval(self):
        """Apply new rotation interval."""
        try:
            interval = int(self.interval_entry.get())
            if interval < 1:
                raise ValueError("Interval must be at least 1 minute")
            
            self.rotation_interval_minutes = interval
            self.update_status(f"Interval set to {interval} min", '#28a745')
            
            # Reset timer if auto-rotate is active
            if self.auto_rotate_enabled:
                self.reset_timer()
                
        except ValueError as e:
            messagebox.showerror("Invalid Input", "Please enter a valid number (minimum 1 minute)")
    
    def start_auto_rotate(self):
        """Start auto-rotation with timer."""
        self.update_status("Auto-rotate enabled", '#28a745')
        self.reset_timer()
    
    def stop_auto_rotate(self):
        """Stop auto-rotation."""
        self.stop_timer_flag = True
        self.timer_label.config(text="--:--")
        self.update_status("Auto-rotate disabled", '#6c757d')
    
    def reset_timer(self):
        """Reset the countdown timer."""
        if not self.auto_rotate_enabled:
            return
        
        # Stop existing timer
        self.stop_timer_flag = True
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1.0)
        
        # Start new timer
        self.time_remaining_seconds = self.rotation_interval_minutes * 60
        self.stop_timer_flag = False
        self.timer_thread = threading.Thread(target=self.timer_worker, daemon=True)
        self.timer_thread.start()
    
    def timer_worker(self):
        """Background worker for countdown timer."""
        while self.time_remaining_seconds > 0 and not self.stop_timer_flag:
            # Update timer display
            mins, secs = divmod(self.time_remaining_seconds, 60)
            self.root.after(0, lambda m=mins, s=secs: self.timer_label.config(text=f"{m:02d}:{s:02d}"))
            
            time.sleep(1)
            self.time_remaining_seconds -= 1
        
        # Timer expired - trigger auto-fetch
        if not self.stop_timer_flag and self.auto_rotate_enabled:
            self.root.after(0, self.auto_rotate_fetch)
    
    def auto_rotate_fetch(self):
        """Fetch and set new wallpaper when timer expires."""
        self.auto_fetch_and_set()


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = WallpaperManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()