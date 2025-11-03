"""
Background daemon service for Paprwall.
Runs the scheduler in the background to automatically fetch and rotate wallpapers.
"""
import os
import sys
import signal
import logging
from pathlib import Path
from riturajprofile_wallpaper.service.scheduler import WallpaperScheduler
from riturajprofile_wallpaper.utils.logger import setup_logger
from riturajprofile_wallpaper import DATA_DIR

logger = setup_logger()

# PID file location
PID_FILE = DATA_DIR / 'paprwall.pid'


class DaemonService:
    """Background service daemon"""
    
    def __init__(self):
        self.scheduler = None
        self.running = False
    
    def start(self):
        """Start the daemon service"""
        try:
            # Check if already running
            if PID_FILE.exists():
                try:
                    with open(PID_FILE, 'r') as f:
                        old_pid = int(f.read().strip())
                    
                    # Check if process is actually running
                    try:
                        os.kill(old_pid, 0)  # Signal 0 just checks if process exists
                        logger.error(f"Service already running with PID {old_pid}")
                        return False
                    except OSError:
                        # Process doesn't exist, remove stale PID file
                        pass
                except:
                    pass
            
            # Write PID file
            with open(PID_FILE, 'w') as f:
                f.write(str(os.getpid()))
            
            logger.info("Starting Paprwall service...")
            
            # Setup signal handlers
            signal.signal(signal.SIGTERM, self._handle_signal)
            signal.signal(signal.SIGINT, self._handle_signal)
            
            # Start scheduler
            self.scheduler = WallpaperScheduler()
            self.scheduler.start()
            
            logger.info("✓ Paprwall service started successfully")
            logger.info("Wallpapers will be fetched daily and rotated automatically")
            
            self.running = True
            
            # Keep running
            while self.running:
                signal.pause()
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            self.stop()
        except Exception as e:
            logger.error(f"Error in daemon service: {e}")
            self.stop()
            return False
    
    def stop(self):
        """Stop the daemon service"""
        logger.info("Stopping Paprwall service...")
        
        self.running = False
        
        if self.scheduler:
            self.scheduler.stop()
        
        # Remove PID file
        if PID_FILE.exists():
            PID_FILE.unlink()
        
        logger.info("✓ Paprwall service stopped")
    
    def _handle_signal(self, signum, frame):
        """Handle termination signals"""
        logger.info(f"Received signal {signum}")
        self.stop()
        sys.exit(0)


def main():
    """Main entry point for daemon"""
    import os
    
    daemon = DaemonService()
    
    try:
        daemon.start()
    except Exception as e:
        logger.error(f"Failed to start daemon: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
