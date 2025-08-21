#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Language Switcher Widget
Provides a popup for language selection
"""

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from configs.language_manager import get_language_manager, get_text
from configs.arabic_fonts import apply_arabic_font

class LanguageSwitcherContent(BoxLayout):
    """Content widget for language switcher popup"""

    def __init__(self, popup_instance, **kwargs):
      super().__init__(**kwargs)
      self.popup = popup_instance
      self.language_manager = get_language_manager()
      self.orientation = 'vertical'
      self.spacing = 20
      self.padding = 30

      # Ensure modal (popup) title text color is black
      # Prefer setting a dedicated API if available; otherwise try common fallbacks.
      try:
        self.popup.title_color = (0, 0, 0, 1)
      except Exception:
        try:
          if hasattr(self.popup, 'title_label') and self.popup.title_label is not None:
            self.popup.title_label.color = (0, 0, 0, 1)
          else:
            for child in getattr(self.popup, 'children', []):
              if isinstance(child, Label) and child.text == getattr(self.popup, 'title', ''):
                child.color = (0, 0, 0, 1)
                break
        except Exception:
          pass

      self.build_ui()

    def build_ui(self):
        """Build the language selection UI"""
        # Title
        title_label = Label(
            text='Choose Language - اختر اللغة',
            font_size=24,
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=50,
            bold=True
        )
        apply_arabic_font(title_label, title_label.text)
        self.add_widget(title_label)

        # Language buttons
        buttons_layout = BoxLayout(
            orientation='horizontal',
            spacing=20,
            size_hint_y=None,
            height=80
        )

        # English button
        english_btn = Button(
            text='English\nإنجليزي',
            font_size=18,
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.5, 1)
        )
        english_btn.bind(on_press=lambda x: self.switch_language('en'))
        apply_arabic_font(english_btn, english_btn.text)
        buttons_layout.add_widget(english_btn)

        # Arabic button
        arabic_btn = Button(
            text='Arabic\nعربي',
            font_size=18,
            background_color=(0.6, 0.8, 0.2, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.5, 1)
        )
        arabic_btn.bind(on_press=lambda x: self.switch_language('ar'))
        apply_arabic_font(arabic_btn, arabic_btn.text)
        buttons_layout.add_widget(arabic_btn)

        self.add_widget(buttons_layout)

        # Current language indicator
        current_lang = self.language_manager.get_current_language()
        current_text = "English" if current_lang == 'en' else "العربية"

        self.current_label = Label(
            text=f'Current: {current_text} - الحالية: {current_text}',
            font_size=14,
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=30
        )
        apply_arabic_font(self.current_label, self.current_label.text)
        self.add_widget(self.current_label)

        # Close button
        close_btn = Button(
            text='Close - إغلاق',
            font_size=16,
            background_color=(0.6, 0.6, 0.6, 1),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=50
        )
        close_btn.bind(on_press=lambda x: self.popup.dismiss())
        apply_arabic_font(close_btn, close_btn.text)
        self.add_widget(close_btn)

    def switch_language(self, language_code):
        """Switch the application language"""
        self.language_manager.set_language(language_code)

        # Update current language indicator
        current_text = "English" if language_code == 'en' else "العربية"
        self.current_label.text = f'Current: {current_text} - الحالية: {current_text}'
        apply_arabic_font(self.current_label, self.current_label.text)

        # Close popup after a short delay
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.popup.dismiss(), 0.5)

class LanguageSwitcherPopup(Popup):
    """Popup for language selection"""

    def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.title = 'Language Settings'
      self.size_hint = (0.6, 0.5)
      self.auto_dismiss = True
      self.separator_color = (0.2, 0.6, 0.8, 1)
      self.background = ''  # Remove default image background
      self.background_color = (1, 1, 1, 1)  # Set background color to white

      # Apply Arabic font to title
      apply_arabic_font(self, self.title)

      # Create content
      content = LanguageSwitcherContent(self)
      self.content = content

def show_language_switcher():
    """Show the language switcher popup"""
    popup = LanguageSwitcherPopup()
    popup.open()
    return popup
