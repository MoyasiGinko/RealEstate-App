from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import os

# Load the KV file for the dashboard interface - use absolute path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir))
_kv_path = os.path.join(_project_root, 'assets', 'kv', 'dashboard.kv')
Builder.load_file(_kv_path)

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        # Initialize any necessary variables or components here

    def on_enter(self):
        # Code to execute when entering the dashboard screen
        pass

    def on_leave(self):
        # Code to execute when leaving the dashboard screen
        pass

    # Additional methods for dashboard functionalities can be added here