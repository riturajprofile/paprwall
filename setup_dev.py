#!/usr/bin/env python3
"""
PaprWall Development Environment Setup Script

This script automates the setup of a development environment for PaprWall,
including dependency installation, virtual environment creation, and basic
validation checks.

Usage:
    python setup_dev.py [options]

Options:
    --skip-venv     Skip virtual environment creation
    --skip-deps     Skip dependency installation
    --skip-tests    Skip running tests
    --clean         Clean existing build artifacts
    --help          Show this help message
"""

import argparse
import os
import sys
import subprocess
import platform
import shutil
import venv
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    END = "\033[0m"


class DevSetup:
    """Development environment setup manager."""

    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.venv_path = self.project_root / ".venv"
        self.src_path = self.project_root / "src"
        self.tests_path = self.project_root / "tests"
        self.system = platform.system().lower()

        # Check if we're already in a virtual environment
        self.in_venv = hasattr(sys, "real_prefix") or (
            hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
        )

    def print_status(self, message: str, status: str = "INFO"):
        """Print colored status message."""
        colors = {
            "INFO": Colors.BLUE,
            "SUCCESS": Colors.GREEN,
            "WARNING": Colors.YELLOW,
            "ERROR": Colors.RED,
            "STEP": Colors.CYAN,
        }
        color = colors.get(status, Colors.WHITE)
        print(f"{color}[{status}]{Colors.END} {message}")

    def run_command(self, cmd: list, check: bool = True, capture_output: bool = False):
        """Run a system command with error handling."""
        try:
            self.print_status(f"Running: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                check=check,
                capture_output=capture_output,
                text=True,
                cwd=self.project_root,
            )
            if capture_output:
                return result.stdout.strip()
            return True
        except subprocess.CalledProcessError as e:
            self.print_status(f"Command failed: {e}", "ERROR")
            if capture_output:
                return None
            return False
        except FileNotFoundError:
            self.print_status(f"Command not found: {cmd[0]}", "ERROR")
            return False

    def check_python_version(self):
        """Check if Python version meets requirements."""
        self.print_status("Checking Python version...", "STEP")

        version = sys.version_info
        if version < (3, 8):
            self.print_status(
                f"Python 3.8+ required, found {version.major}.{version.minor}", "ERROR"
            )
            return False

        self.print_status(
            f"Python {version.major}.{version.minor}.{version.micro} ✓", "SUCCESS"
        )
        return True

    def check_system_dependencies(self):
        """Check and install system dependencies."""
        self.print_status("Checking system dependencies...", "STEP")

        if self.system == "linux":
            # Check for tkinter
            try:
                import tkinter

                self.print_status("Tkinter available ✓", "SUCCESS")
            except ImportError:
                self.print_status(
                    "Tkinter not found. Install with: sudo apt install python3-tk",
                    "WARNING",
                )

        elif self.system == "windows":
            self.print_status("Windows detected - Tkinter should be available", "INFO")

        elif self.system == "darwin":
            self.print_status("macOS detected - Tkinter should be available", "INFO")

        return True

    def create_virtual_environment(self):
        """Create virtual environment if it doesn't exist."""
        if self.in_venv:
            self.print_status("Already in virtual environment", "INFO")
            return True

        self.print_status("Creating virtual environment...", "STEP")

        if self.venv_path.exists():
            self.print_status("Virtual environment already exists", "INFO")
            return True

        try:
            venv.create(self.venv_path, with_pip=True, upgrade_deps=True)
            self.print_status("Virtual environment created ✓", "SUCCESS")

            # Show activation instructions
            if self.system == "windows":
                activation_cmd = ".venv\\Scripts\\activate"
            else:
                activation_cmd = "source .venv/bin/activate"

            self.print_status(f"Activate with: {activation_cmd}", "INFO")
            return True

        except Exception as e:
            self.print_status(f"Failed to create virtual environment: {e}", "ERROR")
            return False

    def get_python_executable(self):
        """Get the Python executable to use."""
        if self.in_venv:
            return sys.executable

        # Use venv python if available
        if self.system == "windows":
            venv_python = self.venv_path / "Scripts" / "python.exe"
        else:
            venv_python = self.venv_path / "bin" / "python"

        if venv_python.exists():
            return str(venv_python)

        return sys.executable

    def install_dependencies(self):
        """Install Python dependencies."""
        self.print_status("Installing dependencies...", "STEP")

        python_exe = self.get_python_executable()

        # Upgrade pip
        if not self.run_command(
            [python_exe, "-m", "pip", "install", "--upgrade", "pip"]
        ):
            return False

        # Install build tools
        if not self.run_command(
            [
                python_exe,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "setuptools",
                "wheel",
                "build",
            ]
        ):
            return False

        # Install runtime dependencies
        requirements_file = self.project_root / "requirements.txt"
        if requirements_file.exists():
            if not self.run_command(
                [python_exe, "-m", "pip", "install", "-r", str(requirements_file)]
            ):
                return False

        # Install development dependencies
        if not self.run_command([python_exe, "-m", "pip", "install", "-e", ".[dev]"]):
            return False

        self.print_status("Dependencies installed ✓", "SUCCESS")
        return True

    def run_tests(self):
        """Run the test suite."""
        self.print_status("Running tests...", "STEP")

        python_exe = self.get_python_executable()

        if not self.tests_path.exists():
            self.print_status("No tests directory found", "WARNING")
            return True

        # Run pytest
        success = self.run_command(
            [python_exe, "-m", "pytest", str(self.tests_path), "-v", "--tb=short"],
            check=False,
        )

        if success:
            self.print_status("All tests passed ✓", "SUCCESS")
        else:
            self.print_status("Some tests failed", "WARNING")

        return True  # Don't fail setup if tests fail

    def validate_installation(self):
        """Validate that everything is working."""
        self.print_status("Validating installation...", "STEP")

        python_exe = self.get_python_executable()

        # Test CLI
        version_output = self.run_command(
            [python_exe, "-m", "paprwall.cli", "--version"], capture_output=True
        )

        if version_output:
            self.print_status(f"CLI working: {version_output}", "SUCCESS")
        else:
            self.print_status("CLI validation failed", "ERROR")
            return False

        # Test imports
        test_imports = [
            "import paprwall",
            "import paprwall.core",
            "import paprwall.cli",
            "import paprwall.gui",
        ]

        for import_stmt in test_imports:
            result = self.run_command(
                [python_exe, "-c", import_stmt], capture_output=True
            )
            if result is not None:
                self.print_status(f"Import OK: {import_stmt.split()[-1]}", "SUCCESS")
            else:
                self.print_status(f"Import failed: {import_stmt}", "ERROR")
                return False

        return True

    def clean_build_artifacts(self):
        """Clean build artifacts and caches."""
        self.print_status("Cleaning build artifacts...", "STEP")

        # Directories to clean
        clean_dirs = [
            "build",
            "dist",
            "*.egg-info",
            "__pycache__",
            ".pytest_cache",
            ".coverage",
            ".mypy_cache",
        ]

        for pattern in clean_dirs:
            if "*" in pattern:
                # Use glob for patterns
                import glob

                for path in glob.glob(pattern):
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                        self.print_status(f"Removed: {path}")
            else:
                path = self.project_root / pattern
                if path.exists():
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                    self.print_status(f"Removed: {path}")

        # Clean Python cache files
        for root, dirs, files in os.walk(self.project_root):
            # Remove __pycache__ directories
            if "__pycache__" in dirs:
                cache_path = Path(root) / "__pycache__"
                shutil.rmtree(cache_path)
                self.print_status(f"Removed: {cache_path}")

            # Remove .pyc files
            for file in files:
                if file.endswith((".pyc", ".pyo")):
                    file_path = Path(root) / file
                    file_path.unlink()

        self.print_status("Build artifacts cleaned ✓", "SUCCESS")

    def show_next_steps(self):
        """Show what to do next."""
        self.print_status("Setup complete! Next steps:", "SUCCESS")

        print(f"\n{Colors.BOLD}Development Commands:{Colors.END}")

        if not self.in_venv and self.venv_path.exists():
            if self.system == "windows":
                print(
                    f"  {Colors.CYAN}Activate venv:{Colors.END} .venv\\Scripts\\activate"
                )
            else:
                print(
                    f"  {Colors.CYAN}Activate venv:{Colors.END} source .venv/bin/activate"
                )

        print(f"  {Colors.CYAN}Run GUI:{Colors.END} paprwall-gui")
        print(f"  {Colors.CYAN}Run CLI:{Colors.END} python -m paprwall.cli --help")
        print(f"  {Colors.CYAN}Run tests:{Colors.END} python -m pytest tests/")
        print(f"  {Colors.CYAN}Format code:{Colors.END} black src/ tests/")
        print(f"  {Colors.CYAN}Lint code:{Colors.END} flake8 src/ tests/")
        print(f"  {Colors.CYAN}Type check:{Colors.END} mypy src/paprwall")

        print(f"\n{Colors.BOLD}Build Commands:{Colors.END}")
        print(f"  {Colors.CYAN}Build package:{Colors.END} python -m build")
        if self.system == "linux":
            print(
                f"  {Colors.CYAN}Build executable:{Colors.END} ./scripts/build_linux.sh"
            )
        elif self.system == "windows":
            print(
                f"  {Colors.CYAN}Build executable:{Colors.END} scripts\\build_windows.bat"
            )

        print(f"\n{Colors.BOLD}Project Info:{Colors.END}")
        print(f"  {Colors.CYAN}Project root:{Colors.END} {self.project_root}")
        print(f"  {Colors.CYAN}Source code:{Colors.END} {self.src_path}")
        print(f"  {Colors.CYAN}Tests:{Colors.END} {self.tests_path}")
        if self.venv_path.exists():
            print(f"  {Colors.CYAN}Virtual env:{Colors.END} {self.venv_path}")

    def run_setup(self, args):
        """Run the complete setup process."""
        self.print_status("Starting PaprWall development setup...", "STEP")
        print(f"{Colors.BOLD}Project:{Colors.END} {self.project_root}")
        print(
            f"{Colors.BOLD}System:{Colors.END} {platform.system()} {platform.machine()}"
        )
        print()

        # Clean if requested
        if args.clean:
            self.clean_build_artifacts()

        # Check Python version
        if not self.check_python_version():
            return False

        # Check system dependencies
        if not self.check_system_dependencies():
            return False

        # Create virtual environment
        if not args.skip_venv and not self.create_virtual_environment():
            return False

        # Install dependencies
        if not args.skip_deps and not self.install_dependencies():
            return False

        # Validate installation
        if not self.validate_installation():
            return False

        # Run tests
        if not args.skip_tests:
            self.run_tests()

        # Show next steps
        self.show_next_steps()

        self.print_status("Development environment setup complete! 🎉", "SUCCESS")
        return True


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="PaprWall Development Environment Setup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_dev.py                    # Full setup
  python setup_dev.py --skip-venv        # Skip virtual environment creation
  python setup_dev.py --clean            # Clean build artifacts first
  python setup_dev.py --skip-tests       # Skip running tests
        """,
    )

    parser.add_argument(
        "--skip-venv", action="store_true", help="Skip virtual environment creation"
    )

    parser.add_argument(
        "--skip-deps", action="store_true", help="Skip dependency installation"
    )

    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")

    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean existing build artifacts before setup",
    )

    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    setup = DevSetup()

    try:
        success = setup.run_setup(args)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        setup.print_status("Setup interrupted by user", "WARNING")
        sys.exit(1)
    except Exception as e:
        setup.print_status(f"Unexpected error: {e}", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    main()
