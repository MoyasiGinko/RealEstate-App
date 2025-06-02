from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class CustomButton(Button):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.size_hint = (None, None)
        self.size = (200, 50)
        self.background_color = (0.2, 0.6, 0.8, 1)  # Custom color

class CustomLabel(Label):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = 20
        self.color = (1, 1, 1, 1)  # White color

class CustomBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Example usage of custom widgets
        self.add_widget(CustomLabel("Welcome to User-Desktop App"))
        self.add_widget(CustomButton("Click Me"))