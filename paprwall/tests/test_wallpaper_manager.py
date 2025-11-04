import unittest
from paprwall.gui.wallpaper_manager_gui import ModernWallpaperGUI

class TestModernWallpaperGUI(unittest.TestCase):
    def setUp(self):
        self.gui = ModernWallpaperGUI()

    def test_initial_state(self):
        self.assertIsNotNone(self.gui.current_wallpaper)
        self.assertIsNotNone(self.gui.current_quote)

    def test_load_image_to_preview(self):
        test_image_path = "path/to/test/image.jpg"  # Replace with a valid test image path
        self.gui.load_image_to_preview(test_image_path)
        self.assertEqual(self.gui.current_wallpaper, test_image_path)

    def test_set_wallpaper(self):
        test_image_path = "path/to/test/image.jpg"  # Replace with a valid test image path
        self.gui.current_wallpaper = test_image_path
        self.gui.set_wallpaper()
        # Add assertions to verify the wallpaper was set correctly

    def test_fetch_random_wallpaper(self):
        self.gui.fetch_random_wallpaper()
        self.assertIsNotNone(self.gui.current_wallpaper)

    def test_refresh_quote_only(self):
        initial_quote = self.gui.current_quote
        self.gui.refresh_quote_only()
        self.assertNotEqual(initial_quote, self.gui.current_quote)

if __name__ == "__main__":
    unittest.main()