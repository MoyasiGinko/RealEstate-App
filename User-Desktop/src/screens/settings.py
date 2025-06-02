from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Add background color
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        title_label = Label(
            text='Settings',
            font_size=dp(24),
            size_hint_y=None,
            height=dp(60),
            color=(0.2, 0.2, 0.2, 1)
        )
        self.layout.add_widget(title_label)

        # Settings content area
        content_area = BoxLayout(orientation='vertical', spacing=dp(10))

        # Description
        description_label = Label(
            text='Configure your application settings here.',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(40),
            color=(0.4, 0.4, 0.4, 1)
        )
        content_area.add_widget(description_label)

        # Add some example settings (you can expand this)
        settings_info = Label(
            text='Settings functionality will be implemented here.\nThis includes database configuration, UI preferences, and more.',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(80),
            color=(0.5, 0.5, 0.5, 1),
            text_size=(None, None),
            halign='center'
        )
        content_area.add_widget(settings_info)

        self.layout.add_widget(content_area)

        # Spacer to push buttons to bottom
        self.layout.add_widget(Label())

        # Button layout at the bottom
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(20),
            padding=[0, dp(10), 0, 0]
        )

        # Back to Dashboard button
        back_button = Button(
            text='← Back to Dashboard',
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            background_color=(0.4, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        back_button.bind(on_press=self.go_to_dashboard)
        button_layout.add_widget(back_button)

        # Spacer between buttons
        button_layout.add_widget(Label())

        # Save Settings button
        self.save_button = Button(
            text='Save Settings',
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            background_color=(0.2, 0.7, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        self.save_button.bind(on_press=self.save_settings)
        button_layout.add_widget(self.save_button)

        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        """Update the background rectangle."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_to_dashboard(self, instance=None):
        """Navigate back to the dashboard."""
        self.manager.current = 'dashboard'

    def save_settings(self, instance):
        """Save the application settings."""
        # Logic to save settings goes here
        print("Settings saved!")

        # You can add actual settings saving logic here, such as:
        # - Saving to a configuration file
        # - Updating database settings
        # - Storing user preferences

        # For now, just show a confirmation message
        # In a real implementation, you might show a popup or toast message