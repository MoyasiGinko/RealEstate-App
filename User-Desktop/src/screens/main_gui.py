from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from configs.language_manager import get_language_manager, get_text
from configs.language_switcher import show_language_switcher
from configs.arabic_fonts import apply_arabic_font
import os

# Load the KV file for the main_gui interface - use absolute path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir))
_kv_path = os.path.join(_project_root, 'assets', 'kv', 'main_gui.kv')
Builder.load_file(_kv_path)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.language_manager = get_language_manager()
        # Register for language change notifications
        self.language_manager.register_observer(self)
        # Bind to on_enter to setup localization
        self.bind(on_enter=self.setup_localization)

    def setup_localization(self, *args):
        """Setup localization and Arabic fonts"""
        try:
            self.update_texts()
            self.apply_fonts()
        except Exception as e:
            print(f"Error setting up localization: {e}")

    def update_texts(self):
        """Update all text widgets with current language"""
        try:
            # Define the mapping of IDs to translation keys
            text_mappings = {
                'company_name_label': 'company_name',
                'app_title_label': 'app_title',
                'tagline_label': 'tagline',
                'subtitle_label': 'subtitle',
                'choose_action_label': 'choose_action',
                'new_property_label': 'new_property',
                'update_property_label': 'update_property',
                'browse_property_label': 'browse_property',
                'upload_property_label': 'upload_property'
            }

            # Update each widget using its ID
            for widget_id, text_key in text_mappings.items():
                try:
                    widget = self.ids.get(widget_id)
                    if widget:
                        new_text = get_text(text_key)
                        widget.text = new_text
                        try:
                            apply_arabic_font(widget, new_text)
                        except Exception:
                            pass
                        # Apply Arabic font if needed
                        if self.language_manager.current_language == 'ar':
                            apply_arabic_font(widget, new_text)
                except Exception as e:
                    print(f"Error updating widget {widget_id}: {e}")

        except Exception as e:
            print(f"Error updating texts: {e}")

    def apply_fonts(self):
        """Apply Arabic fonts to all text widgets if Arabic is selected"""
        if self.language_manager.current_language == 'ar':
            try:
                for widget in self.walk():
                    if hasattr(widget, 'text') and widget.text:
                        apply_arabic_font(widget, widget.text)
            except Exception as e:
                print(f"Error applying fonts: {e}")

    def on_language_changed(self):
        """Called when language is changed"""
        self.setup_localization()

    def show_language_switcher(self):
        """Show the language switcher popup"""
        show_language_switcher()

    def on_enter(self):
        # Code to execute when entering the main screen
        pass

    def on_leave(self):
        # Code to execute when leaving the main screen
        pass

    # Additional methods for main screen functionalities can be added here