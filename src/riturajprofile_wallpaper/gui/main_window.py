"""
Main GUI window for riturajprofile-wallpaper.
"""
import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk

from riturajprofile_wallpaper.config.config_manager import ConfigManager
from riturajprofile_wallpaper.core.rotator import WallpaperRotator
from riturajprofile_wallpaper.utils.logger import setup_logger

logger = setup_logger()


class MainWindow(Gtk.Window):
    """Main application window"""
    
    def __init__(self):
        super().__init__(title="Paprwall - Wallpaper Manager")
        self.set_default_size(900, 700)
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
        """Apply custom CSS styling"""
        css_provider = Gtk.CssProvider()
        css = b"""
        window {
            background-color: #f5f5f5;
        }
        
        .header-bar {
            background: linear-gradient(to bottom, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 8px 8px 0 0;
        }
        
        .header-title {
            font-size: 24px;
            font-weight: bold;
            color: white;
        }
        
        .header-subtitle {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.9);
        }
        
        .preview-frame {
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .info-box {
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        
        .photographer-label {
            font-size: 14px;
            color: #333;
        }
        
        .source-label {
            font-size: 12px;
            color: #666;
        }
        
        button {
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            min-height: 40px;
        }
        
        .primary-button {
            background: linear-gradient(to bottom, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
        }
        
        .primary-button:hover {
            background: linear-gradient(to bottom, #5568d3 0%, #65398b 100%);
        }
        
        .secondary-button {
            background-color: white;
            color: #667eea;
            border: 2px solid #667eea;
        }
        
        .secondary-button:hover {
            background-color: #f0f0f0;
        }
        
        .status-bar {
            background-color: white;
            border-top: 1px solid #e0e0e0;
            padding: 8px 15px;
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
        """Create the user interface"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)
        
        # Header with gradient
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        header_box.get_style_context().add_class("header-bar")
        main_box.pack_start(header_box, False, False, 0)
        
        title = Gtk.Label()
        title.set_markup('<span class="header-title">🖼️ Paprwall</span>')
        title.get_style_context().add_class("header-title")
        header_box.pack_start(title, False, False, 0)
        
        subtitle = Gtk.Label(label="Automatic Wallpaper Manager")
        subtitle.get_style_context().add_class("header-subtitle")
        header_box.pack_start(subtitle, False, False, 0)
        
        # Content area with padding
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        content_box.set_margin_top(20)
        content_box.set_margin_bottom(20)
        content_box.set_margin_start(20)
        content_box.set_margin_end(20)
        main_box.pack_start(content_box, True, True, 0)
        
        # Preview frame
        preview_frame = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        preview_frame.get_style_context().add_class("preview-frame")
        content_box.pack_start(preview_frame, True, True, 0)
        
        self.image_preview = Gtk.Image()
        self.image_preview.set_from_icon_name("image-x-generic", Gtk.IconSize.DIALOG)
        self.image_preview.set_size_request(600, 400)
        preview_frame.pack_start(self.image_preview, True, True, 0)
        
        # Info box
        info_frame = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        info_frame.get_style_context().add_class("info-box")
        content_box.pack_start(info_frame, False, False, 0)
        
        self.photographer_label = Gtk.Label()
        self.photographer_label.set_markup('<span class="photographer-label">📸 No wallpaper loaded</span>')
        self.photographer_label.get_style_context().add_class("photographer-label")
        self.photographer_label.set_xalign(0)
        info_frame.pack_start(self.photographer_label, False, False, 0)
        
        self.source_label = Gtk.Label()
        self.source_label.set_markup('<span class="source-label">Click "Fetch New" to get started</span>')
        self.source_label.get_style_context().add_class("source-label")
        self.source_label.set_xalign(0)
        info_frame.pack_start(self.source_label, False, False, 0)
        
        # Control buttons with better layout
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_homogeneous(True)
        content_box.pack_start(button_box, False, False, 0)
        
        prev_btn = Gtk.Button(label="◄ Previous")
        prev_btn.get_style_context().add_class("secondary-button")
        prev_btn.connect("clicked", self.on_previous)
        button_box.pack_start(prev_btn, True, True, 0)
        
        fetch_btn = Gtk.Button(label="↻ Fetch New")
        fetch_btn.get_style_context().add_class("primary-button")
        fetch_btn.connect("clicked", self.on_fetch)
        button_box.pack_start(fetch_btn, True, True, 0)
        
        next_btn = Gtk.Button(label="Next ►")
        next_btn.get_style_context().add_class("secondary-button")
        next_btn.connect("clicked", self.on_next)
        button_box.pack_start(next_btn, True, True, 0)
        
        # Status bar
        self.statusbar = Gtk.Statusbar()
        self.statusbar.get_style_context().add_class("status-bar")
        main_box.pack_start(self.statusbar, False, False, 0)
        self.update_status("Ready")
    
    def refresh_current_image(self):
        """Refresh the display of current wallpaper"""
        current = self.rotator.get_current_image()
        
        if current:
            # Update info
            source = current.get('source', 'unknown')
            photographer = current.get('photographer', 'Unknown')
            
            photographer_text = f'<span class="photographer-label">📸 Photo by <b>{photographer}</b></span>'
            self.photographer_label.set_markup(photographer_text)
            
            source_text = f'<span class="source-label">Source: {source.capitalize()} • Curated by riturajprofile</span>'
            self.source_label.set_markup(source_text)
            
            # Try to load thumbnail with better scaling
            try:
                path = current.get('local_path') or current.get('path')
                if path:
                    # Load with aspect ratio preserved
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
                    
                    # Calculate scaling to fit nicely
                    orig_width = pixbuf.get_width()
                    orig_height = pixbuf.get_height()
                    target_width = 600
                    target_height = 400
                    
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
            self.photographer_label.set_markup('<span class="photographer-label">📸 No wallpaper loaded</span>')
            self.source_label.set_markup('<span class="source-label">Click "Fetch New" to download beautiful wallpapers</span>')
            self.image_preview.set_from_icon_name("image-x-generic", Gtk.IconSize.DIALOG)
    
    def on_previous(self, button):
        """Handle previous button click"""
        self.update_status("Switching to previous wallpaper...")
        if self.rotator.previous():
            self.refresh_current_image()
            self.update_status("Switched to previous wallpaper")
        else:
            self.update_status("Failed to switch wallpaper")
    
    def on_next(self, button):
        """Handle next button click"""
        self.update_status("Switching to next wallpaper...")
        if self.rotator.next():
            self.refresh_current_image()
            self.update_status("Switched to next wallpaper")
        else:
            self.update_status("Failed to switch wallpaper")
    
    def on_fetch(self, button):
        """Handle fetch new button click"""
        self.update_status("Fetching new wallpapers... This may take a moment.")
        
        # Run fetch in background to keep UI responsive
        def fetch_task():
            result = self.rotator.fetch_and_rotate()
            GLib.idle_add(self.on_fetch_complete, result)
        
        import threading
        thread = threading.Thread(target=fetch_task)
        thread.daemon = True
        thread.start()
    
    def on_fetch_complete(self, success):
        """Handle fetch completion"""
        if success:
            self.refresh_current_image()
            self.update_status("Successfully fetched new wallpapers")
        else:
            self.update_status("Failed to fetch wallpapers. Check your API keys.")
        return False
    
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
        return 1


if __name__ == '__main__':
    sys.exit(main())
