"""
Scheduler for automatic wallpaper rotation.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging

from riturajprofile_wallpaper.core.rotator import WallpaperRotator
from riturajprofile_wallpaper.config.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class WallpaperScheduler:
    """Schedules automatic wallpaper rotation and fetching"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.rotator = WallpaperRotator(self.config)
        self.scheduler = BackgroundScheduler()
    
    def start(self):
        """Start the scheduler"""
        # Schedule daily fetch
        fetch_time = self.config.get_preference('auto_fetch_time', '09:00')
        hour, minute = map(int, fetch_time.split(':'))
        
        self.scheduler.add_job(
            self.fetch_wallpapers,
            CronTrigger(hour=hour, minute=minute),
            id='daily_fetch',
            name='Fetch daily wallpapers',
            replace_existing=True
        )
        
        # Schedule retry check every hour (for failed fetches)
        self.scheduler.add_job(
            self.check_and_retry_fetch,
            IntervalTrigger(hours=1),
            id='fetch_retry',
            name='Retry failed fetches',
            replace_existing=True
        )
        
        # Schedule rotation
        interval = self.config.get_preference('rotation_interval_minutes', 30)
        
        self.scheduler.add_job(
            self.rotate_wallpaper,
            IntervalTrigger(minutes=interval),
            id='rotation',
            name='Rotate wallpaper',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("Scheduler started with daily fetch and retry mechanism")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")
    
    def fetch_wallpapers(self):
        """Job to fetch new wallpapers"""
        logger.info("Fetching daily wallpapers...")
        try:
            success = self.rotator.fetch_and_rotate()
            if success:
                logger.info("Successfully fetched wallpapers")
            else:
                logger.warning("Failed to fetch wallpapers - will retry in 1 hour")
        except Exception as e:
            logger.error(f"Failed to fetch wallpapers: {e}")
    
    def check_and_retry_fetch(self):
        """Check if we need to retry a failed fetch"""
        try:
            if self.rotator.should_retry_fetch():
                logger.info("Retrying wallpaper fetch...")
                success = self.rotator.fetch_and_rotate(is_retry=True)
                if success:
                    logger.info("Retry successful!")
                else:
                    logger.warning("Retry failed - will try again in 1 hour")
        except Exception as e:
            logger.error(f"Error during retry check: {e}")
    
    def rotate_wallpaper(self):
        """Job to rotate to next wallpaper"""
        logger.info("Rotating wallpaper...")
        try:
            self.rotator.next()
            logger.info("Successfully rotated wallpaper")
        except Exception as e:
            logger.error(f"Failed to rotate wallpaper: {e}")
