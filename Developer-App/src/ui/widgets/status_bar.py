"""
Status Bar Widget with API connection monitoring
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.logger import Logger
import time
from datetime import datetime


class StatusBar(BoxLayout):
    """Status bar showing application status and information"""

    def __init__(self, api_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 30
        self.padding = [10, 2]
        self.spacing = 20
        self.api_manager = api_manager
        self.build_status_bar()

        # Schedule regular updates
        Clock.schedule_interval(self.update_status, 1.0)

    def build_status_bar(self):
        """Build status bar components"""
        # Status message area
        self.status_label = Label(
            text='Ready',
            size_hint_x=0.4,
            text_size=(None, None),
            halign='left',
            valign='middle',
            font_size=12
        )
        self.add_widget(self.status_label)

        # Spacer
        spacer = Label(size_hint_x=0.2)
        self.add_widget(spacer)

        # Connection status
        self.connection_label = Label(
            text='DB: Connected',
            size_hint_x=0.2,
            text_size=(None, None),
            halign='center',
            valign='middle',
            font_size=12
        )
        self.add_widget(self.connection_label)

        # Clock
        self.clock_label = Label(
            text='',
            size_hint_x=0.2,
            text_size=(None, None),
            halign='right',
            valign='middle',
            font_size=12        )
        self.add_widget(self.clock_label)

    def update_status(self, dt):
        """Update status bar information"""
        # Update clock
        current_time = datetime.now().strftime('%H:%M:%S')
        self.clock_label.text = current_time

        # Update API connection status
        self.update_api_connection_status()

    def update_api_connection_status(self):
        """Update API connection status"""
        if not self.api_manager:
            self.set_connection_status(False, "No API Manager")
            return

        if not self.api_manager.is_initialized():
            self.set_connection_status(False, "API Not Initialized")
            return

        try:
            # Test connection every 30 seconds to avoid overhead
            if hasattr(self, '_last_connection_check'):
                if time.time() - self._last_connection_check < 30:
                    return

            self._last_connection_check = time.time()

            # Quick connection test
            test_result = self.api_manager.test_connection()
            if test_result.success:
                self.set_connection_status(True, "Connected")
            else:
                self.set_connection_status(False, "Connection Failed")

        except Exception as e:
            self.set_connection_status(False, f"Error: {str(e)[:20]}")

    def set_status(self, message):
        """Set status message"""
        self.status_label.text = message
        Logger.info(f"Status updated: {message}")

    def set_connection_status(self, connected, details=""):
        """Update connection status"""
        if connected:
            self.connection_label.text = f'API: {details}' if details else 'API: Connected'
            self.connection_label.color = (0, 1, 0, 1)  # Green
        else:
            self.connection_label.text = f'API: {details}' if details else 'API: Disconnected'
            self.connection_label.color = (1, 0, 0, 1)  # Red

    def show_temporary_message(self, message, duration=3.0):
        """Show a temporary message that reverts after duration"""
        original_message = self.status_label.text
        self.set_status(message)

        def revert_message(dt):
            self.set_status(original_message)

        Clock.schedule_once(revert_message, duration)
