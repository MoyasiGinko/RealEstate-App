# src/screens/__init__.py
from .main_gui import MainScreen
from .insert_gui import InsertScreen
from .update_gui import UpdateGUIScreen
from .browse_gui import SearchReportScreen
from .upload_gui import UploadScreen
from .about_gui import AboutScreen

__all__ = [
    "InsertScreen",
    "UpdateGUIScreen",
    "SearchReportScreen",
    "AboutScreen",
    "MainScreen",
    "UploadScreen"
]