from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.add_widget(Label(text='Settings', font_size='24sp'))

        self.add_widget(Label(text='Configure your application settings here.'))

        self.save_button = Button(text='Save Settings', size_hint_y=None, height=40)
        self.save_button.bind(on_press=self.save_settings)
        self.add_widget(self.save_button)

    def save_settings(self, instance):
        # Logic to save settings goes here
        print("Settings saved!")