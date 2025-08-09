from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import os

# Load the KV file for the main_gui interface - use absolute path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir))
_kv_path = os.path.join(_project_root, 'assets', 'kv', 'main_gui.kv')
Builder.load_file(_kv_path)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # Initialize any necessary variables or components here

    def on_enter(self):
        # Code to execute when entering the main screen
        pass

    def on_leave(self):
        # Code to execute when leaving the main screen
        pass

    # Additional methods for main screen functionalities can be added here