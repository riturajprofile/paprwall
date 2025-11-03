"""
Comprehensive CLI for Wallpaper Manager
Provides command-line interface for all wallpaper operations
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import requests
from paprwall.gui.wallpaper_manager_gui import WallpaperManagerGUI


class WallpaperCLI:
    """Command-line interface for wallpaper management."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.data_dir = Path.home() / ".paprwall"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.data_dir / "history.json"
        self.wallpapers_dir = self.data_dir / "wallpapers"
        self.wallpapers_dir.mkdir(exist_ok=True)
    
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
    
    def save_history(self, history):
        """Save wallpaper history to JSON file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving history: {e}")
            return False
    
    def add_to_history(self, image_path):
        """Add image to history."""
        history = self.load_history()
        
        entry = {
            "path": os.path.abspath(image_path),
            "timestamp": datetime.now().isoformat(),
            "filename": os.path.basename(image_path)
        }
        
        # Remove if already in history
        history = [h for h in history if h.get("path") != entry["path"]]
        
        # Add to front
        history.insert(0, entry)
        
        # Keep only last 5
        history = history[:5]
        
        # Save
        return self.save_history(history)
    
    def set_wallpaper(self, image_path):
        """Set wallpaper using platform-specific method."""
        import platform
        import subprocess
        
        if not os.path.exists(image_path):
            print(f"❌ Error: Image file not found: {image_path}")
            return False
        
        image_path = os.path.abspath(image_path)
        system = platform.system()
        
        try:
            if system == "Windows":
                import ctypes
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
                
            elif system == "Darwin":  # macOS
                script = f'''
                tell application "System Events"
                    tell every desktop
                        set picture to "{image_path}"
                    end tell
                end tell
                '''
                subprocess.run(["osascript", "-e", script], check=True)
                
            elif system == "Linux":
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
                
                # If gsettings worked, continue to add history
                if success:
                    pass  # Will add to history below
                
                # GNOME (fallback if gsettings didn't work)
                elif 'gnome' in desktop or os.environ.get('GNOME_DESKTOP_SESSION_ID'):
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
                
                # XFCE
                elif 'xfce' in desktop:
                    subprocess.run([
                        "xfconf-query", "-c", "xfce4-desktop",
                        "-p", "/backdrop/screen0/monitor0/workspace0/last-image",
                        "-s", image_path
                    ], check=True)
                
                # Fallback: try feh
                else:
                    subprocess.run(["feh", "--bg-scale", image_path], check=True)
            
            # Add to history
            self.add_to_history(image_path)
            print(f"✅ Wallpaper set successfully: {os.path.basename(image_path)}")
            return True
            
        except Exception as e:
            print(f"❌ Error setting wallpaper: {e}")
            return False
    
    def set_from_url(self, url):
        """Download image from URL and set as wallpaper."""
        print(f"📥 Downloading image from URL...")
        
        try:
            # Download image
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Check if it's an image
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type.lower():
                print("❌ Error: URL does not point to an image")
                return False
            
            # Save to wallpapers directory
            filename = f"wallpaper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            temp_path = self.wallpapers_dir / filename
            
            with open(temp_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Image downloaded: {filename}")
            
            # Set as wallpaper
            return self.set_wallpaper(str(temp_path))
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Download failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def set_from_file(self, file_path):
        """Set wallpaper from local file."""
        return self.set_wallpaper(file_path)
    
    def list_history(self):
        """List wallpaper history."""
        history = self.load_history()
        
        if not history:
            print("📋 No wallpaper history")
            return
        
        print("\n📋 Recent Wallpapers (last 5):")
        print("=" * 80)
        
        for idx, item in enumerate(history, 1):
            print(f"\n  [{idx}] {item['filename']}")
            print(f"      Path: {item['path']}")
            print(f"      Set at: {item['timestamp'][:19]}")
            
            # Check if file still exists
            if not os.path.exists(item['path']):
                print(f"      ⚠️  File no longer exists")
        
        print("\n" + "=" * 80)
        print("💡 Set from history: wallpaper-manager --set-from-history <INDEX>")
    
    def set_from_history(self, index):
        """Set wallpaper from history by index."""
        history = self.load_history()
        
        if not history:
            print("❌ No wallpaper history")
            return False
        
        if index < 1 or index > len(history):
            print(f"❌ Invalid index. Please use 1-{len(history)}")
            return False
        
        item = history[index - 1]
        
        if not os.path.exists(item['path']):
            print(f"❌ File no longer exists: {item['path']}")
            return False
        
        print(f"🖼️  Setting wallpaper from history: {item['filename']}")
        return self.set_wallpaper(item['path'])
    
    def clear_history(self):
        """Clear wallpaper history."""
        try:
            self.save_history([])
            print("✅ History cleared")
            return True
        except Exception as e:
            print(f"❌ Error clearing history: {e}")
            return False
    
    def launch_gui(self):
        """Launch the GUI application."""
        print("🚀 Launching GUI...")
        import tkinter as tk
        root = tk.Tk()
        app = WallpaperManagerGUI(root)
        root.mainloop()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Wallpaper Manager - Set and manage desktop wallpapers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --gui                                    # Launch GUI
  %(prog)s --set-url https://example.com/image.jpg  # Set from URL
  %(prog)s --set-file ~/Pictures/wallpaper.jpg      # Set from local file
  %(prog)s --list-history                           # Show history
  %(prog)s --set-from-history 1                     # Set from history
  %(prog)s --clear-history                          # Clear history
        """
    )
    
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Launch GUI mode'
    )
    
    parser.add_argument(
        '--set-url',
        metavar='URL',
        help='Download and set wallpaper from URL'
    )
    
    parser.add_argument(
        '--set-file',
        metavar='PATH',
        help='Set wallpaper from local file'
    )
    
    parser.add_argument(
        '--list-history',
        action='store_true',
        help='Show last 5 wallpapers'
    )
    
    parser.add_argument(
        '--set-from-history',
        type=int,
        metavar='INDEX',
        help='Set wallpaper from history (1-5)'
    )
    
    parser.add_argument(
        '--clear-history',
        action='store_true',
        help='Clear wallpaper history'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Wallpaper Manager 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = WallpaperCLI()
    
    # Handle commands
    if args.gui:
        cli.launch_gui()
        return 0
    
    elif args.set_url:
        success = cli.set_from_url(args.set_url)
        return 0 if success else 1
    
    elif args.set_file:
        success = cli.set_from_file(args.set_file)
        return 0 if success else 1
    
    elif args.list_history:
        cli.list_history()
        return 0
    
    elif args.set_from_history is not None:
        success = cli.set_from_history(args.set_from_history)
        return 0 if success else 1
    
    elif args.clear_history:
        success = cli.clear_history()
        return 0 if success else 1
    
    else:
        # No arguments - show help
        parser.print_help()
        return 0


if __name__ == '__main__':
    sys.exit(main())
