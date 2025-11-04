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
import random
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import requests


class WallpaperManagerGUI:
    """Main GUI application for wallpaper management with web-inspired design."""
    
    def __init__(self, root):
        """Initialize the wallpaper manager GUI."""
        self.root = root
        self.root.title("PaprWall - Wallpaper Manager")
        
        # Start maximized for full screen experience
        self.root.state('zoomed') if platform.system() == 'Windows' else self.root.attributes('-zoomed', True)
        self.root.minsize(1024, 576)    # Minimum 16:9 size
        self.root.resizable(True, True)
        
        # Dark theme color system (per design spec)
        self.colors = {
            # Backgrounds
            'hero_bg': '#0a0e13',
            'bg_primary': '#0f1419',
            'bg_secondary': '#1a1f26',
            'bg_tertiary': '#242b35',
            'bg_hover': '#2d3748',
            
            # Accents
            'accent_blue': '#3b82f6',
            'accent_purple': '#8b5cf6',
            'accent_cyan': '#06b6d4',
            'success_green': '#10b981',
            'warning_yellow': '#f59e0b',
            'danger_red': '#ef4444',
            
            # Text
            'text_primary': '#f9fafb',
            'text_secondary': '#9ca3af',
            'text_muted': '#6b7280',
            
            # Borders
            'border': '#374151',
            'border_light': '#4b5563'
        }

        self.fonts = {
            'logo': ('Poppins', 28, 'bold'),
            'hero_title': ('Segoe UI', 18, 'normal'),
            'heading': ('Segoe UI', 14, 'bold'),
            'subheading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10, 'normal'),
            'button': ('Segoe UI', 10, 'bold'),
            'small': ('Segoe UI', 8, 'normal'),
            'quote': ('Georgia', 11, 'italic')
        }
        
        # Configure root background
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Setup data directory (cross-platform)
        if platform.system() == "Windows":
            self.data_dir = Path(os.environ.get('APPDATA', Path.home())) / "PaprWall"
        else:
            self.data_dir = Path.home() / ".local" / "share" / "paprwall"
        
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
        
        # Random resolutions
        self.resolutions = [
            "1920x1080", "2560x1440", "3840x2160",
            "1366x768", "1600x900", "1280x720"
        ]
        self.resolution_var = tk.StringVar(value="1920x1080")

        
        # Setup UI
        self.setup_ui()
        
        # Load current wallpaper
        self.refresh_display()
        
        # Check if first run and prompt for installation
        self.root.after(100, self.check_first_run_install)
        
        # Auto-fetch wallpaper and quote on launch
        self.root.after(500, self.auto_fetch_on_launch)
        self.root.after(800, self.fetch_random_quote)
        
        # Fetch second image and start auto-rotation
        self.root.after(5000, self.fetch_second_image_and_start_rotation)
    
    def setup_ui(self):
        """Setup the user interface with responsive full-screen layout."""
        
        # ===== COMPACT HEADER SECTION =====
        hero_section = tk.Frame(
            self.root,
            bg=self.colors['hero_bg']
        )
        hero_section.pack(side=tk.TOP, fill=tk.X)
        hero_section.pack_propagate(True)
        
        # Logo + Title (Left)
        logo_frame = tk.Frame(hero_section, bg=self.colors['hero_bg'])
        logo_frame.pack(side=tk.LEFT, padx=15, pady=8)
        
        tk.Label(
            logo_frame,
            text="Papr",
            font=('Poppins', 20, 'bold'),
            bg=self.colors['hero_bg'],
            fg=self.colors['accent_blue']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            logo_frame,
            text="Wall",
            font=('Poppins', 20, 'bold'),
            bg=self.colors['hero_bg'],
            fg=self.colors['accent_purple']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            logo_frame,
            text="  |  Modern Wallpaper Manager",
            font=('Segoe UI', 12, 'normal'),
            bg=self.colors['hero_bg'],
            fg=self.colors['text_secondary']
        ).pack(side=tk.LEFT, padx=(8, 0))
        
        # Quick Actions (Right)
        actions_frame = tk.Frame(hero_section, bg=self.colors['hero_bg'])
        actions_frame.pack(side=tk.RIGHT, padx=15, pady=8)
        
        # Status Label (moved first)
        self.status_label = tk.Label(
            actions_frame,
            text="● Ready",
            font=self.fonts['body'],
            bg=self.colors['hero_bg'],
            fg=self.colors['success_green']
        )
        self.status_label.pack(side=tk.LEFT, padx=15)
        
        # Random Button
        tk.Button(
            actions_frame,
            text="🎲 Random",
            command=self.fetch_random_wallpaper,
            bg=self.colors['accent_blue'],
            fg='white',
            font=self.fonts['button'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=3)
        
        # Folder Button
        tk.Button(
            actions_frame,
            text="📁 Local",
            command=self.open_wallpapers_folder,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=self.fonts['button'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=3)
        
        # ===== MAIN SECTION (Full Height) =====
        main_section = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_section.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # ==== LEFT SIDEBAR (Fixed 480px width for larger preview) ====
        left_panel = tk.Frame(main_section, bg=self.colors['bg_secondary'], width=480)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        left_panel.pack_propagate(False)
        
        # --- TOP: Preview Section (Responsive Height) ---
        preview_section = tk.Frame(left_panel, bg=self.colors['bg_secondary'])
        preview_section.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Preview Label
        tk.Label(
            preview_section,
            text="Preview",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=self.fonts['heading'],
            anchor='w'
        ).pack(fill=tk.X, padx=12, pady=(8, 5))
        
        # Preview Canvas Container with fixed aspect ratio
        canvas_container = tk.Frame(preview_section, bg='black')
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 8))
        
        # Preview Canvas
        self.preview_canvas = tk.Canvas(
            canvas_container,
            bg='#000000',
            highlightthickness=1,
            highlightbackground=self.colors['border']
        )
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Resolution Badge (overlay on canvas)
        self.resolution_label = tk.Label(
            self.preview_canvas,
            text="1920×1080",
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary'],
            font=self.fonts['small'],
            padx=8,
            pady=4
        )
        
        # Quote Overlay Frame (bottom of canvas with semi-transparent background)
        self.quote_frame = tk.Frame(self.preview_canvas, bg='#000000')
        
        self.quote_text = tk.Label(
            self.quote_frame,
            text='"Change your wallpaper, change your mood"',
            fg=self.colors['text_primary'],
            bg='#000000',
            font=self.fonts['quote'],
            wraplength=420,
            justify='left'
        )
        self.quote_text.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Current quote text storage
        self.current_quote = '"Change your wallpaper, change your mood"'
        
        # Placeholder (will be positioned dynamically)
        self.placeholder_id = self.preview_canvas.create_text(
            200, 150,
            text="🖼️\n\nLoading wallpaper...",
            font=('Segoe UI', 14),
            fill='#666666',
            justify=tk.CENTER
        )
        
        # --- BOTTOM: Controls Section ---
        controls_section = tk.Frame(left_panel, bg=self.colors['bg_secondary'])
        controls_section.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
        
        # URL Fetch Section
        tk.Frame(controls_section, bg=self.colors['border'], height=1).pack(fill=tk.X, pady=(8, 8))
        
        url_label = tk.Label(
            controls_section,
            text="IMAGE URL",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_muted'],
            font=self.fonts['small'],
            anchor='w'
        )
        url_label.pack(fill=tk.X, padx=12, pady=(5, 3))
        
        self.url_entry = tk.Entry(
            controls_section,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=self.fonts['body'],
            relief=tk.FLAT,
            bd=0,
            insertbackground=self.colors['text_primary']
        )
        self.url_entry.pack(fill=tk.X, padx=12, pady=(0, 6))
        self.url_entry.insert(0, "https://picsum.photos/1920/1080")
        
        # Button row
        button_row = tk.Frame(controls_section, bg=self.colors['bg_secondary'])
        button_row.pack(fill=tk.X, padx=12, pady=(0, 10))
        
        self.fetch_btn = tk.Button(
            button_row,
            text="⬇ Fetch",
            command=self.fetch_from_url,
            bg=self.colors['accent_blue'],
            fg='white',
            font=self.fonts['button'],
            relief=tk.FLAT,
            cursor="hand2",
            pady=8
        )
        self.fetch_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        
        # Browse Local File
        browse_button = tk.Button(
            button_row,
            text="📁 Browse",
            command=self.browse_file,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=self.fonts['button'],
            relief=tk.FLAT,
            cursor="hand2",
            pady=8
        )
        browse_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))
        
        # Separator
        tk.Frame(controls_section, bg=self.colors['border'], height=1).pack(fill=tk.X, pady=(8, 8))
        
        # Uninstall button
        uninstall_button = tk.Button(
            controls_section,
            text="🗑️ Uninstall PaprWall",
            command=self.uninstall_app,
            bg=self.colors['danger_red'],
            fg='white',
            font=self.fonts['button'],
            relief=tk.FLAT,
            cursor="hand2",
            pady=8
        )
        uninstall_button.pack(fill=tk.X, padx=12, pady=(0, 10))
        
        # ==== RIGHT PANEL (Expands to fill remaining space) ====
        right_panel = tk.Frame(main_section, bg=self.colors['bg_primary'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Scrollable container for right panel
        right_canvas = tk.Canvas(right_panel, bg=self.colors['bg_primary'], highlightthickness=0)
        right_scrollbar = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=right_canvas.yview)
        right_content = tk.Frame(right_canvas, bg=self.colors['bg_primary'])
        
        right_content.bind(
            "<Configure>",
            lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all"))
        )
        
        right_canvas.create_window((0, 0), window=right_content, anchor='nw', width=right_canvas.winfo_width())
        right_canvas.configure(yscrollcommand=right_scrollbar.set)
        
        # Bind canvas resize to update window width
        right_canvas.bind('<Configure>', lambda e: right_canvas.itemconfig('window', width=e.width))
        right_canvas.create_window((0, 0), window=right_content, anchor='nw', tags='window')
        
        right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        right_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # --- Motivational Quote Section ---
        quote_header = tk.Frame(right_content, bg=self.colors['bg_primary'])
        quote_header.pack(fill=tk.X, padx=15, pady=(12, 8))
        
        tk.Label(
            quote_header,
            text="💭 Motivational Quote",
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            font=self.fonts['heading'],
            anchor='w'
        ).pack(side=tk.LEFT)
        
        quote_card = tk.Frame(
            right_content,
            bg=self.colors['bg_secondary'],
            relief=tk.FLAT
        )
        quote_card.pack(fill=tk.X, padx=15, pady=(0, 12))
        
        # Quote category selector
        category_frame = tk.Frame(quote_card, bg=self.colors['bg_secondary'])
        category_frame.pack(fill=tk.X, padx=12, pady=(12, 8))
        
        tk.Label(
            category_frame,
            text="Category:",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            font=self.fonts['body']
        ).pack(side=tk.LEFT, padx=(0, 8))
        
        # Quote categories
        quote_categories = [
            "💡 Motivational",
            "🔢 Mathematics",
            "🔬 Science",
            "🌟 Famous People",
            "💻 Technology",
            "📚 Philosophy"
        ]
        
        self.quote_category = tk.StringVar(value="💡 Motivational")
        category_dropdown = ttk.Combobox(
            category_frame,
            textvariable=self.quote_category,
            values=quote_categories,
            state='readonly',
            width=18,
            font=self.fonts['body']
        )
        category_dropdown.pack(side=tk.LEFT)
        
        # Quote display area
        quote_display_frame = tk.Frame(quote_card, bg=self.colors['bg_tertiary'])
        quote_display_frame.pack(fill=tk.X, padx=12, pady=(8, 8))
        
        self.quote_display = tk.Label(
            quote_display_frame,
            text=self.current_quote,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=self.fonts['quote'],
            wraplength=600,
            justify='center',
            anchor='center',
            pady=15
        )
        self.quote_display.pack(fill=tk.X, padx=15)
        
        # Quote input area
        quote_input_label = tk.Label(
            quote_card,
            text="CUSTOM QUOTE",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_muted'],
            font=self.fonts['small'],
            anchor='w'
        )
        quote_input_label.pack(fill=tk.X, padx=12, pady=(8, 3))
        
        self.quote_input = tk.Text(
            quote_card,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=self.fonts['body'],
            relief=tk.FLAT,
            bd=0,
            wrap=tk.WORD,
            height=3,
            insertbackground=self.colors['text_primary']
        )
        self.quote_input.pack(fill=tk.X, padx=12, pady=(0, 8))
        self.quote_input.insert(1.0, "Type your own inspirational quote here...")
        
        # Quote action buttons
        quote_button_frame = tk.Frame(quote_card, bg=self.colors['bg_secondary'])
        quote_button_frame.pack(fill=tk.X, padx=12, pady=(0, 12))
        
        tk.Button(
            quote_button_frame,
            text="🎲 Random Quote",
            command=self.fetch_random_quote,
            bg=self.colors['accent_purple'],
            fg='white',
            font=self.fonts['button'],
            relief=tk.FLAT,
            cursor='hand2',
            pady=8
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        
        tk.Button(
            quote_button_frame,
            text="✓ Apply Custom",
            command=self.apply_custom_quote,
            bg=self.colors['accent_cyan'],
            fg='white',
            font=self.fonts['button'],
            relief=tk.FLAT,
            cursor='hand2',
            pady=8
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))
        
        # --- Auto-Rotation Settings ---
        rotation_header = tk.Frame(right_content, bg=self.colors['bg_primary'])
        rotation_header.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        tk.Label(
            rotation_header,
            text="Auto-Rotation",
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            font=self.fonts['heading'],
            anchor='w'
        ).pack(side=tk.LEFT)
        
        rotation_card = tk.Frame(
            right_content,
            bg=self.colors['bg_secondary'],
            relief=tk.FLAT
        )
        rotation_card.pack(fill=tk.X, padx=15, pady=(0, 12))
        
        # Toggle & Interval
        toggle_frame = tk.Frame(rotation_card, bg=self.colors['bg_secondary'])
        toggle_frame.pack(fill=tk.X, padx=12, pady=(12, 8))
        
        self.auto_rotate_var = tk.BooleanVar(value=True)
        toggle_check = ttk.Checkbutton(
            toggle_frame,
            text="Enable Auto-Rotate",
            variable=self.auto_rotate_var,
            command=self.toggle_auto_rotate
        )
        toggle_check.pack(side=tk.LEFT)
        
        tk.Label(
            toggle_frame,
            text="Interval:",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            font=self.fonts['body']
        ).pack(side=tk.LEFT, padx=(15, 5))
        
        self.interval_entry = tk.Entry(
            toggle_frame,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=self.fonts['body'],
            width=6,
            relief=tk.FLAT,
            bd=0
        )
        self.interval_entry.insert(0, "60")
        self.interval_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            toggle_frame,
            text="min",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            font=self.fonts['small']
        ).pack(side=tk.LEFT, padx=5)
        
        apply_btn = tk.Button(
            toggle_frame,
            text="Apply",
            command=self.apply_interval,
            bg=self.colors['accent_blue'],
            fg='white',
            font=self.fonts['button'],
            relief=tk.FLAT,
            cursor='hand2',
            padx=12,
            pady=6
        )
        apply_btn.pack(side=tk.LEFT, padx=10)
        
        # Timer display
        self.timer_label = tk.Label(
            rotation_card,
            text="--:--",
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_cyan'],
            font=('Segoe UI', 16, 'bold')
        )
        self.timer_label.pack(pady=(8, 12))
        
        # --- Current Wallpaper Info ---
        current_header = tk.Frame(right_content, bg=self.colors['bg_primary'])
        current_header.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        tk.Label(
            current_header,
            text="Current Wallpaper",
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            font=self.fonts['heading'],
            anchor='w'
        ).pack(side=tk.LEFT)
        
        current_card = tk.Frame(
            right_content,
            bg=self.colors['bg_secondary'],
            relief=tk.FLAT
        )
        current_card.pack(fill=tk.X, padx=15, pady=(0, 12))
        
        self.current_text = tk.Text(
            current_card,
            height=4,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_secondary'],
            font=self.fonts['body'],
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=12,
            pady=12,
            bd=0
        )
        self.current_text.pack(fill=tk.X, padx=12, pady=12)
        self.current_text.insert(1.0, "No wallpaper set yet")
        self.current_text.config(state=tk.DISABLED)
        
        # --- Recent History Gallery ---
        history_gallery_header = tk.Frame(right_content, bg=self.colors['bg_primary'])
        history_gallery_header.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        tk.Label(
            history_gallery_header,
            text="📜 Recent History Gallery",
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            font=self.fonts['heading'],
            anchor='w'
        ).pack(side=tk.LEFT)
        
        tk.Label(
            history_gallery_header,
            text="Click to preview and set",
            bg=self.colors['bg_primary'],
            fg=self.colors['text_muted'],
            font=self.fonts['small'],
            anchor='e'
        ).pack(side=tk.RIGHT)
        
        history_gallery_card = tk.Frame(
            right_content,
            bg=self.colors['bg_secondary'],
            relief=tk.FLAT
        )
        history_gallery_card.pack(fill=tk.X, padx=15, pady=(0, 12))
        
        gallery_frame = tk.Frame(history_gallery_card, bg=self.colors['bg_secondary'])
        gallery_frame.pack(fill=tk.X, padx=12, pady=12)
        
        gallery_canvas = tk.Canvas(
            gallery_frame,
            bg=self.colors['bg_secondary'],
            height=180,
            highlightthickness=0
        )
        gallery_scrollbar = ttk.Scrollbar(gallery_frame, orient=tk.VERTICAL, command=gallery_canvas.yview)
        
        self.history_gallery_container = tk.Frame(gallery_canvas, bg=self.colors['bg_secondary'])
        self.history_gallery_container.bind(
            "<Configure>",
            lambda e: gallery_canvas.configure(scrollregion=gallery_canvas.bbox("all"))
        )
        
        gallery_canvas.create_window((0, 0), window=self.history_gallery_container, anchor='nw')
        gallery_canvas.configure(yscrollcommand=gallery_scrollbar.set)
        
        gallery_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        gallery_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # --- Primary Action Buttons ---
        action_frame = tk.Frame(right_content, bg=self.colors['bg_primary'])
        action_frame.pack(fill=tk.X, padx=15, pady=(5, 20))
        
        self.set_button = tk.Button(
            action_frame,
            text="✓ Set Wallpaper",
            command=self.set_wallpaper,
            state=tk.DISABLED,
            bg=self.colors['success_green'],
            fg='white',
            font=('Segoe UI', 13, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            pady=15
        )
        self.set_button.pack(fill=tk.X, expand=True)
        
        # Progress bar (initially hidden)
        self.progress = ttk.Progressbar(
            right_content,
            mode='indeterminate',
            length=200
        )
        
        # Store additional widgets that will be referenced
        self.preview_size_label = self.resolution_label
        self.file_entry = self.url_entry  # Reuse URL entry for file path display
        self.auto_fetch_btn = self.fetch_btn  # Can be extended later


    def create_section_header(self, parent, text):
        """Create a section header (legacy - kept for compatibility)."""
        frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        frame.pack(fill=tk.X, padx=20, pady=(6, 6))
        
        tk.Label(
            frame,
            text=text,
            font=self.fonts['subheading'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT)
        
        # Separator line
        sep_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        sep_frame.pack(fill=tk.X, padx=20, pady=(0, 8))
        tk.Frame(sep_frame, bg=self.colors['border'], height=1).pack(fill=tk.X)
    
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
    
    def update_status(self, message, color=None):
        """Update the status bar."""
        if color is None:
            color = self.colors['success_green']
        self.status_label.config(text=f"● {message}", fg=color)
        self.root.update_idletasks()
    
    def check_first_run_install(self):
        """Check if this is the first run and prompt for installation."""
        # Only check if running as a frozen executable (binary)
        if not getattr(sys, 'frozen', False):
            return
        
        system = platform.system()
        
        # Check if already installed
        if system == "Windows":
            install_dir = Path(os.environ.get('LOCALAPPDATA')) / "Programs" / "PaprWall"
            is_installed = (install_dir / "paprwall-gui.exe").exists()
        else:  # Linux
            bin_path = Path.home() / ".local" / "bin" / "paprwall-gui"
            is_installed = bin_path.exists()
        
        # If already installed, don't prompt
        if is_installed:
            return
        
        # Check if user previously dismissed the prompt
        no_prompt_file = self.data_dir / ".no_install_prompt"
        if no_prompt_file.exists():
            return
        
        # Show installation prompt
        result = messagebox.askyesnocancel(
            "Install PaprWall",
            "PaprWall is not installed to your system yet.\n\n"
            "Would you like to install it now?\n\n"
            "This will:\n"
            "• Create a desktop entry/shortcut\n"
            "• Add PaprWall to your application menu\n"
            "• Install the app icon\n\n"
            "Click 'Yes' to install\n"
            "Click 'No' to skip this time\n"
            "Click 'Cancel' to never ask again",
            icon='question'
        )
        
        if result is True:
            # User clicked Yes - install
            try:
                if install_app():
                    messagebox.showinfo(
                        "Installation Complete",
                        "PaprWall has been installed successfully!\n\n"
                        "You can now find it in your application menu."
                    )
            except Exception as e:
                messagebox.showerror("Installation Failed", f"Could not install PaprWall:\n{str(e)}")
        elif result is None:
            # User clicked Cancel - don't ask again
            no_prompt_file.touch()
            messagebox.showinfo(
                "Installation Skipped",
                "You can install PaprWall later by running:\n"
                f"  {Path(sys.executable).name} --install"
            )
    
    def show_toast(self, message, toast_type='success'):
        """Show a toast notification."""
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.attributes('-topmost', True)
        
        bg_color = self.colors['success_green'] if toast_type == 'success' else self.colors['danger_red']
        
        toast_label = tk.Label(
            toast,
            text=message,
            bg=bg_color,
            fg='white',
            font=self.fonts['body'],
            padx=20,
            pady=10
        )
        toast_label.pack()
        
        # Position at top-right
        screen_width = self.root.winfo_screenwidth()
        toast.geometry(f'+{screen_width-350}+20')
        
        # Auto-dismiss after 3 seconds
        self.root.after(3000, toast.destroy)
    
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
        self.update_status("Downloading...", self.colors['accent_blue'])
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
        self.update_status("Downloaded successfully", self.colors['success_green'])
    
    def on_download_error(self, error_message):
        """Handle download error."""
        self.progress.stop()
        self.progress.pack_forget()
        self.fetch_btn.config(state=tk.NORMAL)
        messagebox.showerror("Download Error", error_message)
        self.update_status("Download failed", self.colors['danger_red'])
    
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
    
    def embed_quote_on_image(self, img):
        """Embed the current quote on the image at top-right corner, blended with the image."""
        try:
            # Create a copy to avoid modifying original
            img_with_quote = img.copy()
            
            # Image dimensions
            img_width, img_height = img_with_quote.size
            
            # Try to load a nice font, fallback to default
            try:
                # Smaller font size for top-right corner
                font_size = max(18, img_width // 70)
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Prepare quote text
            quote_text = self.current_quote
            
            # Create a temporary draw object for text measurement
            temp_draw = ImageDraw.Draw(img_with_quote)
            
            # Wrap text to fit in top-right corner (30% of image width)
            max_width = int(img_width * 0.3)
            words = quote_text.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                line_text = ' '.join(current_line)
                bbox = temp_draw.textbbox((0, 0), line_text, font=font)
                if bbox[2] - bbox[0] > max_width:
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(line_text)
                        current_line = []
            
            if current_line:
                lines.append(' '.join(current_line))
            
            quote_text = '\n'.join(lines)
            bbox = temp_draw.textbbox((0, 0), quote_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Position at top-right corner with padding
            padding = 40
            x = img_width - text_width - padding
            y = padding
            
            # Convert image to RGBA for blending
            if img_with_quote.mode != 'RGBA':
                img_with_quote = img_with_quote.convert('RGBA')
            
            # Create overlay with gradient/blur effect for better blending
            overlay = Image.new('RGBA', img_with_quote.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            # Draw a subtle semi-transparent background with more transparency
            bg_padding = 15
            bg_box = [
                x - bg_padding,
                y - bg_padding,
                x + text_width + bg_padding,
                y + text_height + bg_padding
            ]
            
            # Very subtle background (lower opacity for better blending)
            overlay_draw.rectangle(bg_box, fill=(0, 0, 0, 100))
            
            # Composite the overlay
            img_with_quote = Image.alpha_composite(img_with_quote, overlay)
            
            # Draw the text with a subtle shadow for depth
            draw = ImageDraw.Draw(img_with_quote)
            
            # Shadow (offset by 2 pixels)
            shadow_offset = 2
            draw.text((x + shadow_offset, y + shadow_offset), quote_text, font=font, fill=(0, 0, 0, 120))
            
            # Main text
            draw.text((x, y), quote_text, font=font, fill=(255, 255, 255, 240), align='right')
            
            # Convert back to RGB
            if img_with_quote.mode == 'RGBA':
                rgb_img = Image.new('RGB', img_with_quote.size, (255, 255, 255))
                rgb_img.paste(img_with_quote, mask=img_with_quote.split()[3])
                return rgb_img
            
            return img_with_quote
            
        except Exception as e:
            print(f"Error embedding quote: {e}")
            return img
    
    def display_preview(self, image_path, info_text):
        """Display image preview in canvas."""
        try:
            # Open and resize image
            img = Image.open(image_path)
            original_size = f"{img.width} × {img.height}"
            
            # Embed quote on the image
            img = self.embed_quote_on_image(img)
            
            # Force canvas to update its geometry
            self.preview_canvas.update_idletasks()
            
            # Calculate size to fit in canvas (maintain aspect ratio)
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            # Use default size if canvas not yet rendered
            if canvas_width <= 1:
                canvas_width = 456
            if canvas_height <= 1:
                canvas_height = 380
            
            # Remove placeholder
            if self.placeholder_id:
                self.preview_canvas.delete(self.placeholder_id)
                self.placeholder_id = None
            
            # Add padding for better fit
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
            
            # Update resolution badge
            self.preview_size_label.config(text=original_size)
            
            # Place resolution badge on canvas
            self.preview_canvas.delete("resolution")
            self.preview_canvas.create_window(
                canvas_width - 8, 8,
                window=self.preview_size_label,
                anchor='ne',
                tags="resolution"
            )
            
            # Enable set button
            self.set_button.config(state=tk.NORMAL)
            self.update_status("Preview loaded", self.colors['success_green'])
            
        except Exception as e:
            messagebox.showerror("Preview Error", f"Could not load image: {str(e)}")
            self.update_status("Preview failed", self.colors['danger_red'])
    
    def set_wallpaper(self):
        """Set the previewed image as wallpaper."""
        if not self.preview_image_path:
            messagebox.showwarning("No Image", "Please select an image first")
            return
        
        try:
            self.update_status("Preparing wallpaper...", self.colors['accent_blue'])
            
            # Load original image and embed quote
            img = Image.open(self.preview_image_path)
            img_with_quote = self.embed_quote_on_image(img)
            
            # Save the image with embedded quote
            filename = f"wallpaper_quoted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            temp_path = self.wallpapers_dir / filename
            img_with_quote.save(temp_path, quality=95)
            
            # Convert to absolute path
            image_path = os.path.abspath(temp_path)
            
            self.update_status("Setting wallpaper...", self.colors['accent_blue'])
            
            # Set wallpaper based on platform
            success = self.set_wallpaper_platform(image_path)
            
            if success:
                # Add to history
                self.add_to_history(image_path)
                
                # Refresh display
                self.refresh_display()
                
                messagebox.showinfo("Success", "Wallpaper set successfully!")
                self.update_status("Wallpaper applied", self.colors['success_green'])
            else:
                messagebox.showerror("Error", "Failed to set wallpaper")
                self.update_status("Failed", self.colors['danger_red'])
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set wallpaper: {str(e)}")
            self.update_status("Error occurred", self.colors['danger_red'])
    
    def set_wallpaper_platform(self, image_path):
        """Set wallpaper based on platform."""
        system = platform.system()
        
        try:
            if system == "Windows":
                import ctypes
                # Convert to absolute path for Windows
                abs_path = str(Path(image_path).resolve())
                SPI_SETDESKWALLPAPER = 20
                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, abs_path, 3)
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
        """Refresh the history gallery and current wallpaper display."""
        self.history = self.load_history()
        self.display_history_gallery()
        self.display_current_wallpaper()
    
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
            self.update_status("History cleared", self.colors['success_green'])
    
    def auto_fetch_and_set(self):
        """Auto fetch new wallpaper and immediately set it (sync)."""
        self.update_status("Auto-fetching wallpaper...", self.colors['accent_blue'])
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
        self.update_status(f"Auto-fetched: {os.path.basename(image_path)}", self.colors['success_green'])
        self.reset_timer()  # Reset timer after manual fetch
    
    def on_auto_fetch_error(self, error):
        """Handle auto-fetch error."""
        self.auto_fetch_btn.config(state=tk.NORMAL)
        self.update_status("Auto-fetch failed", self.colors['danger_red'])
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
            self.update_status(f"Interval set to {interval} min", self.colors['success_green'])
            
            # Reset timer if auto-rotate is active
            if self.auto_rotate_enabled:
                self.reset_timer()
                
        except ValueError as e:
            messagebox.showerror("Invalid Input", "Please enter a valid number (minimum 1 minute)")
    
    def start_auto_rotate(self):
        """Start auto-rotation with timer."""
        self.update_status("Auto-rotate enabled", self.colors['success_green'])
        self.reset_timer()
    
    def stop_auto_rotate(self):
        """Stop auto-rotation."""
        self.stop_timer_flag = True
        self.timer_label.config(text="--:--")
        self.update_status("Auto-rotate disabled", self.colors['text_muted'])
    
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
    
    def fetch_random_wallpaper(self):
        """Fetch a random wallpaper with current resolution."""
        resolution = self.resolution_var.get()
        width, height = resolution.split('x')
        url = f"https://picsum.photos/{width}/{height}"
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
        self.fetch_from_url()
    
    def update_url_with_resolution(self, event=None):
        """Update URL when resolution changes."""
        current_url = self.url_entry.get().strip()
        if "picsum.photos" in current_url:
            resolution = self.resolution_var.get()
            width, height = resolution.split('x')
            new_url = f"https://picsum.photos/{width}/{height}"
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, new_url)
    
    def open_wallpapers_folder(self):
        """Open wallpapers directory in file manager."""
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(self.wallpapers_dir)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", str(self.wallpapers_dir)])
            else:  # Linux
                subprocess.run(["xdg-open", str(self.wallpapers_dir)])
            self.update_status("Opened wallpapers folder", self.colors['success_green'])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {str(e)}")
    
    def display_history_gallery(self):
        """Display history wallpapers in a gallery format with larger thumbnails."""
        for widget in self.history_gallery_container.winfo_children():
            widget.destroy()
        
        if not self.history:
            tk.Label(
                self.history_gallery_container,
                text="No history yet",
                font=self.fonts['body'],
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_muted']
            ).pack(pady=20)
            return
        
        for idx, item in enumerate(self.history):
            self.create_history_gallery_thumbnail(item, idx)
    
    def create_history_gallery_thumbnail(self, item, index):
        """Create a larger thumbnail widget for history gallery with preview and set functionality."""
        frame = tk.Frame(
            self.history_gallery_container,
            bg=self.colors['bg_tertiary'],
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=self.colors['border']
        )
        frame.pack(fill=tk.X, pady=5)
        
        try:
            # Load larger thumbnail for gallery
            img = Image.open(item["path"])
            img.thumbnail((120, 75), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            inner = tk.Frame(frame, bg=self.colors['bg_tertiary'])
            inner.pack(fill=tk.X, padx=8, pady=8)
            
            # Image thumbnail
            img_label = tk.Label(inner, image=photo, bg=self.colors['bg_tertiary'], cursor="hand2")
            img_label.image = photo
            img_label.pack(side=tk.LEFT, padx=(0, 10))
            
            # Info frame
            info_frame = tk.Frame(inner, bg=self.colors['bg_tertiary'])
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            tk.Label(
                info_frame,
                text=item['filename'][:30],
                font=("Segoe UI", 9, "bold"),
                bg=self.colors['bg_tertiary'],
                fg=self.colors['text_primary'],
                anchor=tk.W
            ).pack(fill=tk.X)
            
            tk.Label(
                info_frame,
                text=item['timestamp'][:10],
                font=("Segoe UI", 8),
                bg=self.colors['bg_tertiary'],
                fg=self.colors['text_muted'],
                anchor=tk.W
            ).pack(fill=tk.X, pady=(2, 0))
            
            # Action buttons frame
            btn_frame = tk.Frame(inner, bg=self.colors['bg_tertiary'])
            btn_frame.pack(side=tk.RIGHT, padx=(10, 0))
            
            # Preview button
            preview_btn = tk.Button(
                btn_frame,
                text="👁 Preview",
                command=lambda path=item["path"]: self.preview_from_history(path),
                bg=self.colors['accent_blue'],
                fg='white',
                font=("Segoe UI", 8, "bold"),
                relief=tk.FLAT,
                cursor="hand2",
                padx=10,
                pady=5
            )
            preview_btn.pack(side=tk.TOP, fill=tk.X, pady=(0, 4))
            
            # Set wallpaper button
            set_btn = tk.Button(
                btn_frame,
                text="✓ Set",
                command=lambda path=item["path"]: self.set_from_history(path),
                bg=self.colors['success_green'],
                fg='white',
                font=("Segoe UI", 8, "bold"),
                relief=tk.FLAT,
                cursor="hand2",
                padx=10,
                pady=5
            )
            set_btn.pack(side=tk.TOP, fill=tk.X)
            
            # Hover effects
            def on_enter(e):
                frame.config(highlightbackground=self.colors['accent_blue'], highlightthickness=2)
            def on_leave(e):
                frame.config(highlightbackground=self.colors['border'], highlightthickness=2)
            
            frame.bind("<Enter>", on_enter)
            frame.bind("<Leave>", on_leave)
            img_label.bind("<Button-1>", lambda e, path=item["path"]: self.preview_from_history(path))
            
        except Exception as e:
            tk.Label(
                frame,
                text=f"Error loading: {item['filename'][:20]}",
                font=("Segoe UI", 8),
                bg=self.colors['bg_tertiary'],
                fg=self.colors['danger_red']
            ).pack(padx=8, pady=8)
    
    def preview_from_history(self, image_path):
        """Preview wallpaper from history without setting it."""
        if os.path.exists(image_path):
            self.preview_image_path = image_path
            self.display_preview(image_path, f"History: {os.path.basename(image_path)}")
            self.update_status("Preview loaded from history", self.colors['success_green'])
        else:
            messagebox.showerror("Error", f"Image file not found:\n{image_path}")
            self.history = [h for h in self.history if h.get("path") != image_path]
            self.save_history()
            self.refresh_display()
    
    def auto_fetch_on_launch(self):
        """Auto-fetch a wallpaper when the GUI launches."""
        self.update_status("Fetching wallpaper...", self.colors['accent_blue'])
        
        def fetch_task():
            try:
                url = self.url_entry.get().strip() or "https://picsum.photos/1920/1080"
                response = requests.get(url, timeout=30, stream=True)
                response.raise_for_status()
                
                filename = f"wallpaper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                temp_path = self.wallpapers_dir / filename
                
                with open(temp_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Display preview
                self.root.after(0, lambda: self.on_launch_fetch_success(str(temp_path)))
                
            except Exception as e:
                self.root.after(0, lambda: self.update_status("Ready", self.colors['success_green']))
        
        threading.Thread(target=fetch_task, daemon=True).start()
    
    def on_launch_fetch_success(self, image_path):
        """Handle successful launch fetch."""
        self.preview_image_path = image_path
        self.display_preview(image_path, f"Picsum: {os.path.basename(image_path)}")
        self.update_status("Downloaded successfully", self.colors['success_green'])
    
    def fetch_second_image_and_start_rotation(self):
        """Fetch a second image and enable auto-rotation."""
        # Fetch second image
        self.update_status("Fetching second wallpaper...", self.colors['accent_blue'])
        
        def fetch_task():
            try:
                url = self.url_entry.get().strip() or "https://picsum.photos/1920/1080"
                response = requests.get(url, timeout=30, stream=True)
                response.raise_for_status()
                
                filename = f"wallpaper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                temp_path = self.wallpapers_dir / filename
                
                with open(temp_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                image_path = str(temp_path)
                success = self.set_wallpaper_platform(image_path)
                
                if success:
                    self.add_to_history(image_path)
                    self.root.after(0, lambda: self.on_second_fetch_success(image_path))
                else:
                    self.root.after(0, lambda: self.update_status("Ready", self.colors['success_green']))
                    
            except Exception as e:
                self.root.after(0, lambda: self.update_status("Ready", self.colors['success_green']))
        
        threading.Thread(target=fetch_task, daemon=True).start()
    
    def on_second_fetch_success(self, image_path):
        """Handle successful second fetch and start auto-rotation."""
        self.refresh_display()
        self.update_status("Auto-rotation started", self.colors['success_green'])
        
        # Start auto-rotation timer
        self.auto_rotate_enabled = True
        self.start_auto_rotate()
    
    def fetch_random_quote(self):
        """Fetch a random quote based on selected category."""
        category = self.quote_category.get()
        self.update_status(f"Fetching {category} quote...", self.colors['accent_purple'])
        
        def fetch_task():
            try:
                quote_text = None
                
                # Map category to API tags/queries
                category_mapping = {
                    "💡 Motivational": ["inspirational", "motivational"],
                    "🔢 Mathematics": ["mathematics", "math"],
                    "🔬 Science": ["science", "physics", "chemistry"],
                    "🌟 Famous People": ["famous-quotes"],
                    "💻 Technology": ["technology", "computers"],
                    "📚 Philosophy": ["philosophy", "wisdom"]
                }
                
                # Get tags for selected category
                tags = category_mapping.get(category, ["inspirational"])
                
                # Try quotable.io API with tags
                try:
                    # Try with first tag
                    tag = tags[0]
                    url = f"https://api.quotable.io/random?tags={tag}"
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    quote_text = f'"{data["content"]}" — {data["author"]}'
                except Exception:
                    # Try zenquotes.io as fallback
                    try:
                        response = requests.get("https://zenquotes.io/api/random", timeout=10)
                        response.raise_for_status()
                        data = response.json()[0]
                        author = data['a'] if data['a'] != 'zenquotes.io' else 'Unknown'
                        quote_text = f'"{data["q"]}" — {author}'
                    except Exception:
                        quote_text = None
                
                if quote_text:
                    self.root.after(0, lambda: self.on_quote_fetched(quote_text))
                else:
                    self.root.after(0, lambda: self.on_quote_fetch_error("Could not fetch quote"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.on_quote_fetch_error(str(e)))
        
        threading.Thread(target=fetch_task, daemon=True).start()
    
    def on_quote_fetched(self, quote_text):
        """Handle successful quote fetch."""
        self.current_quote = quote_text
        self.quote_display.config(text=quote_text)
        self.update_status("Quote updated", self.colors['success_green'])
        
        # Refresh preview if an image is loaded
        if self.preview_image_path:
            self.display_preview(self.preview_image_path, f"Updated quote: {os.path.basename(self.preview_image_path)}")
    
    def on_quote_fetch_error(self, error):
        """Handle quote fetch error with category-specific fallback quotes."""
        self.update_status("Quote fetch failed", self.colors['warning_yellow'])
        
        category = self.quote_category.get()
        
        # Category-specific fallback quotes
        fallback_quotes = {
            "💡 Motivational": [
                '"The only way to do great work is to love what you do." — Steve Jobs',
                '"Believe you can and you\'re halfway there." — Theodore Roosevelt',
                '"Success is not final, failure is not fatal: it is the courage to continue that counts." — Winston Churchill',
                '"Don\'t watch the clock; do what it does. Keep going." — Sam Levenson'
            ],
            "🔢 Mathematics": [
                '"Mathematics is the language in which God has written the universe." — Galileo Galilei',
                '"Pure mathematics is, in its way, the poetry of logical ideas." — Albert Einstein',
                '"Mathematics is not about numbers, equations, or algorithms: it is about understanding." — William Paul Thurston',
                '"The essence of mathematics is not to make simple things complicated, but to make complicated things simple." — Stan Gudder'
            ],
            "🔬 Science": [
                '"Science is not only a disciple of reason but, also, one of romance and passion." — Stephen Hawking',
                '"The important thing is not to stop questioning. Curiosity has its own reason for existing." — Albert Einstein',
                '"Somewhere, something incredible is waiting to be known." — Carl Sagan',
                '"Science knows no country, because knowledge belongs to humanity." — Louis Pasteur'
            ],
            "🌟 Famous People": [
                '"In the end, it\'s not the years in your life that count. It\'s the life in your years." — Abraham Lincoln',
                '"The future belongs to those who believe in the beauty of their dreams." — Eleanor Roosevelt',
                '"Be yourself; everyone else is already taken." — Oscar Wilde',
                '"To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment." — Ralph Waldo Emerson'
            ],
            "💻 Technology": [
                '"Technology is best when it brings people together." — Matt Mullenweg',
                '"The advance of technology is based on making it fit in so that you don\'t really even notice it." — Bill Gates',
                '"Any sufficiently advanced technology is indistinguishable from magic." — Arthur C. Clarke',
                '"Innovation distinguishes between a leader and a follower." — Steve Jobs'
            ],
            "📚 Philosophy": [
                '"The unexamined life is not worth living." — Socrates',
                '"I think, therefore I am." — René Descartes',
                '"Life must be understood backward, but it must be lived forward." — Søren Kierkegaard',
                '"The only true wisdom is in knowing you know nothing." — Socrates'
            ]
        }
        
        quotes = fallback_quotes.get(category, fallback_quotes["💡 Motivational"])
        quote_text = random.choice(quotes)
        self.on_quote_fetched(quote_text)
    
    def apply_custom_quote(self):
        """Apply user's custom quote."""
        custom_text = self.quote_input.get(1.0, tk.END).strip()
        
        if not custom_text or custom_text == "Type your own inspirational quote here...":
            messagebox.showwarning("No Quote", "Please enter a custom quote first")
            return
        
        # Add quotes if not present
        if not custom_text.startswith('"'):
            custom_text = f'"{custom_text}"'
        
        self.current_quote = custom_text
        self.quote_display.config(text=custom_text)
        self.update_status("Custom quote applied", self.colors['success_green'])
        
        # Refresh preview if an image is loaded
        if self.preview_image_path:
            self.display_preview(self.preview_image_path, f"Custom quote: {os.path.basename(self.preview_image_path)}")
        
        messagebox.showinfo("Success", "Custom quote has been embedded on the image!")
    
    def uninstall_app(self):
        """Uninstall PaprWall from the system."""
        result = messagebox.askyesno(
            "Uninstall PaprWall",
            "Are you sure you want to uninstall PaprWall?\n\n"
            "This will remove:\n"
            "• Application binary\n"
            "• Desktop entry and shortcuts\n"
            "• Application icon\n\n"
            "Configuration and wallpaper data will be preserved unless you choose to remove them.",
            icon='warning'
        )
        
        if not result:
            return
        
        try:
            system = platform.system()
            
            if system == "Windows":
                # Run Windows uninstall script
                uninstall_script = Path(os.environ.get('APPDATA')) / "PaprWall" / "UNINSTALL.bat"
                if uninstall_script.exists():
                    # Close the GUI first
                    self.root.quit()
                    subprocess.Popen([str(uninstall_script)], shell=True)
                else:
                    messagebox.showerror(
                        "Uninstall Script Not Found",
                        f"Could not find uninstall script at:\n{uninstall_script}\n\n"
                        "Please manually remove PaprWall from:\n"
                        f"{os.environ.get('LOCALAPPDATA')}\\Programs\\PaprWall"
                    )
            else:
                # Run Linux uninstall script
                uninstall_script = Path.home() / ".local" / "share" / "paprwall" / "uninstall.sh"
                if uninstall_script.exists():
                    # Close the GUI first
                    self.root.quit()
                    subprocess.Popen(['bash', str(uninstall_script)])
                else:
                    messagebox.showerror(
                        "Uninstall Script Not Found",
                        f"Could not find uninstall script at:\n{uninstall_script}\n\n"
                        "Please manually remove PaprWall or run:\n"
                        "pip uninstall paprwall"
                    )
        except Exception as e:
            messagebox.showerror("Uninstall Error", f"Failed to start uninstaller:\n{str(e)}")


def install_app():
    """Install PaprWall to the system."""
    system = platform.system()
    
    if system == "Windows":
        print("Installing PaprWall for Windows...")
        print("=" * 50)
        
        # Get paths
        install_dir = Path(os.environ.get('LOCALAPPDATA')) / "Programs" / "PaprWall"
        data_dir = Path(os.environ.get('APPDATA')) / "PaprWall"
        start_menu = Path(os.environ.get('APPDATA')) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
        
        # Get script directory (where paprwall-gui.exe is located)
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            script_dir = Path(sys.executable).parent
        else:
            # Running as script
            script_dir = Path(__file__).parent.parent.parent.parent
        
        # Create directories
        install_dir.mkdir(parents=True, exist_ok=True)
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy executable
        exe_name = "paprwall-gui.exe" if getattr(sys, 'frozen', False) else "paprwall-gui.py"
        source_exe = script_dir / exe_name
        
        if source_exe.exists():
            shutil.copy2(source_exe, install_dir / "paprwall-gui.exe")
            print(f"✓ Installed to: {install_dir}")
        else:
            print(f"✗ Could not find {exe_name} at {script_dir}")
            return False
        
        # Copy icon if available
        icon_file = script_dir / "paprwall.svg"
        if icon_file.exists():
            shutil.copy2(icon_file, data_dir / "paprwall.svg")
            print("✓ Icon copied")
        
        # Copy uninstall script if available
        uninstall_script = script_dir / "UNINSTALL.bat"
        if uninstall_script.exists():
            shutil.copy2(uninstall_script, data_dir / "UNINSTALL.bat")
            print("✓ Uninstall script copied")
        
        # Create Start Menu shortcut
        try:
            import winshell
            from win32com.client import Dispatch
            
            shortcut_path = start_menu / "PaprWall.lnk"
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.TargetPath = str(install_dir / "paprwall-gui.exe")
            shortcut.Description = "Modern Desktop Wallpaper Manager"
            shortcut.save()
            print("✓ Start Menu shortcut created")
        except ImportError:
            print("⚠ Could not create shortcuts (pywin32 not installed)")
        except Exception as e:
            print(f"⚠ Could not create shortcuts: {e}")
        
        print("\n" + "=" * 50)
        print("Installation Complete!")
        print("=" * 50)
        print(f"\nPaprWall has been installed to: {install_dir}")
        print(f"\nYou can now:")
        print("  1. Find 'PaprWall' in Start Menu")
        print(f"  2. Run: {install_dir}\\paprwall-gui.exe")
        print(f"\nTo uninstall later, run:")
        print(f"  {data_dir}\\UNINSTALL.bat")
        
    else:  # Linux
        print("Installing PaprWall for Linux...")
        print("=" * 50)
        
        # Get paths
        bin_dir = Path.home() / ".local" / "bin"
        apps_dir = Path.home() / ".local" / "share" / "applications"
        icons_dir = Path.home() / ".local" / "share" / "icons" / "hicolor" / "scalable" / "apps"
        data_dir = Path.home() / ".local" / "share" / "paprwall"
        
        # Get script directory
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            script_dir = Path(sys.executable).parent
        else:
            # Running as script
            script_dir = Path(__file__).parent.parent.parent.parent
        
        # Create directories
        bin_dir.mkdir(parents=True, exist_ok=True)
        apps_dir.mkdir(parents=True, exist_ok=True)
        icons_dir.mkdir(parents=True, exist_ok=True)
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy executable
        exe_name = "paprwall-gui"
        source_exe = script_dir / "dist" / exe_name if not getattr(sys, 'frozen', False) else Path(sys.executable)
        
        if source_exe.exists():
            shutil.copy2(source_exe, bin_dir / exe_name)
            os.chmod(bin_dir / exe_name, 0o755)
            print(f"✓ Installed to: {bin_dir / exe_name}")
        else:
            # Try current directory
            source_exe = script_dir / exe_name
            if source_exe.exists():
                shutil.copy2(source_exe, bin_dir / exe_name)
                os.chmod(bin_dir / exe_name, 0o755)
                print(f"✓ Installed to: {bin_dir / exe_name}")
            else:
                print(f"✗ Could not find {exe_name}")
                return False
        
        # Copy icon if available
        icon_file = script_dir / "paprwall.svg"
        if icon_file.exists():
            shutil.copy2(icon_file, icons_dir / "paprwall.svg")
            shutil.copy2(icon_file, data_dir / "paprwall.svg")
            print("✓ Icon installed")
        
        # Copy uninstall script if available
        uninstall_script = script_dir / "uninstall.sh"
        if uninstall_script.exists():
            shutil.copy2(uninstall_script, data_dir / "uninstall.sh")
            os.chmod(data_dir / "uninstall.sh", 0o755)
            print("✓ Uninstall script copied")
        
        # Create desktop entry
        desktop_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=PaprWall
Comment=Modern Desktop Wallpaper Manager
Exec={bin_dir / exe_name}
Icon=paprwall
Terminal=false
Categories=Graphics;Utility;
Keywords=wallpaper;background;image;
"""
        desktop_file = apps_dir / "paprwall.desktop"
        desktop_file.write_text(desktop_entry)
        os.chmod(desktop_file, 0o644)
        print("✓ Desktop entry created")
        
        # Update caches
        try:
            subprocess.run(['gtk-update-icon-cache', '-f', '-t', str(icons_dir.parent.parent)], 
                         stderr=subprocess.DEVNULL, check=False)
            subprocess.run(['update-desktop-database', str(apps_dir)], 
                         stderr=subprocess.DEVNULL, check=False)
            print("✓ System caches updated")
        except Exception:
            pass
        
        print("\n" + "=" * 50)
        print("Installation Complete!")
        print("=" * 50)
        print(f"\nPaprWall has been installed to: {bin_dir / exe_name}")
        print(f"\nYou can now:")
        print("  1. Find 'PaprWall' in your application menu")
        print(f"  2. Run: paprwall-gui")
        print(f"\nTo uninstall later, run:")
        print(f"  {data_dir / 'uninstall.sh'}")
        
        # Check if bin_dir is in PATH
        path_dirs = os.environ.get('PATH', '').split(':')
        if str(bin_dir) not in path_dirs:
            print(f"\n⚠ Note: {bin_dir} is not in your PATH")
            print("Add it by adding this line to your ~/.bashrc or ~/.zshrc:")
            print(f'  export PATH="$HOME/.local/bin:$PATH"')
    
    return True


def uninstall_app_cli():
    """Uninstall PaprWall from the system (CLI mode)."""
    system = platform.system()
    
    if system == "Windows":
        # Run Windows uninstall script
        uninstall_script = Path(os.environ.get('APPDATA')) / "PaprWall" / "UNINSTALL.bat"
        if uninstall_script.exists():
            subprocess.run([str(uninstall_script)], shell=True)
        else:
            print(f"Uninstall script not found at: {uninstall_script}")
            print("\nPlease manually remove PaprWall from:")
            print(f"{os.environ.get('LOCALAPPDATA')}\\Programs\\PaprWall")
            return False
    else:
        # Run Linux uninstall script
        uninstall_script = Path.home() / ".local" / "share" / "paprwall" / "uninstall.sh"
        if uninstall_script.exists():
            subprocess.run(['bash', str(uninstall_script)])
        else:
            print(f"Uninstall script not found at: {uninstall_script}")
            print("\nPlease manually remove PaprWall or run:")
            print("pip uninstall paprwall")
            return False
    
    return True


def main():
    """Launch the GUI application or handle CLI commands."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='PaprWall - Modern Desktop Wallpaper Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  paprwall-gui              # Launch GUI
  paprwall-gui --install    # Install to system
  paprwall-gui --uninstall  # Uninstall from system
        """
    )
    parser.add_argument('--install', action='store_true',
                       help='Install PaprWall to the system')
    parser.add_argument('--uninstall', action='store_true',
                       help='Uninstall PaprWall from the system')
    
    args = parser.parse_args()
    
    # Handle install/uninstall commands
    if args.install:
        sys.exit(0 if install_app() else 1)
    
    if args.uninstall:
        sys.exit(0 if uninstall_app_cli() else 1)
    
    # Launch GUI if no special arguments
    root = tk.Tk()
    app = WallpaperManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()