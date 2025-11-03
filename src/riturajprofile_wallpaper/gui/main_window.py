"""
Main GUI window for riturajprofile-wallpaper.
"""
import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib

from riturajprofile_wallpaper.config.config_manager import ConfigManager
from riturajprofile_wallpaper.core.rotator import WallpaperRotator
from riturajprofile_wallpaper.utils.logger import setup_logger

logger = setup_logger()


class MainWindow(Gtk.Window):
    """Main application window"""
    
    def __init__(self):
        super().__init__(title="riturajprofile-wallpaper")
        self.set_default_size(800, 600)
        self.set_border_width(10)
        
        # Initialize components
        self.config = ConfigManager()
        self.rotator = WallpaperRotator(self.config)
        
        # Create UI
        self.create_ui()
        
        # Load current wallpaper
        self.refresh_current_image()
    
    def create_ui(self):
        """Create the user interface"""
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        
        # Header
        header = Gtk.Label()
        header.set_markup("<b>riturajprofile-wallpaper</b>")
        vbox.pack_start(header, False, False, 0)
        
        # Current wallpaper preview
        self.image_preview = Gtk.Image()
        self.image_preview.set_from_icon_name("image-x-generic", Gtk.IconSize.DIALOG)
        vbox.pack_start(self.image_preview, True, True, 0)
        
        # Image info label
        self.info_label = Gtk.Label(label="No wallpaper loaded")
        vbox.pack_start(self.info_label, False, False, 0)
        
        # Control buttons
        button_box = Gtk.Box(spacing=5)
        vbox.pack_start(button_box, False, False, 0)
        
        prev_btn = Gtk.Button(label="◄ Previous")
        prev_btn.connect("clicked", self.on_previous)
        button_box.pack_start(prev_btn, True, True, 0)
        
        fetch_btn = Gtk.Button(label="↻ Fetch New")
        fetch_btn.connect("clicked", self.on_fetch)
        button_box.pack_start(fetch_btn, True, True, 0)
        
        next_btn = Gtk.Button(label="Next ►")
        next_btn.connect("clicked", self.on_next)
        button_box.pack_start(next_btn, True, True, 0)
        
        # Status bar
        self.statusbar = Gtk.Statusbar()
        vbox.pack_start(self.statusbar, False, False, 0)
        self.update_status("Ready")
    
    def refresh_current_image(self):
        """Refresh the display of current wallpaper"""
        current = self.rotator.get_current_image()
        
        if current:
            # Update info
            source = current.get('source', 'unknown')
            photographer = current.get('photographer', 'Unknown')
            info_text = f"Photo by {photographer} from {source.capitalize()}\nWallpaper by riturajprofile"
            self.info_label.set_text(info_text)
            
            # Try to load thumbnail
            try:
                path = current.get('local_path') or current.get('path')
                if path:
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        path, 400, 300, True
                    )
                    self.image_preview.set_from_pixbuf(pixbuf)
            except Exception as e:
                logger.error(f"Failed to load image: {e}")
        else:
            self.info_label.set_text("No wallpaper loaded. Click 'Fetch New' to get started.")
    
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
