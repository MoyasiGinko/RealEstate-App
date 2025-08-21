
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.button import Button

# Import Arabic font support
from configs.arabic_fonts import apply_arabic_font

Builder.load_file('assets/kv/about_gui.kv')

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add Arabic font support demo after the screen is built
        self.bind(on_enter=self.setup_arabic_fonts)

    def setup_arabic_fonts(self, *args):
        """Setup Arabic fonts for the about screen."""
        try:
            # Configure existing widgets with Arabic font support if they contain Arabic text
            for widget in self.walk(restrict=True):
                if hasattr(widget, 'text') and widget.text:
                    apply_arabic_font(widget, widget.text)
        except Exception as e:
            print(f"Error setting up Arabic fonts: {e}")

    def go_to_main_gui(self, instance=None):
        """Navigate back to the main GUI."""
        self.manager.current = 'main_gui'
