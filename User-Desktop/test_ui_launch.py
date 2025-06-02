#!/usr/bin/env python3
"""
Quick UI launch test to verify the application can be opened.
This will attempt to launch the main application briefly.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from kivy.clock import Clock

def test_ui_launch():
    """Test that the UI can be launched without crashes"""
    print("🚀 Testing UI Launch...")

    try:
        # Import the main application
        from src.main import MainApp

        # Create the app instance
        app = MainApp()

        # Schedule the app to close after 3 seconds
        Clock.schedule_once(lambda dt: app.stop(), 3)

        print("  ✅ App instance created successfully")
        print("  🔄 Starting app (will auto-close in 3 seconds)...")

        # Try to run the app briefly
        app.run()

        print("  ✅ App launched and closed successfully!")
        return True

    except Exception as e:
        print(f"  ❌ UI Launch failed: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Real Estate Application UI Launch Test")
    print("=" * 50)

    success = test_ui_launch()

    print("=" * 50)
    if success:
        print("🎉 UI LAUNCH TEST PASSED!")
        print("✅ The application UI can be opened successfully!")
    else:
        print("❌ UI LAUNCH TEST FAILED!")
    print("=" * 50)
