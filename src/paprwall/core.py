"""
Core functionality for PaprWall wallpaper operations.
This module provides the backend functionality that can be used by both CLI and GUI.
"""

import os
import sys
import json
import platform
import subprocess
import requests
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from PIL import Image, ImageDraw, ImageFont

from . import DATA_DIR, IMAGES_DIR, CONFIG_DIR


class WallpaperCore:
    """Core wallpaper management functionality."""

    def __init__(self):
        """Initialize the wallpaper core."""
        self.quote_categories = {
            "motivational": "motivational",
            "mathematics": "mathematics",
            "science": "science",
            "famous": "famous-quotes",
            "technology": "technology",
            "philosophy": "philosophy"
        }

        self.quote_apis = [
            "https://api.quotable.io/random",
            "https://zenquotes.io/api/random"
        ]

        self.image_sources = [
            "https://picsum.photos/1920/1080",
            "https://source.unsplash.com/1920x1080/nature"
        ]

    def get_quote(self, category: str = "motivational") -> Dict[str, str]:
        """Fetch a quote from available APIs."""
        quote_data = {"text": "Stay motivated!", "author": "PaprWall"}

        for api_url in self.quote_apis:
            try:
                if "quotable.io" in api_url:
                    params = {"tags": self.quote_categories.get(category, "motivational")}
                    response = requests.get(api_url, params=params, timeout=5)
                elif "zenquotes.io" in api_url:
                    response = requests.get(api_url, timeout=5)
                else:
                    continue

                if response.status_code == 200:
                    data = response.json()
                    if "quotable.io" in api_url:
                        quote_data = {
                            "text": data.get("content", "Stay motivated!"),
                            "author": data.get("author", "Unknown")
                        }
                    elif "zenquotes.io" in api_url and isinstance(data, list) and len(data) > 0:
                        quote_data = {
                            "text": data[0].get("q", "Stay motivated!"),
                            "author": data[0].get("a", "Unknown")
                        }
                    break
            except Exception:
                continue

        return quote_data

    def download_image(self, url: Optional[str] = None) -> Optional[str]:
        """Download an image and return the local path."""
        if url is None:
            url = random.choice(self.image_sources)

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Create unique filename
                import hashlib
                import time
                filename = f"wallpaper_{int(time.time())}_{hashlib.md5(url.encode()).hexdigest()[:8]}.jpg"
                filepath = IMAGES_DIR / filename

                with open(filepath, 'wb') as f:
                    f.write(response.content)

                return str(filepath)
        except Exception as e:
            print(f"Failed to download image: {e}")

        return None

    def add_quote_to_image(self, image_path: str, quote_data: Dict[str, str]) -> str:
        """Add quote overlay to image and return new image path."""
        try:
            # Open image
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)

            # Quote text
            quote_text = f'"{quote_data["text"]}"'
            author_text = f"— {quote_data['author']}"

            # Try to load a nice font
            font_size = 32
            author_font_size = 24
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
                author_font = ImageFont.truetype("arial.ttf", author_font_size)
            except:
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
                    author_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", author_font_size)
                except:
                    font = ImageFont.load_default()
                    author_font = ImageFont.load_default()

            # Calculate text dimensions and position (top-right corner)
            img_width, img_height = image.size

            # Wrap text if too long
            max_width = img_width // 3
            quote_lines = self._wrap_text(quote_text, font, max_width)

            # Calculate total text height
            line_height = font_size + 5
            total_height = len(quote_lines) * line_height + author_font_size + 10

            # Position in top-right with padding
            padding = 50
            start_x = img_width - max_width - padding
            start_y = padding

            # Draw semi-transparent background
            bg_padding = 20
            bg_x1 = start_x - bg_padding
            bg_y1 = start_y - bg_padding
            bg_x2 = img_width - padding + bg_padding
            bg_y2 = start_y + total_height + bg_padding

            # Create overlay for semi-transparent background
            overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rectangle([bg_x1, bg_y1, bg_x2, bg_y2], fill=(0, 0, 0, 128))

            # Composite overlay onto image
            image = image.convert('RGBA')
            image = Image.alpha_composite(image, overlay)
            image = image.convert('RGB')
            draw = ImageDraw.Draw(image)

            # Draw quote text
            y_offset = start_y
            for line in quote_lines:
                draw.text((start_x, y_offset), line, font=font, fill='white')
                y_offset += line_height

            # Draw author
            draw.text((start_x, y_offset + 10), author_text, font=author_font, fill='lightgray')

            # Save the modified image
            output_path = image_path.replace('.jpg', '_with_quote.jpg').replace('.png', '_with_quote.jpg')
            image.save(output_path, 'JPEG', quality=95)

            return output_path

        except Exception as e:
            print(f"Failed to add quote to image: {e}")
            return image_path

    def _wrap_text(self, text: str, font, max_width: int) -> List[str]:
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            if bbox[2] - bbox[0] <= max_width or not current_line:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def set_wallpaper(self, image_path: str) -> bool:
        """Set the wallpaper on the system."""
        try:
            system = platform.system().lower()

            if system == "linux":
                return self._set_wallpaper_linux(image_path)
            elif system == "windows":
                return self._set_wallpaper_windows(image_path)
            elif system == "darwin":
                return self._set_wallpaper_macos(image_path)
            else:
                print(f"Unsupported operating system: {system}")
                return False

        except Exception as e:
            print(f"Failed to set wallpaper: {e}")
            return False

    def _set_wallpaper_linux(self, image_path: str) -> bool:
        """Set wallpaper on Linux."""
        desktop_env = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()

        commands = [
            # GNOME
            ['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', f'file://{image_path}'],
            # KDE
            ['qdbus', 'org.kde.plasmashell', '/PlasmaShell', 'org.kde.PlasmaShell.evaluateScript',
             f"var allDesktops = desktops();for(i=0;i<allDesktops.length;i++){{d=allDesktops[i];d.wallpaperPlugin='org.kde.image';d.currentConfigGroup=Array('Wallpaper','org.kde.image','General');d.writeConfig('Image','file://{image_path}')}}"],
            # XFCE
            ['xfconf-query', '-c', 'xfce4-desktop', '-p', '/backdrop/screen0/monitor0/workspace0/last-image', '-s', image_path],
            # Cinnamon
            ['gsettings', 'set', 'org.cinnamon.desktop.background', 'picture-uri', f'file://{image_path}'],
            # MATE
            ['gsettings', 'set', 'org.mate.background', 'picture-filename', image_path],
        ]

        for cmd in commands:
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=10)
                if result.returncode == 0:
                    return True
            except:
                continue

        # Fallback: try feh if available
        try:
            subprocess.run(['feh', '--bg-scale', image_path], check=True, timeout=10)
            return True
        except:
            pass

        return False

    def _set_wallpaper_windows(self, image_path: str) -> bool:
        """Set wallpaper on Windows."""
        import ctypes
        from ctypes import wintypes

        try:
            # Convert to absolute path
            abs_path = os.path.abspath(image_path)

            # Set wallpaper using Windows API
            result = ctypes.windll.user32.SystemParametersInfoW(
                20,  # SPI_SETDESKWALLPAPER
                0,
                abs_path,
                3  # SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
            )
            return bool(result)
        except Exception:
            return False

    def _set_wallpaper_macos(self, image_path: str) -> bool:
        """Set wallpaper on macOS."""
        try:
            script = f'''
            tell application "Finder"
                set desktop picture to POSIX file "{image_path}"
            end tell
            '''
            subprocess.run(['osascript', '-e', script], check=True, timeout=10)
            return True
        except Exception:
            return False

    def save_to_history(self, image_path: str, quote_data: Dict[str, str]) -> None:
        """Save wallpaper to history."""
        history_file = DATA_DIR / "history.json"

        try:
            if history_file.exists():
                with open(history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []

            # Add new entry
            entry = {
                "timestamp": str(int(time.time())),
                "image_path": image_path,
                "quote": quote_data,
                "datetime": str(datetime.now())
            }

            history.insert(0, entry)  # Add to beginning

            # Keep only last 50 entries
            history = history[:50]

            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)

        except Exception as e:
            print(f"Failed to save to history: {e}")


