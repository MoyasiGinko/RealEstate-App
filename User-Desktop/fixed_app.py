"""
Test script for the full application.
"""
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.core.window import Window

# Import screens
from src.models.database_api import get_api
from src.screens.dashboard import DashboardScreen
from src.screens.owner_management import OwnerManagementScreen
from src.screens.property_management import PropertyManagementScreen
from src.screens.search_report import SearchReportScreen
from src.screens.settings import SettingsScreen

# Set window size for desktop application
Window.size = (1024, 768)

class FixedApp(App):
    """Fixed version of the main application."""

    def build(self):
        """Build the application."""
        try:
            # Load the main kivy file using absolute path
            _current_dir = os.path.dirname(os.path.abspath(__file__))
            _main_kv_path = os.path.join(_current_dir, 'assets', 'kv', 'main.kv')
            Builder.load_file(_main_kv_path)

            # Create the screen manager
            sm = ScreenManager(transition=FadeTransition())

            # Connect to the database
            api = get_api()
            api.connect()

            # Create initial data if needed
            api.insert_initial_data()

            # Set the company code for the session
            api.set_company_code('E901')

            # Add screens
            sm.add_widget(DashboardScreen(name='dashboard'))
            sm.add_widget(OwnerManagementScreen(name='owner_management'))
            sm.add_widget(PropertyManagementScreen(name='property_management'))
            sm.add_widget(SearchReportScreen(name='search_report'))
            sm.add_widget(SettingsScreen(name='settings'))

            print("Application built successfully!")
            return sm

        except Exception as e:
            print(f"Error building application: {e}")
            import traceback
            traceback.print_exc()
            return None

if __name__ == '__main__':
    try:
        app = FixedApp()
        app.run()
    except Exception as e:
        print(f"Error running application: {e}")
        import traceback
        traceback.print_exc()
