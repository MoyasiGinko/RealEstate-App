"""
Minimal version of the main application.
"""
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.core.window import Window

# Import essential modules
from src.models.database_api import get_api
from src.screens.dashboard import DashboardScreen
from src.screens.owner_management import OwnerManagementScreen
from src.screens.property_management import PropertyManagementScreen
from src.screens.search_report import SearchReportScreen
from src.screens.settings import SettingsScreen

# Load the main kivy file
Builder.load_file('assets/kv/main.kv')

# Set window size for desktop application
Window.size = (1024, 768)

class MainApp(App):
    """Main application class for the Real Estate Property Management System."""

    def build(self):
        """Build the application."""
        # Create the screen manager
        sm = ScreenManager(transition=FadeTransition())

        # Add screens
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(OwnerManagementScreen(name='owner_management'))
        sm.add_widget(PropertyManagementScreen(name='property_management'))
        sm.add_widget(SearchReportScreen(name='search_report'))
        sm.add_widget(SettingsScreen(name='settings'))

        # Connect to the database
        api = get_api()
        api.connect()

        # Create initial data if needed
        api.insert_initial_data()

        # Set the company code for the session
        api.set_company_code('E901')

        return sm

if __name__ == '__main__':
    try:
        app = MainApp()
        app.run()
    except Exception as e:
        print(f"Error running application: {e}")
        import traceback
        traceback.print_exc()
