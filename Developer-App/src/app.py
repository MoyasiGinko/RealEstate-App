"""
Main Kivy Application Module
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from kivy.app import App
from kivy.config import Config
from kivy.logger import Logger

from .api import APIManager
from .ui.screens.main_screen import MainScreen

# Load environment variables
load_dotenv()


class DeveloperApp(App):
    """Main Kivy Application Class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = os.getenv('APP_TITLE', 'Developer Desktop App')
        self.icon = 'assets/icons/app_icon.png'

        # Initialize API manager
        self.api_manager = APIManager()

    def build_config(self, config):
        """Build app configuration"""
        config.setdefaults('graphics', {
            'width': '1200',
            'height': '800',
            'resizable': '1',
            'borderless': '0',
            'minimum_width': '800',
            'minimum_height': '600'
        })

        config.setdefaults('app', {
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'debug_mode': os.getenv('DEBUG_MODE', 'false')
        })

    def build_settings(self, settings):
        """Build app settings panel"""
        settings_json = """
        [
            {
                "type": "title",
                "title": "Application Settings"
            },
            {
                "type": "bool",
                "title": "Debug Mode",
                "desc": "Enable debug mode for development",
                "section": "app",
                "key": "debug_mode"
            },
            {
                "type": "options",
                "title": "Log Level",
                "desc": "Set application log level",
                "section": "app",
                "key": "log_level",
                "options": ["DEBUG", "INFO", "WARNING", "ERROR"]
            }
        ]        """
        settings.add_json_panel('Application', self.config, data=settings_json)

    def build(self):
        """Build the main application"""
        Logger.info(f"Starting {self.title}")

        # Initialize API manager and database
        init_result = self.api_manager.initialize()
        if not init_result.success:
            Logger.error(f"Failed to initialize API: {init_result.error}")        # Could show error dialog here
        else:
            Logger.info("API initialized successfully")

        # Create and return root widget
        return MainScreen()

    def on_start(self):
        """Called when the app starts"""
        Logger.info("Application started successfully")

    def on_stop(self):
        """Called when the app stops"""
        Logger.info("Application stopping...")
        self.api_manager.close()

    def on_pause(self):
        """Called when the app is paused"""
        return True

    def on_resume(self):
        """Called when the app resumes"""
        pass
