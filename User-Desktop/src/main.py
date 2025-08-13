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
from screens.browse_gui import SearchReportScreen
from screens.about_gui import AboutScreen
from screens.main_gui import MainScreen
from screens.upload_gui import UploadScreen
from screens.insert_gui import InsertScreen
from screens.update_gui import UpdateGUIScreen



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

        self.sm.add_widget(MainScreen(name='main_gui'))
        self.sm.add_widget(InsertScreen(name='insert_gui'))
        self.sm.add_widget(UpdateGUIScreen(name='update_gui'))
        self.sm.add_widget(SearchReportScreen(name='browse_gui'))
        self.sm.add_widget(UploadScreen(name='upload_gui'))
        self.sm.add_widget(AboutScreen(name='about_gui'))

        # Set the default screen
        self.sm.current = 'main_gui'

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