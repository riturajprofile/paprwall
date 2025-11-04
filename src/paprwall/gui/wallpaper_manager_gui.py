"""
PaprWall - Modern Desktop Wallpaper Manager GUI
A clean, feature-rich wallpaper manager with motivational quotes
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
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk, ImageDraw, ImageFont
import requests


class ModernWallpaperGUI:
    """Modern wallpaper manager with clean UI and enhanced features."""

    def __init__(self, root):
        self.root = root
        self.root.title("PaprWall - Modern Wallpaper Manager")

        # Set window icon
        self.set_window_icon()

        # Window setup
        self.setup_window()

        # Initialize variables
        self.init_variables()

        # Setup data directories
        self.setup_directories()

        # Load configuration and history
        self.load_config()
        self.load_history()

        # Build UI
        self.build_ui()

        # Load history gallery after UI is ready
        self.root.after(50, self.update_history_gallery)

        # Check for first run installation
        self.root.after(100, self.check_first_run_installation)

        # Start background tasks
        self.root.after(500, self.fetch_initial_wallpaper)

        # Start auto-rotation if enabled
        self.root.after(1000, self.start_auto_rotate_if_enabled)

    def set_window_icon(self):
        """Set the window icon."""
        try:
            # Find the icon file
            if getattr(sys, "frozen", False):
                # Running as PyInstaller bundle
                bundle_dir = Path(sys._MEIPASS)
                icon_path = bundle_dir / "assets" / "paprwall-icon.png"
            else:
                # Running as script
                gui_dir = Path(__file__).parent
                project_root = gui_dir.parent.parent
                icon_path = project_root / "assets" / "paprwall-icon.png"

            if icon_path.exists():
                # Load icon and set it
                icon_img = Image.open(icon_path)
                icon_photo = ImageTk.PhotoImage(icon_img)
                self.root.iconphoto(True, icon_photo)
                # Keep a reference to prevent garbage collection
                self.root._icon_photo = icon_photo

        except Exception as e:
            # Icon is optional, don't crash if it fails
            pass

    def setup_window(self):
        """Configure main window."""
        # Set minimum size
        self.root.minsize(1200, 700)

        # Maximize window
        if platform.system() == "Windows":
            self.root.state("zoomed")
        else:
            self.root.attributes("-zoomed", True)

        # Modern color scheme
        self.colors = {
            "bg_primary": "#0f1419",
            "bg_secondary": "#1a1f26",
            "bg_tertiary": "#242b35",
            "bg_hover": "#2d3748",
            "accent_blue": "#3b82f6",
            "accent_purple": "#8b5cf6",
            "accent_green": "#10b981",
            "accent_red": "#ef4444",
            "text_primary": "#f9fafb",
            "text_secondary": "#9ca3af",
            "text_muted": "#6b7280",
            "border": "#374151",
        }

        self.root.configure(bg=self.colors["bg_primary"])

    def init_variables(self):
        """Initialize application variables."""
        # Current state
        self.current_wallpaper = None
        self.current_quote = {"text": "Transform your desktop", "author": "PaprWall"}
        self.preview_image = None
        self.is_fetching = False  # Prevent concurrent fetches
        self.fetch_lock = threading.Lock()

        # Auto-rotation
        self.auto_rotate = tk.BooleanVar(value=True)
        self.rotate_interval = tk.IntVar(value=30)  # Changed to 30 minutes
        self.timer_thread = None
        self.timer_running = False
        self.time_remaining = 0

        # Settings
        self.quote_category = tk.StringVar(value="motivational")
        self.auto_fetch_on_start = tk.BooleanVar(value=True)

        # Quote categories
        self.categories = {
            "motivational": "Motivational",
            "mathematics": "Mathematics",
            "science": "Science",
            "famous": "Famous People",
            "technology": "Technology",
            "philosophy": "Philosophy",
        }

        # API endpoints with fallbacks
        self.quote_apis = {
            "quotable": "https://api.quotable.io/random",
            "zenquotes": "https://zenquotes.io/api/random",
            "type.fit": "https://type.fit/api/quotes",
        }

        # Multiple image sources for reliability
        self.image_sources = [
            "https://picsum.photos/1920/1080",
            "https://loremflickr.com/1920/1080/nature",
            "https://loremflickr.com/1920/1080/landscape",
        ]

        # Retry configuration
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def setup_directories(self):
        """Setup data directories."""
        if platform.system() == "Windows":
            base_dir = Path(os.environ.get("APPDATA", Path.home()))
        else:
            base_dir = Path.home() / ".local" / "share"

        self.data_dir = base_dir / "paprwall"
        self.wallpapers_dir = self.data_dir / "wallpapers"
        self.config_file = self.data_dir / "config.json"
        self.history_file = self.data_dir / "history.json"

        # Create directories
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.wallpapers_dir.mkdir(exist_ok=True)

    def load_config(self):
        """Load user configuration."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    self.quote_category.set(config.get("category", "motivational"))
                    self.rotate_interval.set(config.get("interval", 60))
                    self.auto_rotate.set(config.get("auto_rotate", False))
            except Exception as e:
                print(f"Failed to load config: {e}")

    def save_config(self):
        """Save user configuration."""
        try:
            config = {
                "category": self.quote_category.get(),
                "interval": self.rotate_interval.get(),
                "auto_rotate": self.auto_rotate.get(),
            }
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Failed to save config: {e}")

    def load_history(self):
        """Load wallpaper history."""
        self.history = []
        if self.history_file.exists():
            try:
                with open(self.history_file, "r") as f:
                    data = json.load(f)
                    # Ensure it's a list
                    if isinstance(data, list):
                        self.history = data
                    else:
                        self.history = []
            except Exception as e:
                print(f"Failed to load history: {e}")
                self.history = []

    def save_to_history(self, wallpaper_path, quote):
        """Save wallpaper to history."""
        try:
            # Create entry
            entry = {
                "path": str(wallpaper_path),
                "quote": quote,
                "timestamp": datetime.now().isoformat(),
            }

            # Ensure history is a list
            if not isinstance(self.history, list):
                self.history = []

            # Add to beginning
            self.history.insert(0, entry)
            self.history = self.history[:50]  # Keep last 50

            # Save to file
            with open(self.history_file, "w") as f:
                json.dump(self.history, f, indent=2)

            # Update gallery display
            self.root.after(0, self.update_history_gallery)
        except Exception as e:
            print(f"Failed to save history: {e}")

    def build_ui(self):
        """Build the user interface."""
        # Create main sections
        self.create_header()
        self.create_main_area()
        self.create_sidebar()

    def create_header(self):
        """Create header bar."""
        header = tk.Frame(self.root, bg=self.colors["bg_secondary"], height=60)
        header.pack(side=tk.TOP, fill=tk.X)
        header.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(header, bg=self.colors["bg_secondary"])
        logo_frame.pack(side=tk.LEFT, padx=20, pady=10)

        tk.Label(
            logo_frame,
            text="PaprWall",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors["bg_secondary"],
            fg=self.colors["accent_blue"],
        ).pack(side=tk.LEFT)

        tk.Label(
            logo_frame,
            text="Modern Wallpaper Manager",
            font=("Segoe UI", 10),
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_secondary"],
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Quick actions
        actions = tk.Frame(header, bg=self.colors["bg_secondary"])
        actions.pack(side=tk.RIGHT, padx=20, pady=10)

        # Status indicator
        self.status_label = tk.Label(
            actions,
            text="● Ready",
            font=("Segoe UI", 10),
            bg=self.colors["bg_secondary"],
            fg=self.colors["accent_green"],
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

        # Quick action buttons
        self.create_button(
            actions,
            "Random",
            lambda: self.fetch_random_wallpaper(),
            self.colors["accent_blue"],
        ).pack(side=tk.LEFT, padx=2)

        self.create_button(
            actions, "Browse", self.browse_local_file, self.colors["bg_tertiary"]
        ).pack(side=tk.LEFT, padx=2)

    def create_main_area(self):
        """Create main content area."""
        main = tk.Frame(self.root, bg=self.colors["bg_primary"])
        main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Preview section (bigger vertically)
        preview_container = tk.Frame(main, bg=self.colors["bg_secondary"])
        preview_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Preview header
        preview_header = tk.Frame(preview_container, bg=self.colors["bg_secondary"])
        preview_header.pack(fill=tk.X, pady=(10, 15))

        tk.Label(
            preview_header,
            text="Preview",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
        ).pack(side=tk.LEFT, padx=15)

        # Resolution info
        self.resolution_label = tk.Label(
            preview_header,
            text="1920×1080",
            font=("Segoe UI", 10),
            bg=self.colors["bg_tertiary"],
            fg=self.colors["text_secondary"],
            padx=10,
            pady=5,
        )
        self.resolution_label.pack(side=tk.RIGHT, padx=15)

        # Preview canvas (expands vertically)
        canvas_frame = tk.Frame(preview_container, bg="black")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        self.preview_canvas = tk.Canvas(
            canvas_frame,
            bg="#000000",
            highlightthickness=1,
            highlightbackground=self.colors["border"],
        )
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)

        # Quote display
        quote_frame = tk.Frame(preview_container, bg=self.colors["bg_tertiary"])
        quote_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        # Quote content frame with refresh button
        quote_content_frame = tk.Frame(quote_frame, bg=self.colors["bg_tertiary"])
        quote_content_frame.pack(fill=tk.BOTH, expand=True)

        self.quote_display = tk.Label(
            quote_content_frame,
            text='"Transform your desktop with beautiful wallpapers"',
            font=("Georgia", 11, "italic"),
            bg=self.colors["bg_tertiary"],
            fg=self.colors["text_primary"],
            wraplength=750,
            justify="left",
            padx=20,
            pady=15,
        )
        self.quote_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Refresh quote button
        self.create_button(
            quote_content_frame,
            "↻",
            self.refresh_quote_only,
            self.colors["accent_blue"],
            width=3,
        ).pack(side=tk.RIGHT, padx=10, pady=5)

        # Action buttons
        button_frame = tk.Frame(preview_container, bg=self.colors["bg_secondary"])
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        self.create_button(
            button_frame,
            "Set as Wallpaper",
            self.set_wallpaper,
            self.colors["accent_green"],
            width=20,
        ).pack(side=tk.LEFT, padx=5)

        self.create_button(
            button_frame,
            "Refresh",
            self.fetch_random_wallpaper,
            self.colors["accent_blue"],
            width=15,
        ).pack(side=tk.LEFT, padx=5)

        # History gallery (fixed height at bottom)
        self.create_history_section(main)

    def create_history_section(self, parent):
        """Create history gallery section."""
        history_container = tk.Frame(parent, bg=self.colors["bg_secondary"], height=180)
        history_container.pack(fill=tk.X, expand=False, padx=20, pady=(0, 20))
        history_container.pack_propagate(False)

        # Header
        header = tk.Frame(history_container, bg=self.colors["bg_secondary"])
        header.pack(fill=tk.X, pady=(10, 10), padx=15)

        tk.Label(
            header,
            text="History",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
        ).pack(side=tk.LEFT)

        # Gallery canvas
        gallery_frame = tk.Frame(history_container, bg=self.colors["bg_secondary"])
        gallery_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Scrollable canvas
        self.history_canvas = tk.Canvas(
            gallery_frame,
            bg=self.colors["bg_secondary"],
            height=150,
            highlightthickness=0,
        )

        scrollbar = ttk.Scrollbar(
            gallery_frame, orient=tk.HORIZONTAL, command=self.history_canvas.xview
        )

        self.history_canvas.configure(xscrollcommand=scrollbar.set)

        self.history_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create inner frame for thumbnails
        self.history_frame = tk.Frame(
            self.history_canvas, bg=self.colors["bg_secondary"]
        )
        self.history_canvas_window = self.history_canvas.create_window(
            (0, 0), window=self.history_frame, anchor="nw"
        )

        self.history_frame.bind("<Configure>", self.on_history_configure)

    def on_history_configure(self, event):
        """Update scroll region when history frame changes."""
        self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all"))

    def create_sidebar(self):
        """Create right sidebar with controls."""
        sidebar = tk.Frame(self.root, bg=self.colors["bg_secondary"], width=450)
        sidebar.pack(side=tk.RIGHT, fill=tk.BOTH)
        sidebar.pack_propagate(False)

        # Scrollable content
        canvas = tk.Canvas(
            sidebar, bg=self.colors["bg_secondary"], highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(sidebar, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg_secondary"])

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Sections
        self.create_category_section(scrollable_frame)
        self.create_auto_rotation_section(scrollable_frame)
        self.create_url_section(scrollable_frame)
        self.create_settings_section(scrollable_frame)

    def create_section(self, parent, title):
        """Create a section container."""
        section = tk.Frame(parent, bg=self.colors["bg_secondary"])
        section.pack(fill=tk.X, padx=15, pady=(15, 0))

        tk.Label(
            section,
            text=title,
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
        ).pack(anchor="w", pady=(0, 10))

        return section

    def create_category_section(self, parent):
        """Create quote category selection."""
        section = self.create_section(parent, "Quote Category")

        for key, label in self.categories.items():
            rb = tk.Radiobutton(
                section,
                text=label,
                variable=self.quote_category,
                value=key,
                font=("Segoe UI", 10),
                bg=self.colors["bg_secondary"],
                fg=self.colors["text_primary"],
                selectcolor=self.colors["bg_tertiary"],
                activebackground=self.colors["bg_secondary"],
                activeforeground=self.colors["accent_blue"],
                command=self.on_category_change,
            )
            rb.pack(anchor="w", pady=2)

    def create_auto_rotation_section(self, parent):
        """Create auto-rotation controls."""
        section = self.create_section(parent, "Auto-Rotation")

        # Enable checkbox
        check = tk.Checkbutton(
            section,
            text="Enable auto-rotation",
            variable=self.auto_rotate,
            font=("Segoe UI", 10),
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
            selectcolor=self.colors["bg_tertiary"],
            activebackground=self.colors["bg_secondary"],
            command=self.toggle_auto_rotate,
        )
        check.pack(anchor="w", pady=5)

        # Interval control
        interval_frame = tk.Frame(section, bg=self.colors["bg_secondary"])
        interval_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            interval_frame,
            text="Interval (minutes):",
            font=("Segoe UI", 10),
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_secondary"],
        ).pack(side=tk.LEFT)

        interval_spin = tk.Spinbox(
            interval_frame,
            from_=5,
            to=1440,
            textvariable=self.rotate_interval,
            width=8,
            font=("Segoe UI", 10),
            bg=self.colors["bg_tertiary"],
            fg=self.colors["text_primary"],
            buttonbackground=self.colors["bg_hover"],
        )
        interval_spin.pack(side=tk.RIGHT)

        # Timer display
        self.timer_label = tk.Label(
            section,
            text="Next update: --:--",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["bg_tertiary"],
            fg=self.colors["accent_blue"],
            padx=10,
            pady=5,
        )
        self.timer_label.pack(fill=tk.X, pady=5)

    def create_url_section(self, parent):
        """Create custom URL input."""
        section = self.create_section(parent, "Custom Image URL")

        self.url_entry = tk.Entry(
            section,
            font=("Segoe UI", 10),
            bg=self.colors["bg_tertiary"],
            fg=self.colors["text_primary"],
            insertbackground=self.colors["text_primary"],
            relief=tk.FLAT,
        )
        self.url_entry.pack(fill=tk.X, pady=5, ipady=5)

        self.create_button(
            section, "Fetch from URL", self.fetch_from_url, self.colors["accent_purple"]
        ).pack(fill=tk.X, pady=5)

    def create_settings_section(self, parent):
        """Create settings and utilities."""
        section = self.create_section(parent, "Settings & Utilities")

        # Install to system (if not installed)
        if not self.is_already_installed() and getattr(sys, "frozen", False):
            self.create_button(
                section,
                "Install to System",
                self.install_to_system,
                self.colors["accent_blue"],
            ).pack(fill=tk.X, pady=5)

        # Open data folder
        self.create_button(
            section,
            "Open Data Folder",
            self.open_data_folder,
            self.colors["bg_tertiary"],
        ).pack(fill=tk.X, pady=5)

        # Clear history
        self.create_button(
            section, "Clear History", self.clear_history, self.colors["bg_tertiary"]
        ).pack(fill=tk.X, pady=5)

        # Uninstall
        if self.is_already_installed():
            self.create_button(
                section,
                "Uninstall PaprWall",
                self.uninstall_app,
                self.colors["accent_red"],
            ).pack(fill=tk.X, pady=5)

        # About
        self.create_button(
            section, "About", self.show_about, self.colors["bg_tertiary"]
        ).pack(fill=tk.X, pady=5)

    def create_button(self, parent, text, command, bg_color, width=None):
        """Create a styled button."""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg=bg_color,
            fg="white",
            activebackground=self.colors["bg_hover"],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
        )
        if width:
            btn.config(width=width)
        return btn

    # ===== Event Handlers =====

    def on_category_change(self):
        """Handle category change."""
        self.save_config()
        self.update_status("Category changed", "accent_green")

    def toggle_auto_rotate(self):
        """Toggle auto-rotation."""
        if self.auto_rotate.get():
            self.start_auto_rotation()
        else:
            self.stop_auto_rotation()
        self.save_config()

    def browse_local_file(self):
        """Browse and select local image file."""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            self.load_image_to_preview(file_path)
            self.current_wallpaper = file_path
            self.update_status("Local image loaded", "accent_green")

    def _fetch_image_helper(self, url, filename_prefix="temp", fetch_quote=True):
        """Helper method to fetch and process images."""
        try:
            if fetch_quote:
                self.fetch_quote()

            response = requests.get(
                url,
                timeout=10,
                allow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0"},
            )

            if response.status_code == 200:
                # Determine file extension
                content_type = response.headers.get("content-type", "").lower()
                if "png" in content_type:
                    ext = "png"
                elif "webp" in content_type:
                    ext = "webp"
                else:
                    ext = "jpg"

                temp_path = (
                    self.wallpapers_dir / f"{filename_prefix}_{int(time.time())}.{ext}"
                )
                with open(temp_path, "wb") as f:
                    f.write(response.content)

                self.root.after(0, lambda: self.load_image_to_preview(str(temp_path)))
                self.current_wallpaper = str(temp_path)
                self.root.after(
                    0, lambda: self.update_status("Image loaded", "accent_green")
                )
                return True
            else:
                self.root.after(
                    0, lambda: self.update_status("Failed to fetch", "accent_red")
                )
                return False
        except Exception as e:
            print(f"[ERROR] Fetch failed: {e}")
            self.root.after(
                0, lambda: self.update_status(f"Error: {str(e)}", "accent_red")
            )
            return False

    def fetch_random_wallpaper(self):
        """Fetch random wallpaper from internet, always try picsum first, then fallback."""
        with self.fetch_lock:
            if self.is_fetching:
                print("[DEBUG] Already fetching, ignoring request")
                return
            self.is_fetching = True

        self.update_status("Fetching wallpaper...", "accent_blue")

        def fetch():
            import random

            success = False
            last_error = None
            sources = ["https://picsum.photos/1920/1080"] + [s for s in self.image_sources if s != "https://picsum.photos/1920/1080"]

            for attempt in range(self.max_retries):
                # Always try picsum first, then fallback to other sources
                url = sources[0] if attempt == 0 else random.choice(sources[1:])
                try:
                    print(f"[DEBUG] Attempt {attempt + 1}/{self.max_retries}: Fetching from {url}")
                    response = requests.get(
                        url,
                        timeout=15,
                        allow_redirects=True,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        },
                    )

                    if response.status_code == 200:
                        temp_path = self.wallpapers_dir / f"temp_{int(time.time())}.jpg"
                        with open(temp_path, "wb") as f:
                            f.write(response.content)

                        print(f"[DEBUG] Image saved to: {temp_path}")

                        self.fetch_quote_with_retry()
                        time.sleep(0.5)

                        preview_path = self.embed_quote_on_image(str(temp_path))
                        self.current_wallpaper = str(temp_path)

                        self.root.after(0, lambda p=preview_path: self.load_image_to_preview(p))
                        self.root.after(0, lambda: self.update_status("Wallpaper loaded", "accent_green"))

                        success = True
                        break
                    else:
                        last_error = f"HTTP {response.status_code}"
                        print(f"[WARN] Attempt {attempt + 1} failed: {last_error}")

                except requests.exceptions.Timeout:
                    last_error = "Request timeout"
                    print(f"[WARN] Attempt {attempt + 1} timeout")

                except requests.exceptions.ConnectionError as e:
                    last_error = "Network connection error"
                    print(f"[WARN] Attempt {attempt + 1} connection error: {e}")

                except Exception as e:
                    last_error = str(e)
                    print(f"[WARN] Attempt {attempt + 1} failed: {e}")

                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)

            if not success:
                error_msg = f"Failed after {self.max_retries} attempts"
                if last_error:
                    error_msg += f": {last_error}"

                self.root.after(0, lambda msg=error_msg: self.update_status(msg[:50], "accent_red"))
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("Fetch Failed", f"{msg}\n\nPlease check your internet connection."))

            with self.fetch_lock:
                self.is_fetching = False

        threading.Thread(target=fetch, daemon=True).start()

    def fetch_quote_with_retry(self):
        """Fetch quote with retry logic (synchronous)."""
        fallback_quotes = [
            {
                "text": "The only way to do great work is to love what you do.",
                "author": "Steve Jobs",
            },
            {
                "text": "Innovation distinguishes between a leader and a follower.",
                "author": "Steve Jobs",
            },
            {"text": "Stay hungry, stay foolish.", "author": "Steve Jobs"},
            {
                "text": "The future belongs to those who believe in the beauty of their dreams.",
                "author": "Eleanor Roosevelt",
            },
            {
                "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
                "author": "Winston Churchill",
            },
        ]

        for attempt in range(2):  # Try twice for quotes
            try:
                category = self.quote_category.get()
                url = self.quote_apis["quotable"]
                params = {"tags": category}

                response = requests.get(url, params=params, timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    quote = {
                        "text": data.get("content", "Stay motivated!"),
                        "author": data.get("author", "Unknown"),
                    }
                    self.current_quote = quote
                    self.root.after(0, self.update_quote_display)
                    print(f"[DEBUG] Quote fetched: {quote['text'][:50]}...")
                    return

            except Exception as e:
                print(f"[DEBUG] Quote fetch attempt {attempt + 1} failed: {e}")
                if attempt == 0:
                    time.sleep(1)  # Wait before retry

        # Use fallback quote
        import random

        quote = random.choice(fallback_quotes)
        self.current_quote = quote
        self.root.after(0, self.update_quote_display)
        print(f"[DEBUG] Using fallback quote: {quote['text'][:50]}...")

    def fetch_quote(self):
        """Fetch motivational quote with fallbacks (async version)."""

        def fetch():
            self.fetch_quote_with_retry()

        threading.Thread(target=fetch, daemon=True).start()

    def update_quote_display(self):
        """Update the quote display label with current quote."""
        try:
            quote_text = self.current_quote.get("text", "")
            author_text = self.current_quote.get("author", "")
            display_text = f'"{quote_text}"\n\n— {author_text}'
            self.quote_display.config(text=display_text)
            print(f"[DEBUG] Updated quote display: {len(quote_text)} chars")
        except Exception as e:
            print(f"[ERROR] Failed to update quote display: {e}")

    def refresh_quote_only(self):
        """Refresh only the quote without changing the wallpaper."""
        self.update_status("Refreshing quote...", "accent_blue")

        def refresh():
            try:
                # Fetch new quote with retry
                self.fetch_quote_with_retry()

                # If there's a current wallpaper, re-embed the new quote on it
                if self.current_wallpaper:
                    preview_path = self.embed_quote_on_image(self.current_wallpaper)
                    self.root.after(0, lambda: self.load_image_to_preview(preview_path))

                self.root.after(
                    0, lambda: self.update_status("Quote refreshed", "accent_green")
                )
            except Exception as e:
                print(f"[ERROR] Failed to refresh quote: {e}")
                self.root.after(
                    0, lambda: self.update_status("Failed to refresh", "accent_red")
                )

        threading.Thread(target=refresh, daemon=True).start()

    def set_wallpaper(self):
        """Set current image as wallpaper."""
        if not self.current_wallpaper:
            messagebox.showwarning("No Image", "Please load an image first")
            return

        self.update_status("Setting wallpaper...", "accent_blue")

        def set_wp():
            try:
                print(f"[DEBUG] Setting wallpaper: {self.current_wallpaper}")
                # Embed quote on the wallpaper
                final_path = self.embed_quote_on_image(self.current_wallpaper)
                print(f"[DEBUG] Wallpaper with quote saved to: {final_path}")

                # Set as system wallpaper
                success = self.set_system_wallpaper(final_path)
                print(f"[DEBUG] Wallpaper set result: {success}")

                if success:
                    # Save original image path (without quote) to history for cleaner thumbnails
                    self.root.after(
                        0, lambda: self.save_to_history(self.current_wallpaper, self.current_quote)
                    )
                    self.root.after(
                        0, lambda: self.update_status("Wallpaper set!", "accent_green")
                    )
                    self.root.after(
                        0,
                        lambda: messagebox.showinfo(
                            "Success", "Wallpaper set successfully!"
                        ),
                    )
                else:
                    self.root.after(
                        0, lambda: self.update_status("Failed to set", "accent_red")
                    )
            except Exception as e:
                print(f"[ERROR] Failed to set wallpaper: {e}")
                self.root.after(
                    0, lambda: messagebox.showerror("Error", f"Failed: {str(e)}")
                )

        threading.Thread(target=set_wp, daemon=True).start()

    def fetch_from_url(self):
        """Fetch image from custom URL."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Please enter an image URL")
            return

        self.update_status("Fetching from URL...", "accent_blue")

        def fetch():
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    temp_path = self.wallpapers_dir / f"custom_{int(time.time())}.jpg"
                    with open(temp_path, "wb") as f:
                        f.write(response.content)

                    self.root.after(
                        0, lambda: self.load_image_to_preview(str(temp_path))
                    )
                    self.current_wallpaper = str(temp_path)
                    self.root.after(
                        0, lambda: self.update_status("Image loaded", "accent_green")
                    )
                else:
                    self.root.after(
                        0, lambda: self.update_status("Invalid URL", "accent_red")
                    )
            except Exception as e:
                self.root.after(
                    0, lambda: self.update_status(f"Error: {str(e)}", "accent_red")
                )

        threading.Thread(target=fetch, daemon=True).start()

    def load_image_to_preview(self, image_path):
        """Load and display image in preview."""
        try:
            # First load image to get dimensions
            img = Image.open(image_path)

            # Update resolution label
            self.resolution_label.config(text=f"{img.width}×{img.height}")

            # Create preview with quote (if available)
            if hasattr(self, "current_quote") and self.current_quote:
                preview_path = self.embed_quote_on_image(image_path)
                if preview_path != image_path:  # Quote was embedded successfully
                    img = Image.open(preview_path)

            # Resize to fit canvas
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()

            if canvas_width > 1 and canvas_height > 1:
                img.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)

            # Convert to PhotoImage
            self.preview_image = ImageTk.PhotoImage(img)

            # Display on canvas
            self.preview_canvas.delete("all")
            x = canvas_width // 2
            y = canvas_height // 2
            self.preview_canvas.create_image(x, y, image=self.preview_image)

        except Exception as e:
            print(f"[ERROR] Failed to load image: {e}")
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def embed_quote_on_image(self, image_path):
        """Embed quote permanently on the image file at top-right corner."""
        try:
            img = Image.open(image_path)
            print(f"[DEBUG] Opened image for quote embedding: {image_path}")

            # Get quote
            if not hasattr(self, "current_quote") or not self.current_quote:
                return image_path  # Return original if no quote

            quote_text = self.current_quote.get("text", "")
            if not quote_text:
                return image_path  # Return original if no quote

            author_text = f"— {self.current_quote.get('author', '')}"

            # Load font with robust fallback
            font = None
            author_font = None
            font_paths = [
                ("arial.ttf", 16, 12),
                ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16, 12),
                ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16, 12),
                ("/System/Library/Fonts/Arial.ttf", 16, 12),  # macOS
                ("C:/Windows/Fonts/arial.ttf", 16, 12),  # Windows
            ]

            for fp, fs, afs in font_paths:
                try:
                    font = ImageFont.truetype(fp, fs)
                    author_font = ImageFont.truetype(fp, afs)
                    print(f"[DEBUG] Loaded font: {fp}")
                    break
                except Exception as fe:
                    print(f"[DEBUG] Font load failed: {fp} ({fe})")

            if font is None:
                try:
                    font = ImageFont.load_default()
                    author_font = font
                    print("[DEBUG] Using default font.")
                except:
                    return image_path  # Return original if font loading fails

            # Calculate position (top-right corner)
            img_width, img_height = img.size
            max_width = max(img_width // 3, 300)

            # Create drawing context
            draw = ImageDraw.Draw(img)

            # Wrap text
            lines = self.wrap_text(quote_text, font, max_width, draw)
            if not lines:
                return image_path

            # Position at top-right
            padding = max(30, img_width // 40)
            x = img_width - max_width - padding
            y = padding

            # Calculate text dimensions - more compact
            line_height = 24  # Reduced line height
            try:
                line_height = font.size + 4 if hasattr(font, "size") else 24
            except:
                pass

            # Calculate actual text height more precisely
            author_height = 16  # Height for author line
            total_height = len(lines) * line_height + author_height + 15  # Minimal extra space

            # Draw semi-transparent background with tighter padding
            try:
                overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)
                overlay_draw.rectangle(
                    [x - 12, y - 10, img_width - padding + 10, y + total_height + 10],
                    fill=(0, 0, 0, 150),
                )

                # Convert image to RGBA and composite with overlay
                if img.mode != "RGBA":
                    img = img.convert("RGBA")
                img = Image.alpha_composite(img, overlay)
                img = img.convert("RGB")

                # Recreate drawing context after compositing
                draw = ImageDraw.Draw(img)
            except Exception as e:
                print(f"[DEBUG] Overlay creation failed, using direct drawing: {e}")
                # Fallback: draw directly on image with tighter padding
                draw.rectangle(
                    [x - 12, y - 10, img_width - padding + 10, y + total_height + 10],
                    fill=(0, 0, 0),
                    outline=(50, 50, 50),
                )
            # Recreate drawing context after compositing
            draw = ImageDraw.Draw(img)

            # Draw quote text on image
            y_offset = y
            for line in lines:
                draw.text((x, y_offset), line, font=font, fill="white")
                y_offset += line_height

            # Draw author text with minimal spacing
            draw.text(
                (x, y_offset + 5), author_text, font=author_font, fill="lightgray"
            )

            # Save permanently with embedded quote
            output_path = str(self.wallpapers_dir / f"wallpaper_{int(time.time())}.jpg")
            img.save(output_path, "JPEG", quality=95)
            print(f"[DEBUG] Saved wallpaper with quote: {output_path}")
            return output_path

        except Exception as e:
            print(f"[ERROR] Failed to embed quote on image: {e}")
            return image_path

    def wrap_text(self, text, font, max_width, draw):
        """Wrap text to fit width."""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        return lines or [text]

    def set_system_wallpaper(self, image_path):
        """Set wallpaper on the system."""
        try:
            system = platform.system()

            if system == "Windows":
                import ctypes

                abs_path = str(Path(image_path).resolve())
                ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
                return True

            elif system == "Linux":
                # Try GNOME
                try:
                    subprocess.run(
                        [
                            "gsettings",
                            "set",
                            "org.gnome.desktop.background",
                            "picture-uri",
                            f"file://{image_path}",
                        ],
                        check=True,
                        capture_output=True,
                    )
                    return True
                except:
                    pass

                # Try KDE
                try:
                    script = f"""
                    qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript '
                        var allDesktops = desktops();
                        for (i=0;i<allDesktops.length;i++) {{
                            d = allDesktops[i];
                            d.wallpaperPlugin = "org.kde.image";
                            d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                            d.writeConfig("Image", "file://{image_path}");
                        }}
                    '
                    """
                    subprocess.run(script, shell=True, check=True, capture_output=True)
                    return True
                except:
                    pass

                # Try XFCE
                try:
                    subprocess.run(
                        [
                            "xfconf-query",
                            "-c",
                            "xfce4-desktop",
                            "-p",
                            "/backdrop/screen0/monitor0/workspace0/last-image",
                            "-s",
                            image_path,
                        ],
                        check=True,
                        capture_output=True,
                    )
                    return True
                except:
                    pass

                # Try feh as fallback
                try:
                    subprocess.run(
                        ["feh", "--bg-scale", image_path],
                        check=True,
                        capture_output=True,
                    )
                    return True
                except:
                    pass

            return False

        except Exception as e:
            print(f"Failed to set wallpaper: {e}")
            return False

    def update_history_gallery(self):
        """Update history thumbnail gallery."""
        try:
            print(f"[DEBUG] Updating history gallery. History entries: {len(self.history) if isinstance(self.history, list) else 0}")
            
            # Clear existing thumbnails
            for widget in self.history_frame.winfo_children():
                widget.destroy()

            # Ensure history is valid
            if (
                not self.history
                or not isinstance(self.history, list)
                or len(self.history) == 0
            ):
                print("[DEBUG] No history to display")
                tk.Label(
                    self.history_frame,
                    text="No history yet",
                    font=("Segoe UI", 10),
                    bg=self.colors["bg_secondary"],
                    fg=self.colors["text_muted"],
                ).pack(pady=20)
                return

            # Create thumbnails for recent entries
            created_count = 0
            for entry in self.history[:10]:
                if entry and isinstance(entry, dict) and "path" in entry:
                    self.create_history_thumbnail(entry)
                    created_count += 1
            
            print(f"[DEBUG] Created {created_count} history thumbnails")
        except Exception as e:
            print(f"[ERROR] Failed to update history gallery: {e}")

    def create_history_thumbnail(self, entry):
        """Create a thumbnail widget for history entry with Set button."""
        try:
            if not entry or "path" not in entry:
                print(f"[DEBUG] Invalid history entry: {entry}")
                return

            image_path = entry.get("path")
            if not image_path or not Path(image_path).exists():
                print(f"[DEBUG] Image path not found: {image_path}")
                return

            # Container frame
            container = tk.Frame(
                self.history_frame,
                bg=self.colors["bg_tertiary"],
                relief=tk.FLAT,
            )
            container.pack(side=tk.LEFT, padx=5, pady=5)

            # Load and resize image
            img = Image.open(image_path)
            img.thumbnail((120, 80), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            # Image label
            img_label = tk.Label(container, image=photo, bg=self.colors["bg_tertiary"])
            img_label.image = photo  # Keep reference
            img_label.pack(padx=5, pady=(5, 2))

            # Set button
            set_btn = tk.Button(
                container,
                text="Set",
                command=lambda e=entry: self.set_from_history(e),
                font=("Segoe UI", 8),
                bg=self.colors["accent_green"],
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                padx=8,
                pady=2,
            )
            set_btn.pack(pady=(0, 5))

            # Hover effect
            def on_enter(e):
                container.config(bg=self.colors["accent_blue"])
                img_label.config(bg=self.colors["accent_blue"])

            def on_leave(e):
                container.config(bg=self.colors["bg_tertiary"])
                img_label.config(bg=self.colors["bg_tertiary"])

            container.bind("<Enter>", on_enter)
            container.bind("<Leave>", on_leave)
            img_label.bind("<Enter>", on_enter)
            img_label.bind("<Leave>", on_leave)

        except Exception as e:
            print(f"Failed to create thumbnail for {entry.get('path', 'unknown')}: {e}")

    def load_from_history(self, image_path):
        """Load wallpaper from history to preview."""
        if Path(image_path).exists():
            self.load_image_to_preview(image_path)
            self.current_wallpaper = image_path
            self.update_status("Loaded from history", "accent_green")
        else:
            messagebox.showerror("Error", "Image file not found")

    def set_from_history(self, entry):
        """Set wallpaper directly from history with its original quote."""
        if not entry or not isinstance(entry, dict):
            messagebox.showerror("Error", "Invalid history entry")
            return
            
        image_path = entry.get("path")
        if not image_path or not Path(image_path).exists():
            messagebox.showerror("Error", "Image file not found")
            return

        self.update_status("Setting wallpaper...", "accent_blue")

        def set_wp():
            try:
                # Get the quote from history entry
                quote = entry.get("quote", self.current_quote)
                
                # Temporarily set the quote to the one from history
                original_quote = self.current_quote
                self.current_quote = quote
                
                # Embed quote on the image
                final_path = self.embed_quote_on_image(image_path)
                
                # Restore current quote
                self.current_quote = original_quote
                
                # Set as wallpaper
                success = self.set_system_wallpaper(final_path)
                if success:
                    self.root.after(
                        0,
                        lambda: self.update_status(
                            "Wallpaper set!", "accent_green"
                        ),
                    )
                    self.root.after(
                        0,
                        lambda: messagebox.showinfo(
                            "Success", "Wallpaper set from history!"
                        ),
                    )
                else:
                    self.root.after(
                        0, lambda: self.update_status("Failed to set", "accent_red")
                    )
            except Exception as e:
                print(f"[ERROR] Failed to set from history: {e}")
                self.root.after(
                    0, lambda: messagebox.showerror("Error", f"Failed: {str(e)}")
                )

        threading.Thread(target=set_wp, daemon=True).start()

    def start_auto_rotation(self):
        """Start auto-rotation timer."""
        if self.timer_running:
            return

        self.timer_running = True
        self.time_remaining = self.rotate_interval.get() * 60
        self.update_timer()

    def stop_auto_rotation(self):
        """Stop auto-rotation timer."""
        self.timer_running = False
        self.timer_label.config(text="Next update: --:--")

    def update_timer(self):
        """Update timer display and fetch when needed."""
        if not self.timer_running or not self.auto_rotate.get():
            return

        if self.time_remaining <= 0:
            # Time to fetch new wallpaper
            self.fetch_random_wallpaper()
            self.time_remaining = self.rotate_interval.get() * 60

        # Update display
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label.config(text=f"Next update: {minutes:02d}:{seconds:02d}")

        self.time_remaining -= 1

        # Schedule next update
        self.root.after(1000, self.update_timer)

    def start_auto_rotate_if_enabled(self):
        """Start auto-rotation if enabled on startup."""
        if self.auto_rotate.get():
            self.start_auto_rotation()

    def fetch_initial_wallpaper(self):
        """Fetch initial wallpaper on startup."""
        if self.auto_fetch_on_start.get():
            self.fetch_random_wallpaper()

    def open_data_folder(self):
        """Open data directory."""
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(self.data_dir)
            elif system == "Darwin":
                subprocess.run(["open", str(self.data_dir)])
            else:
                subprocess.run(["xdg-open", str(self.data_dir)])
            self.update_status("Opened data folder", "accent_green")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {str(e)}")

    def clear_history(self):
        """Clear wallpaper history."""
        if not self.history:
            messagebox.showinfo("Info", "History is already empty")
            return

        if messagebox.askyesno(
            "Clear History", "Are you sure you want to clear all history?"
        ):
            self.history = []
            try:
                with open(self.history_file, "w") as f:
                    json.dump([], f)
                self.update_history_gallery()
                self.update_status("History cleared", "accent_green")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear history: {str(e)}")

    def uninstall_app(self):
        """Uninstall application."""
        result = messagebox.askyesno(
            "Uninstall PaprWall",
            "Are you sure you want to uninstall PaprWall?\n\n"
            "This will remove the application from your system.\n"
            "Your data and settings will be preserved.",
            icon="warning",
        )

        if not result:
            return

        try:
            from ..installer import uninstall_system

            self.root.quit()
            uninstall_system()
        except Exception as e:
            messagebox.showerror("Error", f"Uninstallation failed: {str(e)}")

    def show_about(self):
        """Show about dialog."""
        about_window = tk.Toplevel(self.root)
        about_window.title("About PaprWall")
        about_window.geometry("400x300")
        about_window.configure(bg=self.colors["bg_secondary"])
        about_window.resizable(False, False)

        # Center window
        about_window.transient(self.root)
        about_window.grab_set()

        # Content
        content = tk.Frame(about_window, bg=self.colors["bg_secondary"])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        tk.Label(
            content,
            text="PaprWall",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["bg_secondary"],
            fg=self.colors["accent_blue"],
        ).pack(pady=(0, 10))

        tk.Label(
            content,
            text="Modern Wallpaper Manager",
            font=("Segoe UI", 12),
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_secondary"],
        ).pack(pady=(0, 20))

        from .. import __version__

        tk.Label(
            content,
            text=f"Version {__version__}",
            font=("Segoe UI", 10),
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
        ).pack(pady=5)

        tk.Label(
            content,
            text="Transform your desktop with\nbeautiful wallpapers and quotes",
            font=("Segoe UI", 10),
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_secondary"],
            justify=tk.CENTER,
        ).pack(pady=15)

        tk.Label(
            content,
            text="© 2024 PaprWall\nMIT License",
            font=("Segoe UI", 9),
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_muted"],
            justify=tk.CENTER,
        ).pack(pady=15)

        # Close button
        self.create_button(
            content, "Close", about_window.destroy, self.colors["accent_blue"]
        ).pack(pady=10)

    def update_status(self, message, color_key):
        """Update status label."""
        color = self.colors.get(color_key, self.colors["text_primary"])
        self.status_label.config(text=f"● {message}", fg=color)
        self.root.update_idletasks()

    def check_first_run_installation(self):
        """Check if this is first run and prompt for installation."""
        # Only check if running as frozen executable
        if not getattr(sys, "frozen", False):
            return

        # Check if already installed
        if self.is_already_installed():
            return

        # Check if user previously dismissed
        no_prompt_file = self.data_dir / ".no_install_prompt"
        if no_prompt_file.exists():
            return

        # Prompt user for installation
        response = messagebox.askyesnocancel(
            "Install PaprWall",
            "Welcome to PaprWall! 🎨\n\n"
            "Would you like to install PaprWall to your system?\n\n"
            "This will create:\n"
            "  • Desktop shortcut\n"
            "  • Start Menu entry (Windows) / Application menu (Linux)\n"
            "  • Easy uninstall option\n\n"
            "You can also install later from Settings.\n\n"
            "Yes = Install now\n"
            "No = Ask me next time\n"
            "Cancel = Don't ask again",
            icon="question",
        )

        if response is True:
            # User clicked Yes - install
            self.install_to_system()
        elif response is None:
            # User clicked Cancel - don't ask again
            try:
                no_prompt_file.touch()
            except:
                pass

    def is_already_installed(self):
        """Check if PaprWall is already installed."""
        system = platform.system()

        if system == "Windows":
            # Check if installed in Programs folder
            install_dir = (
                Path(os.environ.get("LOCALAPPDATA", Path.home()))
                / "Programs"
                / "PaprWall"
            )
            return (install_dir / "paprwall-gui.exe").exists()
        else:  # Linux
            # Check if binary exists in user's bin
            bin_path = Path.home() / ".local" / "bin" / "paprwall-gui"
            return bin_path.exists()

    def install_to_system(self):
        """Install PaprWall to the system."""
        try:
            from ..installer import install_system

            self.update_status("Installing...", "accent_blue")

            # Run installation
            result = install_system()

            if result == 0:
                messagebox.showinfo(
                    "Installation Complete",
                    "✅ PaprWall has been installed successfully!\n\n"
                    "You can now find it in:\n"
                    "  • Start Menu (Windows)\n"
                    "  • Application Menu (Linux)\n"
                    "  • Desktop shortcut\n\n"
                    "Enjoy using PaprWall! 🎨",
                )
                self.update_status("Installation successful", "accent_green")
            else:
                messagebox.showerror(
                    "Installation Failed",
                    "Could not complete installation.\n\n"
                    "You can try installing manually from Settings.",
                )
                self.update_status("Installation failed", "accent_red")

        except Exception as e:
            messagebox.showerror(
                "Installation Error",
                f"An error occurred during installation:\n{str(e)}",
            )
            self.update_status("Installation error", "accent_red")


# Legacy class name for compatibility
WallpaperManagerGUI = ModernWallpaperGUI


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="PaprWall - Modern Wallpaper Manager")
    parser.add_argument("--install", action="store_true", help="Install to system")
    parser.add_argument(
        "--uninstall", action="store_true", help="Uninstall from system"
    )
    args = parser.parse_args()

    if args.install:
        from ..installer import install_system

        sys.exit(install_system())

    if args.uninstall:
        from ..installer import uninstall_system

        sys.exit(uninstall_system())

    # Launch GUI
    root = tk.Tk()
    app = ModernWallpaperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
