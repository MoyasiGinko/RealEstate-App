#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Screen Arabic Font Integration Utility
Adds Arabic font support to existing screens with minimal code changes
"""

from configs.arabic_fonts import apply_arabic_font

class ArabicScreenMixin:
    """
    Mixin class to add Arabic font support to any screen.

    Usage:
    class YourScreen(ArabicScreenMixin, Screen):
        pass
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_enter=self.setup_arabic_fonts)

    def setup_arabic_fonts(self, *args):
        """Apply Arabic fonts to all text widgets in the screen"""
        try:
            for widget in self.walk(restrict=True):
                if hasattr(widget, 'text') and widget.text:
                    apply_arabic_font(widget, widget.text)
        except Exception as e:
            print(f"Error setting up Arabic fonts: {e}")

def add_arabic_support_to_screen(screen_instance):
    """
    Add Arabic font support to an existing screen instance.

    Args:
        screen_instance: The screen instance to add Arabic support to

    Usage:
        screen = YourScreen()
        add_arabic_support_to_screen(screen)
    """
    def setup_fonts(*args):
        try:
            for widget in screen_instance.walk(restrict=True):
                if hasattr(widget, 'text') and widget.text:
                    apply_arabic_font(widget, widget.text)
        except Exception as e:
            print(f"Error setting up Arabic fonts: {e}")

    # Bind the setup function to screen enter event
    screen_instance.bind(on_enter=setup_fonts)

# Example integration templates

SCREEN_INTEGRATION_TEMPLATE = '''
# Add this import at the top of your screen file:
from configs.screen_utils import ArabicScreenMixin

# Change your screen class definition from:
# class YourScreen(Screen):
#
# To:
class YourScreen(ArabicScreenMixin, Screen):
    pass

# That's it! Arabic fonts will be automatically applied.
'''

MANUAL_INTEGRATION_TEMPLATE = '''
# Add these imports at the top of your screen file:
from configs.arabic_fonts import apply_arabic_font

# Add this method to your screen class:
def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.bind(on_enter=self.setup_arabic_fonts)

def setup_arabic_fonts(self, *args):
    """Apply Arabic fonts to all text widgets"""
    for widget in self.walk(restrict=True):
        if hasattr(widget, 'text') and widget.text:
            apply_arabic_font(widget, widget.text)
'''