def set_wallpaper_from_file(file_path: str, add_quote: bool = True, category: str = "motivational") -> int:
    """Set wallpaper from a local file."""
    try:
        core = WallpaperCore()

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return 1

        final_path = file_path
        quote_data = {"text": "", "author": ""}

        if add_quote:
            quote_data = core.get_quote(category)
            final_path = core.add_quote_to_image(file_path, quote_data)

        success = core.set_wallpaper(final_path)
        if success:
            core.save_to_history(final_path, quote_data)
            print(f"Wallpaper set successfully: {final_path}")
            return 0
        else:
            print("Failed to set wallpaper")
            return 1

    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        return 1


def fetch_and_set_wallpaper(category: str = "motivational", add_quote: bool = True) -> int:
    """Fetch a new wallpaper and set it."""
    try:
        core = WallpaperCore()

        print(f"Fetching wallpaper with {category} quote...")

        # Download image
        image_path = core.download_image()
        if not image_path:
            print("Failed to download wallpaper")
            return 1

        final_path = image_path
        quote_data = {"text": "", "author": ""}

        if add_quote:
            quote_data = core.get_quote(category)
            final_path = core.add_quote_to_image(image_path, quote_data)

        success = core.set_wallpaper(final_path)
        if success:
            core.save_to_history(final_path, quote_data)
            print(f"Wallpaper set successfully!")
            if add_quote:
                print(f"Quote: \"{quote_data['text']}\" — {quote_data['author']}")
            return 0
        else:
            print("Failed to set wallpaper")
            return 1

    except Exception as e:
        print(f"Error fetching wallpaper: {e}")
        return 1


if __name__ == "__main__":
    # Test the core functionality
    fetch_and_set_wallpaper()
