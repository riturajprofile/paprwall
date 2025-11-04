def install_system():
    """Install PaprWall to the system."""
    import platform
    import shutil
    from pathlib import Path

    # Define installation paths based on the operating system
    system = platform.system()
    if system == "Windows":
        install_path = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Programs" / "PaprWall"
        bin_path = install_path / "paprwall-gui.exe"
    else:  # Assume Linux for simplicity
        install_path = Path.home() / ".local" / "bin"
        bin_path = install_path / "paprwall-gui"

    # Create installation directory if it doesn't exist
    install_path.mkdir(parents=True, exist_ok=True)

    # Copy the executable to the installation path
    shutil.copy(Path(__file__).parent.parent / "paprwall" / "__main__.py", bin_path)

    # Create a desktop shortcut (Windows only)
    if system == "Windows":
        import winshell
        desktop = winshell.desktop()
        shortcut = winshell.shortcut()
        shortcut.path = str(bin_path)
        shortcut.description = "PaprWall - Modern Wallpaper Manager"
        shortcut.write(desktop / "PaprWall.lnk")

    return 0  # Success


def uninstall_system():
    """Uninstall PaprWall from the system."""
    import platform
    from pathlib import Path

    # Define paths based on the operating system
    system = platform.system()
    if system == "Windows":
        install_path = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Programs" / "PaprWall"
        bin_path = install_path / "paprwall-gui.exe"
        if bin_path.exists():
            bin_path.unlink()  # Remove the executable
        if install_path.exists():
            install_path.rmdir()  # Remove the directory if empty
    else:  # Assume Linux for simplicity
        bin_path = Path.home() / ".local" / "bin" / "paprwall-gui"
        if bin_path.exists():
            bin_path.unlink()  # Remove the executable

    return 0  # Success