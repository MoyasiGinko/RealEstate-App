# src/screens/__init__.py

from .owner_management import OwnerManagementScreen
from .property_management import PropertyManagementScreen
from .browse_gui import SearchReportScreen
from .about_gui import AboutScreen
from .main_gui import MainScreen

__all__ = [
    "OwnerManagementScreen",
    "PropertyManagementScreen",
    "SearchReportScreen",
    "AboutScreen",
    "MainScreen",
]