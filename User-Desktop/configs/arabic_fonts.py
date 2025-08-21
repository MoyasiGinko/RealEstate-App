#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production Arabic Font Configuration with Global Font Support
Clean and simple Arabic font support for the Real Estate Management System
"""

from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import os
import re

class ArabicFonts:
    """Production-ready Arabic font support with global font switching"""

    FONT_NAME = 'ArabicFont'

    def __init__(self):
        self.fonts_registered = False
        self.original_default_font = None
        self._setup_fonts()

    def _setup_fonts(self):
        """Register Arabic fonts"""
        try:
            # Get the app root directory
            app_root = self._get_app_root()

            # Font paths
            regular_font = os.path.join(app_root, 'assets', 'fonts', 'Amiri-Regular.ttf')
            bold_font = os.path.join(app_root, 'assets', 'fonts', 'Amiri-Bold.ttf')

            # Check if fonts exist
            if not os.path.exists(regular_font):
                print(f"⚠️  Arabic font not found: {regular_font}")
                return

            # Store original default font before registering custom one
            try:
                self.original_default_font = LabelBase._fonts.get('default', {}).get('regular')
            except:
                pass

            # Store the Arabic font path for later use
            self.arabic_font_path = regular_font

            # Register fonts
            params = {
                'name': self.FONT_NAME,
                'fn_regular': regular_font,
            }

            if os.path.exists(bold_font):
                params['fn_bold'] = bold_font

            LabelBase.register(**params)
            self.fonts_registered = True
            print("✅ Arabic fonts registered successfully")

        except Exception as e:
            print(f"❌ Error registering Arabic fonts: {e}")

    def set_global_arabic_font(self):
        """Set Arabic font as the global default for all new widgets"""
        if not self.fonts_registered:
            print("⚠️  Arabic fonts not available, cannot set as global default")
            return False

        try:
            # Use the stored Arabic font path
            if not hasattr(self, 'arabic_font_path') or not self.arabic_font_path:
                print("⚠️  Arabic font path not available")
                return False

            # Set as default font - all new widgets will use this
            LabelBase.register(name='default', fn_regular=self.arabic_font_path)

            # Also set font for specific widget types to ensure coverage
            from kivy.uix.label import Label
            from kivy.uix.button import Button
            from kivy.uix.textinput import TextInput
            from kivy.uix.spinner import Spinner

            # Update default font properties for different widget classes
            Label._font_name = self.FONT_NAME
            Button._font_name = self.FONT_NAME
            TextInput._font_name = self.FONT_NAME
            Spinner._font_name = self.FONT_NAME

            print("🌐 Arabic font set as global default for all widget types")
            return True
        except Exception as e:
            print(f"❌ Error setting global Arabic font: {e}")
            return False

    def restore_default_font(self):
        """Restore the original system default font"""
        try:
            if self.original_default_font and os.path.exists(self.original_default_font):
                LabelBase.register(name='default', fn_regular=self.original_default_font)
                print("🌐 System default font restored")
            else:
                # Try to use a common system font as fallback
                import platform
                if platform.system() == "Windows":
                    # Use standard Windows fonts
                    try:
                        LabelBase.register(name='default', fn_regular='C:/Windows/Fonts/arial.ttf')
                    except:
                        pass
                print("🌐 Font reset to system default")
            return True
        except Exception as e:
            print(f"❌ Error restoring default font: {e}")
            return False

    def _get_app_root(self):
        """Get the application root directory"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.dirname(current_dir)  # Go up one level from configs/

    def is_arabic_text(self, text):
        """Check if text contains Arabic characters"""
        if not text:
            return False
        return bool(re.search(r'[\u0600-\u06FF]', text))

    def apply_font(self, widget, text=None):
        """Apply Arabic font to widget if text contains Arabic"""
        if not self.fonts_registered:
            return

        text_to_check = text or getattr(widget, 'text', '')

        if self.is_arabic_text(text_to_check):
            widget.font_name = self.FONT_NAME

        # For Spinners, also apply font to their dropdown options
        from kivy.uix.spinner import Spinner
        if isinstance(widget, Spinner):
            # Apply font to the spinner text itself
            if hasattr(widget, 'font_name'):
                widget.font_name = self.FONT_NAME

            # Apply font to dropdown options if they contain Arabic
            if hasattr(widget, 'values'):
                for value in widget.values:
                    if self.is_arabic_text(value):
                        widget.font_name = self.FONT_NAME
                        break

# Global instance
_arabic_fonts = None

def init_arabic_fonts():
    """Initialize Arabic fonts (call once at app startup)"""
    global _arabic_fonts
    if _arabic_fonts is None:
        _arabic_fonts = ArabicFonts()
    return _arabic_fonts

def set_global_arabic_font():
    """Set Arabic as the global default font"""
    if _arabic_fonts is None:
        init_arabic_fonts()
    return _arabic_fonts.set_global_arabic_font()

def restore_default_font():
    """Restore system default font"""
    if _arabic_fonts is None:
        init_arabic_fonts()
    return _arabic_fonts.restore_default_font()

def apply_font_to_all_widgets(root_widget):
    """Apply Arabic font to all widgets in a widget tree"""
    if _arabic_fonts is None:
        init_arabic_fonts()

    if not _arabic_fonts.fonts_registered:
        return

    try:
        # Walk through all widgets in the tree
        for widget in root_widget.walk():
            if hasattr(widget, 'font_name'):
                # Check if the widget has Arabic text
                text_to_check = ""
                if hasattr(widget, 'text') and widget.text:
                    text_to_check = widget.text
                elif hasattr(widget, 'hint_text') and widget.hint_text:
                    text_to_check = widget.hint_text
                elif hasattr(widget, 'values') and widget.values:
                    text_to_check = " ".join(str(v) for v in widget.values)

                # Apply Arabic font if text contains Arabic characters
                if _arabic_fonts.is_arabic_text(text_to_check):
                    widget.font_name = _arabic_fonts.FONT_NAME

        print("🔄 Applied Arabic font to all existing widgets")
    except Exception as e:
        print(f"⚠️ Error applying font to existing widgets: {e}")

def apply_arabic_font(widget, text=None):
    """Apply Arabic font to widget if needed (for backward compatibility)"""
    if _arabic_fonts is None:
        init_arabic_fonts()
    _arabic_fonts.apply_font(widget, text)

def create_arabic_label(text="", **kwargs):
    """Create a label with Arabic font support"""
    label = Label(text=text, **kwargs)
    apply_arabic_font(label, text)
    return label

def create_arabic_button(text="", **kwargs):
    """Create a button with Arabic font support"""
    button = Button(text=text, **kwargs)
    apply_arabic_font(button, text)
    return button

def create_arabic_textinput(text="", **kwargs):
    """Create a text input with Arabic font support"""
    text_input = TextInput(text=text, **kwargs)
    apply_arabic_font(text_input, text)
    return text_input
