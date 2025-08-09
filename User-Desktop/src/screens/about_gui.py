from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)

        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Add background color
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        title_label = Label(
            text='About',
            font_size=dp(24),
            size_hint_y=None,
            height=dp(60),
            color=(0.2, 0.2, 0.2, 1)
        )
        self.layout.add_widget(title_label)

        # About content area
        content_area = BoxLayout(orientation='vertical', spacing=dp(10))

        # App Name
        app_name_label = Label(
            text='MyApp',
            font_size=dp(20),
            size_hint_y=None,
            height=dp(40),
            color=(0.3, 0.3, 0.6, 1)
        )
        content_area.add_widget(app_name_label)

        # Version
        version_label = Label(
            text='Version: 1.0.0',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(30),
            color=(0.4, 0.4, 0.4, 1)
        )
        content_area.add_widget(version_label)

        # Author
        author_label = Label(
            text='Author: Luay Alkawaz',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(30),
            color=(0.4, 0.4, 0.4, 1)
        )
        content_area.add_widget(author_label)

        # Description
        description_label = Label(
            text='This application helps users manage their tasks efficiently and intuitively.\nThank you for using MyApp!',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(60),
            color=(0.5, 0.5, 0.5, 1),
            halign='center',
            valign='middle'
        )
        description_label.bind(size=lambda s, _: s.setter('text_size')(s, s.size))
        content_area.add_widget(description_label)

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

        # Back to Main button
        back_button = Button(
            text='← Back to Main',
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            background_color=(0.4, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        back_button.bind(on_press=self.go_to_main_gui)
        button_layout.add_widget(back_button)

        # Spacer between buttons
        button_layout.add_widget(Label())

        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        """Update the background rectangle."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_to_main_gui(self, instance=None):
        """Navigate back to the main GUI."""
        self.manager.current = 'main_gui'
