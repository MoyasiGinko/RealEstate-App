"""
Test script for property management screen.
"""
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

# Import needed modules
from src.models.database_api import get_api
from src.screens.property_management import PropertyManagementScreen

# Set window size for desktop application
Window.size = (1024, 768)

class TestApp(App):
    """Test application for property management screen."""

    def build(self):
        """Build the application."""
        # Create main layout
        layout = BoxLayout(orientation='vertical')

        # Connect to the database
        api = get_api()
        api.connect()

        # Create initial data if needed
        api.insert_initial_data()

        # Set the company code for the session
        api.set_company_code('E901')

        # Add property management screen
        property_screen = PropertyManagementScreen(name='property_management')
        layout.add_widget(property_screen)

        # Give the screen a chance to initialize
        property_screen.on_enter()

        return layout

if __name__ == '__main__':
    try:
        app = TestApp()
        app.run()
    except Exception as e:
        print(f"Error running application: {e}")
        import traceback
        traceback.print_exc()
