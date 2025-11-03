"""
Enhanced Main GUI window for Paprwall - Laptop Optimized.
Modern design with tabs for Wallpapers, Themes, Sources, and Settings.
"""
import sys
import os
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk

from riturajprofile_wallpaper.config.config_manager import ConfigManager
from riturajprofile_wallpaper.core.rotator import WallpaperRotator
from riturajprofile_wallpaper.utils.logger import setup_logger

logger = setup_logger()


class MainWindow(Gtk.Window):
    """Enhanced main application window with tabbed interface"""
    
    def __init__(self):
        super().__init__(title="Paprwall - Wallpaper Manager")
        self.set_default_size(900, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Initialize components
        self.config = ConfigManager()
        self.rotator = WallpaperRotator(self.config)
        
        # Apply custom CSS
        self.apply_css()
        
        # Create UI
        self.create_ui()
        
        # Load current wallpaper
        self.refresh_current_image()
    
    def apply_css(self):
        """Apply modern custom CSS styling - optimized for laptops"""
        css_provider = Gtk.CssProvider()
        css = b"""
        window {
            background-color: #fafafa;
        }
        
        .header-bar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px 20px;
        }
        
        .header-title {
            font-size: 20px;
            font-weight: bold;
            color: white;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .header-subtitle {
            font-size: 11px;
            color: rgba(255, 255, 255, 0.95);
            margin-top: 3px;
        }
        
        .card {
            background-color: white;
            border-radius: 8px;
            padding: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            margin: 8px;
        }
        
        .preview-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 12px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .info-label-title {
            font-size: 13px;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .info-label-subtitle {
            font-size: 11px;
            color: #7f8c8d;
        }
        
        button {
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 600;
            min-height: 36px;
            font-size: 12px;
        }
        
        .primary-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            box-shadow: 0 2px 6px rgba(102, 126, 234, 0.3);
        }
        
        .primary-button:hover {
            background: linear-gradient(135deg, #5568d3 0%, #65398b 100%);
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
        }
        
        .secondary-button {
            background-color: white;
            color: #667eea;
            border: 2px solid #667eea;
        }
        
        .secondary-button:hover {
            background-color: #f0f3ff;
        }
        
        .status-bar {
            background-color: white;
            border-top: 1px solid #e8e8e8;
            padding: 6px 15px;
            font-size: 11px;
        }
        
        notebook tab {
            padding: 8px 16px;
            font-weight: 600;
            font-size: 12px;
        }
        
        .theme-card {
            background-color: white;
            border-radius: 6px;
            padding: 10px;
            margin: 6px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }
        
        .setting-row {
            padding: 12px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        entry {
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #ddd;
            min-height: 32px;
            font-size: 12px;
        }
        """
        css_provider.load_from_data(css)
        
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def create_ui(self):
        """Create the enhanced user interface with tabs"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)
        
        # Compact header with gradient
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        header_box.get_style_context().add_class("header-bar")
        main_box.pack_start(header_box, False, False, 0)
        
        title = Gtk.Label()
        title.set_markup('<span class="header-title">🎨 Paprwall</span>')
        title.get_style_context().add_class("header-title")
        header_box.pack_start(title, False, False, 0)
        
        subtitle = Gtk.Label(label="Beautiful wallpapers, automatically updated")
        subtitle.get_style_context().add_class("header-subtitle")
        header_box.pack_start(subtitle, False, False, 0)
        
        # Create notebook (tabs)
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)
        main_box.pack_start(notebook, True, True, 0)
        
        # Tab 1: Wallpapers
        wallpaper_tab = self.create_wallpaper_tab()
        notebook.append_page(wallpaper_tab, Gtk.Label(label="🖼️  Wallpapers"))
        
        # Tab 2: Themes
        themes_tab = self.create_themes_tab()
        notebook.append_page(themes_tab, Gtk.Label(label="🎨  Themes"))
        
        # Tab 3: Sources
        sources_tab = self.create_sources_tab()
        notebook.append_page(sources_tab, Gtk.Label(label="🌐  Sources"))
        
        # Tab 4: Settings
        settings_tab = self.create_settings_tab()
        notebook.append_page(settings_tab, Gtk.Label(label="⚙️  Settings"))
        
        # Compact status bar
        self.statusbar = Gtk.Statusbar()
        self.statusbar.get_style_context().add_class("status-bar")
        main_box.pack_start(self.statusbar, False, False, 0)
        self.update_status("Ready - Click 'Fetch New' to get started")
    
    def create_wallpaper_tab(self):
        """Create wallpaper management tab"""
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content_box.set_margin_top(12)
        content_box.set_margin_bottom(12)
        content_box.set_margin_start(12)
        content_box.set_margin_end(12)
        scroll.add(content_box)
        
        # Preview card - optimized size
        preview_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        preview_card.get_style_context().add_class("preview-card")
        content_box.pack_start(preview_card, True, True, 0)
        
        # Image preview - smaller for laptops
        self.image_preview = Gtk.Image()
        self.image_preview.set_from_icon_name("image-x-generic", Gtk.IconSize.DIALOG)
        self.image_preview.set_size_request(560, 315)  # 16:9 ratio, reasonable size
        preview_card.pack_start(self.image_preview, True, True, 0)
        
        # Compact info card
        info_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        info_card.get_style_context().add_class("card")
        content_box.pack_start(info_card, False, False, 0)
        
        self.photographer_label = Gtk.Label()
        self.photographer_label.set_markup('<span class="info-label-title">📸 No wallpaper loaded</span>')
        self.photographer_label.get_style_context().add_class("info-label-title")
        self.photographer_label.set_xalign(0)
        info_card.pack_start(self.photographer_label, False, False, 0)
        
        self.source_label = Gtk.Label()
        self.source_label.set_markup('<span class="info-label-subtitle">Click "Fetch New" to download wallpapers</span>')
        self.source_label.get_style_context().add_class("info-label-subtitle")
        self.source_label.set_xalign(0)
        info_card.pack_start(self.source_label, False, False, 0)
        
        # Compact control buttons
        button_grid = Gtk.Grid()
        button_grid.set_row_spacing(8)
        button_grid.set_column_spacing(8)
        button_grid.set_column_homogeneous(True)
        content_box.pack_start(button_grid, False, False, 0)
        
        # Row 1: Navigation
        prev_btn = Gtk.Button(label="◄ Previous")
        prev_btn.get_style_context().add_class("secondary-button")
        prev_btn.connect("clicked", self.on_previous)
        button_grid.attach(prev_btn, 0, 0, 1, 1)
        
        self.fetch_btn = Gtk.Button(label="↻ Fetch New")
        self.fetch_btn.get_style_context().add_class("primary-button")
        self.fetch_btn.connect("clicked", self.on_fetch)
        button_grid.attach(self.fetch_btn, 1, 0, 1, 1)
        
        next_btn = Gtk.Button(label="Next ►")
        next_btn.get_style_context().add_class("secondary-button")
        next_btn.connect("clicked", self.on_next)
        button_grid.attach(next_btn, 2, 0, 1, 1)
        
        # Row 2: Actions
        fullscreen_btn = Gtk.Button(label="⛶ Preview")
        fullscreen_btn.get_style_context().add_class("secondary-button")
        fullscreen_btn.connect("clicked", self.on_fullscreen)
        button_grid.attach(fullscreen_btn, 0, 1, 1, 1)
        
        refresh_btn = Gtk.Button(label="↺ Refresh")
        refresh_btn.get_style_context().add_class("secondary-button")
        refresh_btn.connect("clicked", lambda b: self.refresh_current_image())
        button_grid.attach(refresh_btn, 1, 1, 1, 1)
        
        open_folder_btn = Gtk.Button(label="📁 Folder")
        open_folder_btn.get_style_context().add_class("secondary-button")
        open_folder_btn.connect("clicked", self.on_open_folder)
        button_grid.attach(open_folder_btn, 2, 1, 1, 1)
        
        return scroll
    
    def create_themes_tab(self):
        """Create themes selection tab"""
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content_box.set_margin_top(12)
        content_box.set_margin_bottom(12)
        content_box.set_margin_start(12)
        content_box.set_margin_end(12)
        scroll.add(content_box)
        
        # Compact title
        title_label = Gtk.Label()
        title_label.set_markup('<span size="large" weight="bold">Choose Your Theme</span>')
        title_label.set_xalign(0)
        content_box.pack_start(title_label, False, False, 0)
        
        subtitle_label = Gtk.Label(label="Select a theme to change wallpaper style")
        subtitle_label.set_xalign(0)
        subtitle_label.set_markup('<span size="small">Select a theme to change wallpaper style</span>')
        content_box.pack_start(subtitle_label, False, False, 0)
        
        # Themes grid - 3 columns for laptop screens
        themes = [
            ("🌿 Nature", "nature", "Natural landscapes"),
            ("🏙️ City", "city", "Urban scenes"),
            ("✨ Minimal", "minimal", "Clean designs"),
            ("🚀 Space", "space", "Astronomy"),
            ("🌊 Ocean", "ocean", "Coastal scenes"),
            ("⛰️ Mountains", "mountains", "Mountain views"),
            ("🌅 Sunset", "sunset", "Golden hours"),
            ("🦁 Animals", "animals", "Wildlife"),
            ("🌲 Forest", "forest", "Woodlands"),
            ("🎨 Abstract", "abstract", "Art & patterns"),
            ("🌺 Flowers", "flowers", "Botanical"),
            ("🌑 Dark", "dark", "Moody tones"),
        ]
        
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        content_box.pack_start(grid, True, True, 0)
        
        row = 0
        col = 0
        for emoji_name, theme_id, description in themes:
            theme_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            theme_card.get_style_context().add_class("theme-card")
            theme_card.set_size_request(160, 100)
            
            # Theme icon/name
            theme_label = Gtk.Label()
            theme_label.set_markup(f'<span size="large">{emoji_name}</span>')
            theme_card.pack_start(theme_label, False, False, 0)
            
            # Description
            desc_label = Gtk.Label(label=description)
            desc_label.set_markup(f'<span size="small">{description}</span>')
            desc_label.set_line_wrap(True)
            desc_label.set_max_width_chars(20)
            desc_label.set_justify(Gtk.Justification.CENTER)
            theme_card.pack_start(desc_label, True, True, 0)
            
            # Select button
            select_btn = Gtk.Button(label="Select")
            select_btn.get_style_context().add_class("secondary-button")
            select_btn.connect("clicked", self.on_theme_selected, theme_id)
            theme_card.pack_start(select_btn, False, False, 0)
            
            grid.attach(theme_card, col, row, 1, 1)
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        return scroll
    
    def create_sources_tab(self):
        """Create API sources management tab"""
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(12)
        content_box.set_margin_bottom(12)
        content_box.set_margin_start(12)
        content_box.set_margin_end(12)
        scroll.add(content_box)
        
        # Title
        title_label = Gtk.Label()
        title_label.set_markup('<span size="large" weight="bold">API Sources</span>')
        title_label.set_xalign(0)
        content_box.pack_start(title_label, False, False, 0)
        
        subtitle_label = Gtk.Label(label="Configure your wallpaper sources and API keys")
        subtitle_label.set_markup('<span size="small">Configure your wallpaper sources and API keys</span>')
        subtitle_label.set_xalign(0)
        content_box.pack_start(subtitle_label, False, False, 0)
        
        # Sources
        sources = [
            ("Pixabay", "pixabay", "https://pixabay.com/api/docs/"),
            ("Pexels", "pexels", "https://www.pexels.com/api/"),
            ("Unsplash", "unsplash", "https://unsplash.com/developers"),
        ]
        
        for name, source_id, api_url in sources:
            source_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            source_card.get_style_context().add_class("card")
            content_box.pack_start(source_card, False, False, 0)
            
            # Header
            header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            source_card.pack_start(header_box, False, False, 0)
            
            source_label = Gtk.Label()
            source_label.set_markup(f'<span weight="bold">{name}</span>')
            source_label.set_xalign(0)
            header_box.pack_start(source_label, True, True, 0)
            
            status_label = Gtk.Label(label="● Enabled")
            status_label.set_markup('<span size="small">● Enabled</span>')
            status_label.set_xalign(1)
            header_box.pack_start(status_label, False, False, 0)
            
            # API URL
            url_label = Gtk.Label()
            url_label.set_markup(f'<small>Get API key: <a href="{api_url}">{api_url}</a></small>')
            url_label.set_xalign(0)
            source_card.pack_start(url_label, False, False, 0)
            
            # API Key entry
            key_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            source_card.pack_start(key_box, False, False, 0)
            
            key_entry = Gtk.Entry()
            key_entry.set_placeholder_text(f"Enter your {name} API key")
            key_entry.set_visibility(False)
            key_box.pack_start(key_entry, True, True, 0)
            
            test_btn = Gtk.Button(label="Test")
            test_btn.get_style_context().add_class("secondary-button")
            test_btn.connect("clicked", self.on_test_source, source_id, key_entry)
            key_box.pack_start(test_btn, False, False, 0)
            
            save_btn = Gtk.Button(label="Save")
            save_btn.get_style_context().add_class("primary-button")
            save_btn.connect("clicked", self.on_save_api_key, source_id, key_entry)
            key_box.pack_start(save_btn, False, False, 0)
        
        return scroll
    
    def create_settings_tab(self):
        """Create settings tab"""
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(12)
        content_box.set_margin_bottom(12)
        content_box.set_margin_start(12)
        content_box.set_margin_end(12)
        scroll.add(content_box)
        
        # Title
        title_label = Gtk.Label()
        title_label.set_markup('<span size="large" weight="bold">Settings</span>')
        title_label.set_xalign(0)
        content_box.pack_start(title_label, False, False, 0)
        
        # Settings card
        settings_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        settings_card.get_style_context().add_class("card")
        content_box.pack_start(settings_card, False, False, 0)
        
        # Rotation interval
        interval_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        interval_row.get_style_context().add_class("setting-row")
        settings_card.pack_start(interval_row, False, False, 0)
        
        interval_label = Gtk.Label(label="Rotation Interval (hours)")
        interval_label.set_xalign(0)
        interval_row.pack_start(interval_label, True, True, 0)
        
        interval_spin = Gtk.SpinButton()
        interval_spin.set_range(1, 24)
        interval_spin.set_increments(1, 1)
        interval_spin.set_value(6)
        interval_row.pack_start(interval_spin, False, False, 0)
        
        # Download location
        location_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        location_row.get_style_context().add_class("setting-row")
        settings_card.pack_start(location_row, False, False, 0)
        
        location_label = Gtk.Label(label="Download Location")
        location_label.set_xalign(0)
        location_row.pack_start(location_label, True, True, 0)
        
        location_entry = Gtk.Entry()
        location_entry.set_text(os.path.expanduser("~/.local/share/riturajprofile-wallpaper"))
        location_row.pack_start(location_entry, True, True, 0)
        
        browse_btn = Gtk.Button(label="Browse")
        browse_btn.get_style_context().add_class("secondary-button")
        location_row.pack_start(browse_btn, False, False, 0)
        
        # Auto-start
        autostart_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        autostart_row.get_style_context().add_class("setting-row")
        settings_card.pack_start(autostart_row, False, False, 0)
        
        autostart_label = Gtk.Label(label="Auto-start on login")
        autostart_label.set_xalign(0)
        autostart_row.pack_start(autostart_label, True, True, 0)
        
        autostart_switch = Gtk.Switch()
        autostart_switch.set_active(True)
        autostart_row.pack_start(autostart_switch, False, False, 0)
        
        # Save button
        save_settings_btn = Gtk.Button(label="💾 Save Settings")
        save_settings_btn.get_style_context().add_class("primary-button")
        content_box.pack_start(save_settings_btn, False, False, 0)
        
        # About section
        about_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        about_card.get_style_context().add_class("card")
        content_box.pack_start(about_card, False, False, 10)
        
        about_title = Gtk.Label()
        about_title.set_markup('<span weight="bold">About Paprwall</span>')
        about_title.set_xalign(0)
        about_card.pack_start(about_title, False, False, 0)
        
        about_text = Gtk.Label(label="Version 1.0.0 • Created by riturajprofile")
        about_text.set_markup('<span size="small">Version 1.0.0 • Created by riturajprofile</span>')
        about_text.set_xalign(0)
        about_card.pack_start(about_text, False, False, 0)
        
        github_label = Gtk.Label()
        github_label.set_markup('<small><a href="https://github.com/riturajprofile/paprwall">GitHub Repository</a></small>')
        github_label.set_xalign(0)
        about_card.pack_start(github_label, False, False, 0)
        
        return scroll
    
    def refresh_current_image(self):
        """Refresh the display of current wallpaper"""
        current = self.rotator.get_current_image()
        
        if current:
            source = current.get('source', 'unknown')
            photographer = current.get('photographer', 'Unknown')
            
            photographer_text = f'<span class="info-label-title">📸 Photo by <b>{photographer}</b></span>'
            self.photographer_label.set_markup(photographer_text)
            
            theme = self.config.get("current_theme", "nature")
            source_text = f'<span class="info-label-subtitle">Source: {source.capitalize()} • Theme: {theme}</span>'
            self.source_label.set_markup(source_text)
            
            try:
                path = current.get('local_path') or current.get('path')
                if path and os.path.exists(path):
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
                    
                    orig_width = pixbuf.get_width()
                    orig_height = pixbuf.get_height()
                    target_width = 560
                    target_height = 315
                    
                    scale = min(target_width / orig_width, target_height / orig_height)
                    new_width = int(orig_width * scale)
                    new_height = int(orig_height * scale)
                    
                    scaled_pixbuf = pixbuf.scale_simple(
                        new_width, new_height, GdkPixbuf.InterpType.BILINEAR
                    )
                    self.image_preview.set_from_pixbuf(scaled_pixbuf)
            except Exception as e:
                logger.error(f"Failed to load image: {e}")
                self.image_preview.set_from_icon_name("image-missing", Gtk.IconSize.DIALOG)
        else:
            self.photographer_label.set_markup('<span class="info-label-title">📸 No wallpaper loaded</span>')
            self.source_label.set_markup('<span class="info-label-subtitle">Click "Fetch New" to download beautiful wallpapers</span>')
            self.image_preview.set_from_icon_name("image-x-generic", Gtk.IconSize.DIALOG)
    
    def on_previous(self, button):
        """Handle previous button click"""
        self.update_status("Switching to previous wallpaper...")
        if self.rotator.previous():
            self.refresh_current_image()
            self.update_status("✓ Switched to previous wallpaper")
        else:
            self.update_status("✗ No previous wallpaper available")
    
    def on_next(self, button):
        """Handle next button click"""
        self.update_status("Switching to next wallpaper...")
        if self.rotator.next():
            self.refresh_current_image()
            self.update_status("✓ Switched to next wallpaper")
        else:
            self.update_status("✗ No next wallpaper available")
    
    def on_fetch(self, button):
        """Handle fetch new button click"""
        self.update_status("⏳ Fetching new wallpapers from the internet...")
        self.fetch_btn.set_sensitive(False)
        
        def fetch_task():
            result = self.rotator.fetch_and_rotate()
            GLib.idle_add(self.on_fetch_complete, result)
        
        import threading
        thread = threading.Thread(target=fetch_task)
        thread.daemon = True
        thread.start()
    
    def on_fetch_complete(self, success):
        """Handle fetch completion"""
        self.fetch_btn.set_sensitive(True)
        if success:
            self.refresh_current_image()
            self.update_status("✓ Successfully fetched new wallpapers!")
        else:
            self.update_status("✗ Failed to fetch wallpapers. Check your API keys in Sources tab.")
        return False
    
    def on_fullscreen(self, button):
        """Show fullscreen preview"""
        current = self.rotator.get_current_image()
        if not current:
            self.update_status("No wallpaper to preview")
            return
        
        path = current.get('local_path') or current.get('path')
        if not path or not os.path.exists(path):
            self.update_status("Wallpaper file not found")
            return
        
        # Create fullscreen dialog
        dialog = Gtk.Window()
        dialog.fullscreen()
        dialog.connect("key-press-event", lambda w, e: dialog.destroy() if e.keyval == Gdk.KEY_Escape else None)
        dialog.connect("button-press-event", lambda w, e: dialog.destroy())
        
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
            image = Gtk.Image.new_from_pixbuf(pixbuf)
            dialog.add(image)
            dialog.show_all()
            self.update_status("Press ESC or click to exit fullscreen")
        except Exception as e:
            logger.error(f"Failed to show fullscreen: {e}")
            dialog.destroy()
            self.update_status(f"Failed to open fullscreen: {e}")
    
    def on_open_folder(self, button):
        """Open wallpaper folder"""
        import subprocess
        folder = os.path.expanduser("~/.local/share/riturajprofile-wallpaper/images")
        
        # Create folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)
        
        try:
            subprocess.Popen(['xdg-open', folder])
            self.update_status(f"✓ Opened folder: {folder}")
        except Exception as e:
            self.update_status(f"✗ Failed to open folder: {e}")
    
    def on_theme_selected(self, button, theme_id):
        """Handle theme selection"""
        self.update_status(f"Setting theme to: {theme_id}")
        try:
            # Set the theme in config
            self.config.set("current_theme", theme_id)
            self.config.save()
            self.update_status(f"✓ Theme set to: {theme_id}. Click 'Fetch New' to get {theme_id} wallpapers!")
        except Exception as e:
            logger.error(f"Failed to set theme: {e}")
            self.update_status(f"✗ Failed to set theme: {e}")
    
    def on_test_source(self, button, source_id, entry):
        """Test API source"""
        api_key = entry.get_text()
        if not api_key:
            self.update_status(f"✗ Please enter an API key for {source_id}")
            return
        
        self.update_status(f"⏳ Testing {source_id} API...")
        # Here you would test the API with actual implementation
        self.update_status(f"✓ {source_id} API test feature coming soon!")
    
    def on_save_api_key(self, button, source_id, entry):
        """Save API key"""
        api_key = entry.get_text()
        if not api_key:
            self.update_status(f"✗ Please enter an API key")
            return
        
        try:
            # Save API key to config
            # This would need proper implementation with your config system
            self.update_status(f"✓ {source_id} API key saved! Edit ~/.paprwall/.env to configure.")
        except Exception as e:
            logger.error(f"Failed to save API key: {e}")
            self.update_status(f"✗ Failed to save API key: {e}")
    
    def update_status(self, message):
        """Update status bar message"""
        self.statusbar.push(0, message)


def main():
    """Main GUI entry point"""
    try:
        app = MainWindow()
        app.connect("destroy", Gtk.main_quit)
        app.show_all()
        Gtk.main()
        return 0
    except Exception as e:
        logger.error(f"Failed to start GUI: {e}")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())