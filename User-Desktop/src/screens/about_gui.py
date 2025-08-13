
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file('assets/kv/about_gui.kv')

class AboutScreen(Screen):
    def go_to_main_gui(self, instance=None):
        """Navigate back to the main GUI."""
        self.manager.current = 'main_gui'
