from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import os

# Load the KV file for the main_gui interface - use absolute path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir))
_kv_path = os.path.join(_project_root, 'assets', 'kv', 'upload_gui.kv')
Builder.load_file(_kv_path)

class UploadScreen(Screen):
  pass