"""
Basic functionality tests for PaprWall core module.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from paprwall.core import (
    WallpaperCore,
    set_wallpaper_from_file,
    fetch_and_set_wallpaper,
)


class TestWallpaperCore:
    """Test the WallpaperCore class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.core = WallpaperCore()

    def test_init(self):
        """Test WallpaperCore initialization."""
        assert self.core.quote_categories is not None
        assert "motivational" in self.core.quote_categories
        assert self.core.quote_apis is not None
        assert len(self.core.quote_apis) > 0

    def test_quote_categories(self):
        """Test that all expected quote categories are available."""
        expected_categories = [
            "motivational",
            "mathematics",
            "science",
            "famous",
            "technology",
            "philosophy",
        ]

        for category in expected_categories:
            assert category in self.core.quote_categories

    @patch("requests.get")
    def test_get_quote_success(self, mock_get):
        """Test successful quote retrieval."""
        # Mock successful response from quotable.io
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "content": "Test quote content",
            "author": "Test Author",
        }
        mock_get.return_value = mock_response

        quote = self.core.get_quote("motivational")

        assert quote["text"] == "Test quote content"
        assert quote["author"] == "Test Author"

    @patch("requests.get")
    def test_get_quote_failure(self, mock_get):
        """Test quote retrieval when API fails."""
        # Mock failed response
        mock_get.side_effect = Exception("Network error")

        quote = self.core.get_quote("motivational")

        # Should return default quote on failure
        assert quote["text"] == "Stay motivated!"
        assert quote["author"] == "PaprWall"

    @patch("requests.get")
    def test_download_image_success(self, mock_get):
        """Test successful image download."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake image data"
        mock_get.return_value = mock_response

        with tempfile.TemporaryDirectory() as temp_dir:
            # Patch the IMAGES_DIR to use temp directory
            with patch("paprwall.core.IMAGES_DIR", Path(temp_dir)):
                result = self.core.download_image("https://example.com/test.jpg")

                assert result is not None
                assert Path(result).exists()
                assert Path(result).read_bytes() == b"fake image data"

    @patch("requests.get")
    def test_download_image_failure(self, mock_get):
        """Test image download failure."""
        mock_get.side_effect = Exception("Network error")

        result = self.core.download_image("https://example.com/test.jpg")
        assert result is None

    def test_wrap_text(self):
        """Test text wrapping functionality."""
        from PIL import ImageFont

        # Use default font for testing
        font = ImageFont.load_default()
        text = "This is a very long text that should be wrapped"
        max_width = 100  # Small width to force wrapping

        lines = self.core._wrap_text(text, font, max_width)

        assert isinstance(lines, list)
        assert len(lines) > 1  # Text should be wrapped into multiple lines
        assert all(isinstance(line, str) for line in lines)

    def test_set_wallpaper_unsupported_os(self):
        """Test wallpaper setting on unsupported OS."""
        with patch("platform.system", return_value="UnsupportedOS"):
            result = self.core.set_wallpaper("/fake/path.jpg")
            assert result is False

    @patch("subprocess.run")
    def test_set_wallpaper_linux_gnome(self, mock_run):
        """Test wallpaper setting on Linux GNOME."""
        mock_run.return_value.returncode = 0

        with patch("platform.system", return_value="Linux"):
            result = self.core._set_wallpaper_linux("/test/path.jpg")
            assert result is True

    @patch("ctypes.windll.user32.SystemParametersInfoW")
    def test_set_wallpaper_windows(self, mock_api):
        """Test wallpaper setting on Windows."""
        mock_api.return_value = True

        result = self.core._set_wallpaper_windows("/test/path.jpg")
        assert result is True

    def test_save_to_history(self):
        """Test saving wallpaper to history."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Patch DATA_DIR to use temp directory
            with patch("paprwall.core.DATA_DIR", Path(temp_dir)):
                quote_data = {"text": "Test quote", "author": "Test Author"}

                self.core.save_to_history("/test/image.jpg", quote_data)

                history_file = Path(temp_dir) / "history.json"
                assert history_file.exists()

                with open(history_file, "r") as f:
                    history = json.load(f)

                assert len(history) == 1
                assert history[0]["image_path"] == "/test/image.jpg"
                assert history[0]["quote"] == quote_data


class TestCLIFunctions:
    """Test CLI helper functions."""

    @patch("paprwall.core.WallpaperCore")
    def test_set_wallpaper_from_file_success(self, mock_core_class):
        """Test setting wallpaper from file successfully."""
        # Create mock core instance
        mock_core = Mock()
        mock_core.get_quote.return_value = {"text": "Test", "author": "Test"}
        mock_core.add_quote_to_image.return_value = "/test/output.jpg"
        mock_core.set_wallpaper.return_value = True
        mock_core.save_to_history.return_value = None
        mock_core_class.return_value = mock_core

        with patch("os.path.exists", return_value=True):
            result = set_wallpaper_from_file("/test/input.jpg")

        assert result == 0

    @patch("paprwall.core.WallpaperCore")
    def test_set_wallpaper_from_file_not_found(self, mock_core_class):
        """Test setting wallpaper from non-existent file."""
        with patch("os.path.exists", return_value=False):
            result = set_wallpaper_from_file("/nonexistent/file.jpg")

        assert result == 1

    @patch("paprwall.core.WallpaperCore")
    def test_fetch_and_set_wallpaper_success(self, mock_core_class):
        """Test fetching and setting wallpaper successfully."""
        # Create mock core instance
        mock_core = Mock()
        mock_core.download_image.return_value = "/test/downloaded.jpg"
        mock_core.get_quote.return_value = {"text": "Test", "author": "Test"}
        mock_core.add_quote_to_image.return_value = "/test/output.jpg"
        mock_core.set_wallpaper.return_value = True
        mock_core.save_to_history.return_value = None
        mock_core_class.return_value = mock_core

        result = fetch_and_set_wallpaper()

        assert result == 0

    @patch("paprwall.core.WallpaperCore")
    def test_fetch_and_set_wallpaper_download_fail(self, mock_core_class):
        """Test fetching wallpaper when download fails."""
        # Create mock core instance
        mock_core = Mock()
        mock_core.download_image.return_value = None  # Download fails
        mock_core_class.return_value = mock_core

        result = fetch_and_set_wallpaper()

        assert result == 1


@pytest.fixture
def sample_image():
    """Create a sample test image."""
    from PIL import Image

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        # Create a simple test image
        img = Image.new("RGB", (100, 100), color="blue")
        img.save(tmp.name, "JPEG")
        yield tmp.name

    # Cleanup
    Path(tmp.name).unlink(missing_ok=True)


def test_add_quote_to_image_integration(sample_image):
    """Integration test for adding quote to image."""
    core = WallpaperCore()
    quote_data = {"text": "Test Quote", "author": "Test Author"}

    result_path = core.add_quote_to_image(sample_image, quote_data)

    assert result_path is not None
    assert Path(result_path).exists()

    # Cleanup
    Path(result_path).unlink(missing_ok=True)


if __name__ == "__main__":
    pytest.main([__file__])
