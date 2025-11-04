"""
CLI tests for PaprWall command-line interface.
"""

import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

from paprwall.cli import create_parser, main


class TestCLIParser:
    """Test the CLI argument parser."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = create_parser()

    def test_parser_creation(self):
        """Test that parser is created correctly."""
        assert self.parser is not None
        assert self.parser.prog == "paprwall"

    def test_version_argument(self):
        """Test --version argument."""
        with pytest.raises(SystemExit) as exc_info:
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.parser.parse_args(["--version"])

        # SystemExit with code 0 indicates successful version display
        assert exc_info.value.code == 0

    def test_gui_argument(self):
        """Test --gui argument."""
        args = self.parser.parse_args(["--gui"])
        assert args.gui is True

    def test_install_argument(self):
        """Test --install argument."""
        args = self.parser.parse_args(["--install"])
        assert args.install is True

    def test_uninstall_argument(self):
        """Test --uninstall argument."""
        args = self.parser.parse_args(["--uninstall"])
        assert args.uninstall is True

    def test_set_wallpaper_argument(self):
        """Test --set-wallpaper argument."""
        args = self.parser.parse_args(["--set-wallpaper", "/path/to/image.jpg"])
        assert args.set_wallpaper == "/path/to/image.jpg"

    def test_fetch_argument(self):
        """Test --fetch argument."""
        args = self.parser.parse_args(["--fetch"])
        assert args.fetch is True

    def test_category_argument(self):
        """Test --category argument."""
        args = self.parser.parse_args(["--category", "science"])
        assert args.category == "science"

    def test_category_default(self):
        """Test default category."""
        args = self.parser.parse_args([])
        assert args.category == "motivational"

    def test_category_invalid(self):
        """Test invalid category."""
        with pytest.raises(SystemExit):
            self.parser.parse_args(["--category", "invalid"])

    def test_no_quote_argument(self):
        """Test --no-quote argument."""
        args = self.parser.parse_args(["--no-quote"])
        assert args.no_quote is True

    def test_verbose_argument(self):
        """Test --verbose argument."""
        args = self.parser.parse_args(["--verbose"])
        assert args.verbose is True

        args = self.parser.parse_args(["-v"])
        assert args.verbose is True

    def test_config_dir_argument(self):
        """Test --config-dir argument."""
        args = self.parser.parse_args(["--config-dir", "/custom/config"])
        assert str(args.config_dir) == "/custom/config"

    def test_default_arguments(self):
        """Test default argument values."""
        args = self.parser.parse_args([])
        assert args.gui is False
        assert args.install is False
        assert args.uninstall is False
        assert args.set_wallpaper is None
        assert args.fetch is False
        assert args.category == "motivational"
        assert args.no_quote is False
        assert args.verbose is False
        assert args.config_dir is None


class TestCLIMain:
    """Test the main CLI function."""

    @patch("paprwall.cli.install_system")
    def test_main_install(self, mock_install):
        """Test main function with --install argument."""
        mock_install.return_value = 0

        result = main(["--install"])

        assert result == 0
        mock_install.assert_called_once()

    @patch("paprwall.cli.uninstall_system")
    def test_main_uninstall(self, mock_uninstall):
        """Test main function with --uninstall argument."""
        mock_uninstall.return_value = 0

        result = main(["--uninstall"])

        assert result == 0
        mock_uninstall.assert_called_once()

    @patch("paprwall.cli.set_wallpaper_from_file")
    def test_main_set_wallpaper(self, mock_set_wallpaper):
        """Test main function with --set-wallpaper argument."""
        mock_set_wallpaper.return_value = 0

        result = main(["--set-wallpaper", "/path/to/image.jpg"])

        assert result == 0
        mock_set_wallpaper.assert_called_once_with(
            "/path/to/image.jpg", add_quote=True, category="motivational"
        )

    @patch("paprwall.cli.set_wallpaper_from_file")
    def test_main_set_wallpaper_no_quote(self, mock_set_wallpaper):
        """Test main function with --set-wallpaper and --no-quote."""
        mock_set_wallpaper.return_value = 0

        result = main(["--set-wallpaper", "/path/to/image.jpg", "--no-quote"])

        assert result == 0
        mock_set_wallpaper.assert_called_once_with(
            "/path/to/image.jpg", add_quote=False, category="motivational"
        )

    @patch("paprwall.cli.fetch_and_set_wallpaper")
    def test_main_fetch(self, mock_fetch):
        """Test main function with --fetch argument."""
        mock_fetch.return_value = 0

        result = main(["--fetch"])

        assert result == 0
        mock_fetch.assert_called_once_with(category="motivational", add_quote=True)

    @patch("paprwall.cli.fetch_and_set_wallpaper")
    def test_main_fetch_with_category(self, mock_fetch):
        """Test main function with --fetch and --category."""
        mock_fetch.return_value = 0

        result = main(["--fetch", "--category", "science", "--no-quote"])

        assert result == 0
        mock_fetch.assert_called_once_with(category="science", add_quote=False)

    @patch("tkinter.Tk")
    @patch("paprwall.cli.WallpaperManagerGUI")
    def test_main_gui_default(self, mock_gui, mock_tk):
        """Test main function with default GUI behavior."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        mock_app = Mock()
        mock_gui.return_value = mock_app

        result = main([])

        assert result == 0
        mock_tk.assert_called_once()
        mock_gui.assert_called_once_with(mock_root)
        mock_root.mainloop.assert_called_once()

    @patch("tkinter.Tk")
    @patch("paprwall.cli.WallpaperManagerGUI")
    def test_main_gui_explicit(self, mock_gui, mock_tk):
        """Test main function with explicit --gui argument."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        mock_app = Mock()
        mock_gui.return_value = mock_app

        result = main(["--gui"])

        assert result == 0
        mock_tk.assert_called_once()
        mock_gui.assert_called_once_with(mock_root)
        mock_root.mainloop.assert_called_once()

    def test_main_keyboard_interrupt(self):
        """Test main function with keyboard interrupt."""
        with patch("paprwall.cli.install_system", side_effect=KeyboardInterrupt):
            result = main(["--install"])
            assert result == 1

    def test_main_exception_verbose(self):
        """Test main function with exception in verbose mode."""
        with patch("paprwall.cli.install_system", side_effect=Exception("Test error")):
            result = main(["--install", "--verbose"])
            assert result == 1

    def test_main_exception_quiet(self):
        """Test main function with exception in quiet mode."""
        with patch("paprwall.cli.install_system", side_effect=Exception("Test error")):
            result = main(["--install"])
            assert result == 1

    @patch("sys.stderr", new_callable=StringIO)
    def test_main_error_output(self, mock_stderr):
        """Test that errors are written to stderr."""
        with patch("paprwall.cli.install_system", side_effect=Exception("Test error")):
            result = main(["--install"])

            assert result == 1
            error_output = mock_stderr.getvalue()
            assert "Error: Test error" in error_output

    @patch("sys.stdout", new_callable=StringIO)
    def test_main_keyboard_interrupt_message(self, mock_stdout):
        """Test keyboard interrupt message."""
        with patch("paprwall.cli.install_system", side_effect=KeyboardInterrupt):
            result = main(["--install"])

            assert result == 1
            output = mock_stdout.getvalue()
            assert "Operation cancelled by user." in output

    @patch("tkinter.Tk")
    @patch("paprwall.cli.WallpaperManagerGUI")
    def test_main_gui_with_cli_args(self, mock_gui, mock_tk):
        """Test main function passes CLI args to GUI if supported."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        mock_app = Mock()
        mock_app.set_cli_args = Mock()  # App supports CLI args
        mock_gui.return_value = mock_app

        result = main(["--gui", "--verbose"])

        assert result == 0
        # Should call set_cli_args if method exists
        mock_app.set_cli_args.assert_called_once()

    @patch("tkinter.Tk")
    @patch("paprwall.cli.WallpaperManagerGUI")
    def test_main_gui_without_cli_args_support(self, mock_gui, mock_tk):
        """Test main function when GUI doesn't support CLI args."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        mock_app = Mock()
        # App doesn't have set_cli_args method
        if hasattr(mock_app, "set_cli_args"):
            delattr(mock_app, "set_cli_args")
        mock_gui.return_value = mock_app

        result = main(["--gui"])

        assert result == 0
        # Should not crash when method doesn't exist

    def test_main_no_args(self):
        """Test main function with no arguments uses sys.argv."""
        with patch("sys.argv", ["paprwall"]):
            with patch("tkinter.Tk") as mock_tk:
                with patch("paprwall.cli.WallpaperManagerGUI") as mock_gui:
                    mock_root = Mock()
                    mock_tk.return_value = mock_root
                    mock_app = Mock()
                    mock_gui.return_value = mock_app

                    # Call main without arguments (uses sys.argv)
                    result = main()

                    assert result == 0


class TestCLIIntegration:
    """Integration tests for CLI functionality."""

    def test_help_message(self):
        """Test that help message is displayed correctly."""
        parser = create_parser()

        with pytest.raises(SystemExit) as exc_info:
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                parser.parse_args(["--help"])

        # Help should exit with code 0
        assert exc_info.value.code == 0

        # Check that help contains expected information
        help_output = mock_stdout.getvalue()
        assert "Modern Desktop Wallpaper Manager" in help_output
        assert "--install" in help_output
        assert "--uninstall" in help_output
        assert "--set-wallpaper" in help_output
        assert "--fetch" in help_output

    def test_mutually_exclusive_operations(self):
        """Test that certain operations work correctly when combined."""
        # These should work fine together
        args = create_parser().parse_args(
            ["--fetch", "--category", "science", "--no-quote"]
        )
        assert args.fetch is True
        assert args.category == "science"
        assert args.no_quote is True

    def test_all_quote_categories_valid(self):
        """Test that all quote categories are valid parser choices."""
        parser = create_parser()
        categories = [
            "motivational",
            "mathematics",
            "science",
            "famous",
            "technology",
            "philosophy",
        ]

        for category in categories:
            args = parser.parse_args(["--category", category])
            assert args.category == category


if __name__ == "__main__":
    pytest.main([__file__])
