"""
Scheduler for automatic wallpaper fetching from Picsum every N minutes.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

from paprwall.core.rotator import WallpaperRotator
from paprwall.config.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class WallpaperScheduler:
    """Schedules periodic wallpaper fetch-and-set jobs"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.rotator = WallpaperRotator(self.config)
        self.scheduler = BackgroundScheduler()
    
    def start(self):
        """Start the scheduler with interval-based fetching"""
        # Fetch interval (minutes). Default 90 minutes.
        interval = int(self.config.get_preference('rotation_interval_minutes', 90) or 90)

        self.scheduler.add_job(
            self.fetch_wallpapers,
            IntervalTrigger(minutes=interval),
            id='picsum_fetch_interval',
            name=f'Fetch from Picsum every {interval} minutes',
            replace_existing=True
        )

        self.scheduler.start()
        logger.info(f"Scheduler started: fetching wallpapers every {interval} minutes")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")
    
    def fetch_wallpapers(self):
        """Job to fetch new wallpapers and set immediately"""
        logger.info("Fetching new wallpaper(s) from Picsum...")
        try:
            success = self.rotator.fetch_and_rotate()
            if success:
                logger.info("Successfully fetched and set wallpaper")
            else:
                logger.warning("Failed to fetch/set wallpaper")
        except Exception as e:
            logger.error(f"Failed to fetch wallpapers: {e}")
