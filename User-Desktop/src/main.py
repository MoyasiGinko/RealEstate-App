from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.core.window import Window
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.models.database_api import get_api

# Import screens
from src.screens.dashboard import DashboardScreen
from src.screens.owner_management import OwnerManagementScreen
from src.screens.property_management import PropertyManagementScreen
from src.screens.search_report import SearchReportScreen
from src.screens.settings import SettingsScreen

# Load the main kivy file using absolute path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_dir)
_main_kv_path = os.path.join(_project_root, 'assets', 'kv', 'main.kv')
Builder.load_file(_main_kv_path)

# Set window size for desktop application
Window.size = (1024, 768)

class MainApp(App):
    """Main application class for the Real Estate Property Management System."""

    def build(self):
        """Build the application and set up the screen manager."""
        # Connect to the database
        self.api = get_api()
        if not self.api.connect():
            print("Database connection failed!")
            return

        # Set company code from settings (for now, hardcoded)
        self.api.set_company_code('E901')

        # Set up the screen manager with transition
        self.sm = ScreenManager(transition=FadeTransition())

        # Add all screens to the manager
        self.sm.add_widget(DashboardScreen(name='dashboard'))
        self.sm.add_widget(OwnerManagementScreen(name='owner_management'))
        self.sm.add_widget(PropertyManagementScreen(name='property_management'))
        self.sm.add_widget(SearchReportScreen(name='search_report'))
        self.sm.add_widget(SettingsScreen(name='settings'))

        # Set the default screen
        self.sm.current = 'dashboard'

        return self.sm

    def change_screen(self, screen_name):
        """Change to the specified screen."""
        self.sm.current = screen_name

    def on_stop(self):
        """Clean up resources when the application stops."""
        # Close the database connection
        self.api.close()
        print("Application stopped, database connection closed.")

if __name__ == '__main__':
    MainApp().run()