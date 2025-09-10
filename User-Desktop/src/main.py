from kivy.app import App
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.models.database_api import get_api

# Initialize Arabic font support
from configs.arabic_fonts import init_arabic_fonts, set_global_arabic_font, restore_default_font, apply_font_to_all_widgets
from configs.language_manager import get_language_manager

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
    rtl = BooleanProperty(False)

    def build(self):
        """Build the application and set up the screen manager."""
        # Initialize Arabic font support
        self.arabic_fonts = init_arabic_fonts()

        if self.arabic_fonts.fonts_registered:
            print("✅ Arabic fonts initialized successfully!")
        else:
            print("⚠️  Arabic fonts not available, using system defaults")

        # Initialize language manager and set up global font observer
        self.language_manager = get_language_manager()
        self.language_manager.register_observer(self)

        # Set global default font based on current language
        self._update_global_font()

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

    def on_language_changed(self):
        """Called when language is changed - update global font"""
        self._update_global_font()

    def _update_global_font(self):
        """Set global default font based on current language"""
        if not hasattr(self, 'arabic_fonts') or not self.arabic_fonts.fonts_registered:
            return

        current_lang = self.language_manager.get_current_language()

        if current_lang == 'ar':
            # Enable RTL mode for KV bindings
            try:
                self.rtl = True
            except Exception:
                pass
            # Set Arabic font as the global default
            set_global_arabic_font()
            # Also apply Arabic font to all existing widgets
            if hasattr(self, 'sm') and self.sm:
                apply_font_to_all_widgets(self.sm)
        else:
            # Restore system default font
            try:
                self.rtl = False
            except Exception:
                pass
            restore_default_font()

if __name__ == '__main__':
    MainApp().run()