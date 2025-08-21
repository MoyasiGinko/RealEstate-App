
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
        # Update texts when screen is built
        self.bind(on_enter=self.on_screen_enter)

    def on_screen_enter(self, *args):
        """Called when screen is entered"""
        self.update_texts()
        self.setup_arabic_fonts()

    def update_texts(self):
        """Update all text elements with current language"""
        try:
            # Update title
            if hasattr(self.ids, 'about_title'):
                self.ids.about_title.text = get_text('about_us', 'About Us')

            # Update company name
            if hasattr(self.ids, 'company_name_label'):
                self.ids.company_name_label.text = get_text('company_name_full', 'Al-Kawaz Software and Information Technology')

            # Update version
            if hasattr(self.ids, 'version_label'):
                self.ids.version_label.text = get_text('version', 'Version: 1.0.0')

            # Update author
            if hasattr(self.ids, 'author_label'):
                self.ids.author_label.text = get_text('author', 'Author: Luay Alkawaz')

            # Update description
            if hasattr(self.ids, 'description_label'):
                self.ids.description_label.text = get_text('description', 'This application helps users manage real estate properties efficiently and intuitively.\nProfessional • Reliable • Innovative\nThank you for using our system!')

            # Update back button
            if hasattr(self.ids, 'back_btn'):
                self.ids.back_btn.text = get_text('back_to_main', '← Back to Main')

            # Update language button
            if hasattr(self.ids, 'language_btn'):
                self.ids.language_btn.text = get_text('language', 'Language') + '\n' + 'اللغة'

            # Apply fonts after text updates
            self.setup_arabic_fonts()

        except Exception as e:
            print(f"Error updating texts in about screen: {e}")

    def show_language_switcher(self):
        """Show language switcher popup"""
        from configs.language_switcher import show_language_switcher
        show_language_switcher()

    def setup_arabic_fonts(self, *args):
        """Setup Arabic fonts for the about screen."""
        try:
            # Configure widgets with Arabic font support if they contain Arabic text
            for widget in self.walk(restrict=True):
                if hasattr(widget, 'text') and widget.text:
                    apply_arabic_font(widget, widget.text)
        except Exception as e:
            print(f"Error setting up Arabic fonts: {e}")

    def on_language_changed(self):
        """Called when language is changed"""
        try:
            self.update_texts()
        except Exception as e:
            print(f"Error handling language change in about screen: {e}")

    def go_to_main_gui(self, instance=None):
        """Navigate back to the main GUI."""
        self.manager.current = 'main_gui'
