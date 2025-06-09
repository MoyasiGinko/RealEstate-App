"""
Developer Desktop Application Package

A best-practice Kivy desktop application with professional structure
and comprehensive features including database integration, configuration
management, logging, and modular architecture.

Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Developer"
__email__ = "developer@example.com"
__description__ = "Professional Kivy Desktop Application"

# Package imports
from .app import DeveloperApp
from .core import *
from .ui import *

__all__ = ['DeveloperApp']
