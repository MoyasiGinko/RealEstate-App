# src/screens/__init__.py

from .dashboard import DashboardScreen
from .owner_management import OwnerManagementScreen
from .property_management import PropertyManagementScreen
from .search_report import SearchReportScreen
from .about_gui import SettingsScreen

__all__ = [
    "DashboardScreen",
    "OwnerManagementScreen",
    "PropertyManagementScreen",
    "SearchReportScreen",
    "SettingsScreen",
]