#!/usr/bin/env python3
"""
Main entry point for the Kivy Desktop Application
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.app import DeveloperApp


def main():
    """Main application entry point"""
    app = DeveloperApp()
    app.run()


if __name__ == "__main__":
    main()
