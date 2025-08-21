
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.button import Button

# Import Arabic font support and language management
from configs.arabic_fonts import apply_arabic_font
from configs.language_manager import get_language_manager, get_text

Builder.load_file('assets/kv/about_gui.kv')

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language_manager = get_language_manager()
        self.language_manager.register_observer(self)
        # Add Arabic font support demo after the screen is built
        self.bind(on_enter=self.setup_arabic_fonts)

    def show_language_switcher(self):
        """Show language switcher popup"""
        from configs.language_switcher import LanguageSwitcherPopup
        popup = LanguageSwitcherPopup()
        popup.open()

    def setup_arabic_fonts(self, *args):
        """Setup Arabic fonts for the about screen."""
        try:
            # Configure existing widgets with Arabic font support if they contain Arabic text
            for widget in self.walk(restrict=True):
                if hasattr(widget, 'text') and widget.text:
                    apply_arabic_font(widget, widget.text)
        except Exception as e:
            print(f"Error setting up Arabic fonts: {e}")

    def on_language_changed(self):
        """Called when language is changed"""
        try:
            self.setup_arabic_fonts()
        except Exception as e:
            print(f"Error handling language change in about screen: {e}")

    def go_to_main_gui(self, instance=None):
        """Navigate back to the main GUI."""
        self.manager.current = 'main_gui'
