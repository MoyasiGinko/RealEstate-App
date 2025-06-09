"""
Settings Screen for application configuration with API management
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.app import App
import os


class SettingsScreen(BoxLayout):
    """Settings screen for application configuration"""

    def __init__(self, api_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.api_manager = api_manager
        self.build_ui()

    def build_ui(self):
        """Build settings UI"""
        # Header
        header = Label(
            text='Application Settings',
            font_size=24,
            size_hint_y=None,
            height=60,
            bold=True
        )
        self.add_widget(header)

        # Scrollable settings content
        scroll = ScrollView()
        settings_layout = GridLayout(
            cols=1,
            spacing=20,
            size_hint_y=None,
            padding=10
        )
        settings_layout.bind(minimum_height=settings_layout.setter('height'))

        # UI Settings
        ui_section = self.create_ui_settings()
        settings_layout.add_widget(ui_section)

        # Database Settings
        db_section = self.create_database_settings()
        settings_layout.add_widget(db_section)

        # Application Settings
        app_section = self.create_app_settings()
        settings_layout.add_widget(app_section)

        # Action buttons
        actions_section = self.create_action_buttons()
        settings_layout.add_widget(actions_section)

        scroll.add_widget(settings_layout)
        self.add_widget(scroll)

    def create_ui_settings(self):
        """Create UI settings section"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=200,
            spacing=10
        )

        # Section title
        title = Label(
            text='User Interface',
            font_size=18,
            size_hint_y=None,
            height=40,
            bold=True
        )
        section.add_widget(title)

        # Theme selection
        theme_layout = BoxLayout(size_hint_y=None, height=40)
        theme_layout.add_widget(Label(text='Theme:', size_hint_x=0.3))
        theme_spinner = Spinner(
            text='Light',
            values=['Light', 'Dark', 'Auto'],
            size_hint_x=0.7
        )
        theme_spinner.bind(text=self.on_theme_change)
        theme_layout.add_widget(theme_spinner)
        section.add_widget(theme_layout)

        # Font size
        font_layout = BoxLayout(size_hint_y=None, height=40)
        font_layout.add_widget(Label(text='Font Size:', size_hint_x=0.3))
        self.font_slider = Slider(
            min=10, max=20, value=14, step=1,
            size_hint_x=0.5
        )
        self.font_slider.bind(value=self.on_font_size_change)
        font_layout.add_widget(self.font_slider)
        self.font_label = Label(text='14', size_hint_x=0.2)
        font_layout.add_widget(self.font_label)
        section.add_widget(font_layout)

        # Auto-save toggle
        autosave_layout = BoxLayout(size_hint_y=None, height=40)
        autosave_layout.add_widget(Label(text='Auto-save:', size_hint_x=0.7))
        autosave_switch = Switch(active=True, size_hint_x=0.3)
        autosave_switch.bind(active=self.on_autosave_toggle)
        autosave_layout.add_widget(autosave_switch)
        section.add_widget(autosave_layout)

        return section

    def create_database_settings(self):
        """Create database settings section"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=280,
            spacing=10
        )

        # Section title
        title = Label(
            text='Database & API Settings',
            font_size=18,
            size_hint_y=None,
            height=40,
            bold=True
        )
        section.add_widget(title)

        # Database type selection
        db_type_layout = BoxLayout(size_hint_y=None, height=40)
        db_type_layout.add_widget(Label(text='Database Type:', size_hint_x=0.3))
        self.db_type_spinner = Spinner(
            text=os.getenv('DB_TYPE', 'sqlite'),
            values=['sqlite', 'mysql', 'postgresql'],
            size_hint_x=0.7
        )
        self.db_type_spinner.bind(text=self.on_db_type_change)
        db_type_layout.add_widget(self.db_type_spinner)
        section.add_widget(db_type_layout)

        # Connection status
        status_layout = BoxLayout(size_hint_y=None, height=40)
        status_layout.add_widget(Label(text='Connection Status:', size_hint_x=0.5))
        self.connection_status_label = Label(
            text='Checking...',
            size_hint_x=0.5,
            color=(1, 1, 0, 1)  # Yellow
        )
        status_layout.add_widget(self.connection_status_label)
        section.add_widget(status_layout)

        # Test connection button
        test_btn = Button(
            text='Test API Connection',
            size_hint_y=None,
            height=40
        )
        test_btn.bind(on_press=self.test_api_connection)
        section.add_widget(test_btn)

        # Database configuration button
        config_btn = Button(
            text='Configure Database',
            size_hint_y=None,
            height=40
        )
        config_btn.bind(on_press=self.show_database_config)
        section.add_widget(config_btn)

        # Auto-backup toggle
        backup_layout = BoxLayout(size_hint_y=None, height=40)
        backup_layout.add_widget(Label(text='Auto Backup:', size_hint_x=0.7))
        backup_switch = Switch(active=True, size_hint_x=0.3)
        backup_switch.bind(active=self.on_backup_toggle)
        backup_layout.add_widget(backup_switch)
        section.add_widget(backup_layout)        # Update connection status
        self.update_connection_status()

        return section

    def create_app_settings(self):
        """Create application settings section"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=120,
            spacing=10
        )

        # Section title
        title = Label(
            text='Application',
            font_size=18,
            size_hint_y=None,
            height=40,
            bold=True
        )
        section.add_widget(title)

        # Debug mode toggle
        debug_layout = BoxLayout(size_hint_y=None, height=40)
        debug_layout.add_widget(Label(text='Debug Mode:', size_hint_x=0.7))
        debug_switch = Switch(active=False, size_hint_x=0.3)
        debug_switch.bind(active=self.on_debug_toggle)
        debug_layout.add_widget(debug_switch)
        section.add_widget(debug_layout)

        # Log level
        log_layout = BoxLayout(size_hint_y=None, height=40)
        log_layout.add_widget(Label(text='Log Level:', size_hint_x=0.3))
        log_spinner = Spinner(
            text='INFO',
            values=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
            size_hint_x=0.7
        )
        log_spinner.bind(text=self.on_log_level_change)
        log_layout.add_widget(log_spinner)
        section.add_widget(log_layout)

        return section

    def create_action_buttons(self):
        """Create action buttons section"""
        section = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=60,
            spacing=20
        )

        # Save button
        save_btn = Button(text='Save Settings')
        save_btn.bind(on_press=self.on_save_settings)
        section.add_widget(save_btn)

        # Reset button
        reset_btn = Button(text='Reset to Defaults')
        reset_btn.bind(on_press=self.on_reset_settings)
        section.add_widget(reset_btn)

        # Export button
        export_btn = Button(text='Export Settings')
        export_btn.bind(on_press=self.on_export_settings)
        section.add_widget(export_btn)

        return section

    # Event handlers
    def on_theme_change(self, spinner, text):
        Logger.info(f"Theme changed to: {text}")

    def on_font_size_change(self, slider, value):
        self.font_label.text = str(int(value))
        Logger.info(f"Font size changed to: {int(value)}")

    def on_autosave_toggle(self, switch, value):
        Logger.info(f"Auto-save toggled: {value}")

    def on_backup_toggle(self, switch, value):
        Logger.info(f"Auto-backup toggled: {value}")

    def on_interval_change(self, slider, value):
        self.interval_label.text = str(int(value))
        Logger.info(f"Backup interval changed to: {int(value)} hours")

    def on_manual_backup(self, button):
        Logger.info("Manual backup requested")
        # Here you would trigger the actual backup
        button.text = "Backup Created!"
        # Reset button text after delay (you might want to use Clock.schedule_once)

    def on_debug_toggle(self, switch, value):
        Logger.info(f"Debug mode toggled: {value}")

    def on_log_level_change(self, spinner, text):
        Logger.info(f"Log level changed to: {text}")

    def on_save_settings(self, button):
        Logger.info("Settings saved")
        button.text = "Settings Saved!"

    def on_reset_settings(self, button):
        Logger.info("Settings reset to defaults")
        button.text = "Settings Reset!"

    def on_export_settings(self, button):
        Logger.info("Settings exported")
        button.text = "Settings Exported!"

    def on_db_type_change(self, spinner, text):
        """Handle database type change"""
        Logger.info(f"Database type changed to: {text}")
        # In a real app, you'd update the environment variable and restart connection

    def test_api_connection(self, button):
        """Test API connection"""
        if not self.api_manager:
            self.connection_status_label.text = "No API Manager"
            self.connection_status_label.color = (1, 0, 0, 1)  # Red
            return

        if not self.api_manager.is_initialized():
            self.connection_status_label.text = "Not Initialized"
            self.connection_status_label.color = (1, 0, 0, 1)  # Red
            return

        self.connection_status_label.text = "Testing..."
        self.connection_status_label.color = (1, 1, 0, 1)  # Yellow

        try:
            test_result = self.api_manager.test_connection()
            if test_result.success:
                self.connection_status_label.text = "Connected ✓"
                self.connection_status_label.color = (0, 1, 0, 1)  # Green
                Logger.info("API connection test successful")
            else:
                self.connection_status_label.text = "Failed ✗"
                self.connection_status_label.color = (1, 0, 0, 1)  # Red
                Logger.error(f"API connection test failed: {test_result.error}")
        except Exception as e:
            self.connection_status_label.text = "Error ✗"
            self.connection_status_label.color = (1, 0, 0, 1)  # Red
            Logger.error(f"Connection test error: {str(e)}")

    def update_connection_status(self):
        """Update connection status on load"""
        if not self.api_manager:
            self.connection_status_label.text = "No API Manager"
            self.connection_status_label.color = (1, 0, 0, 1)  # Red
            return

        if not self.api_manager.is_initialized():
            self.connection_status_label.text = "Not Initialized"
            self.connection_status_label.color = (1, 0, 0, 1)  # Red
            return

        # Quick status check without full test
        self.connection_status_label.text = "Initialized ✓"
        self.connection_status_label.color = (0, 1, 0, 1)  # Green

    def show_database_config(self, button):
        """Show database configuration dialog"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Title
        title = Label(text='Database Configuration', font_size=18, size_hint_y=None, height=40)
        content.add_widget(title)

        # Current configuration display
        config_info = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=150)

        current_type = os.getenv('DB_TYPE', 'sqlite')
        config_info.add_widget(Label(text=f"Current Type: {current_type}", size_hint_y=None, height=30))

        if current_type == 'sqlite':
            db_path = os.getenv('DATABASE_PATH', './data/local.db')
            config_info.add_widget(Label(text=f"Database Path: {db_path}", size_hint_y=None, height=30))
        else:
            host = os.getenv('DB_HOST', 'localhost')
            port = os.getenv('DB_PORT', '3306' if current_type == 'mysql' else '5432')
            name = os.getenv('DB_NAME', 'developer_app')
            config_info.add_widget(Label(text=f"Host: {host}:{port}", size_hint_y=None, height=30))
            config_info.add_widget(Label(text=f"Database: {name}", size_hint_y=None, height=30))

        if self.api_manager and self.api_manager.is_initialized():
            db_info_result = self.api_manager.get_database_info()
            if db_info_result.success:
                info = db_info_result.data
                config_info.add_widget(Label(text=f"Status: {info.get('status', 'Unknown')}", size_hint_y=None, height=30))

        content.add_widget(config_info)

        # Instructions
        instructions = Label(
            text="To change database settings:\n1. Edit the .env file\n2. Restart the application",
            size_hint_y=None,
            height=60,
            text_size=(None, None)
        )
        content.add_widget(instructions)

        # Close button
        close_btn = Button(text='Close', size_hint_y=None, height=40)
        content.add_widget(close_btn)

        # Create popup
        popup = Popup(
            title='Database Configuration',
            content=content,
            size_hint=(0.8, 0.7)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
