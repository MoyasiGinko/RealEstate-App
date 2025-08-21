#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production Arabic Font Configuration
Clean and simple Arabic font support for the Real Estate Management System
"""

from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import os
import re

class ArabicFonts:
    """Production-ready Arabic font support"""

    FONT_NAME = 'ArabicFont'

    def __init__(self):
        self.fonts_registered = False
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

# Global instance
_arabic_fonts = None

def init_arabic_fonts():
    """Initialize Arabic fonts (call once at app startup)"""
    global _arabic_fonts
    if _arabic_fonts is None:
        _arabic_fonts = ArabicFonts()
    return _arabic_fonts

def apply_arabic_font(widget, text=None):
    """Apply Arabic font to widget if needed"""
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
