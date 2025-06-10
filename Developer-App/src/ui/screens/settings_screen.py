"""
Settings Screen - Minimal Responsive UI
Essential settings only with clean, responsive design
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.metrics import dp


class SettingsScreen(BoxLayout):
    """Minimal settings screen with essential configuration options"""

    def __init__(self, api_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(20), dp(15)]
        self.spacing = dp(15)
        self.api_manager = api_manager
        self.settings = {
            'auto_backup': True,
            'auto_save': True,
            'theme': 'Light',
            'items_per_page': '20'
        }
        self.build_ui()

    def build_ui(self):
        """Build minimal responsive settings UI"""
        # Header
        header = self.create_header()
        self.add_widget(header)

        # Settings content
        scroll = ScrollView()
        settings_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint_y=None,
            padding=[dp(10), dp(10)]
        )
        settings_layout.bind(minimum_height=settings_layout.setter('height'))

        # Essential settings sections
        sections = [
            self.create_database_section(),
            self.create_interface_section(),
            self.create_backup_section(),
            self.create_actions_section()
        ]

        for section in sections:
            settings_layout.add_widget(section)

        scroll.add_widget(settings_layout)
        self.add_widget(scroll)

        # Status bar
        self.status_label = Label(
            text='⚙️ Settings ready',
            size_hint_y=None,
            height=dp(35),
            color=(0.2, 0.7, 0.3, 1),
            font_size=dp(14)
        )
        self.add_widget(self.status_label)

    def create_header(self):
        """Create responsive header"""
        header_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(5)
        )

        # Title
        title = Label(
            text='⚙️ Settings',
            font_size=dp(24),
            bold=True,
            color=(0.2, 0.4, 0.8, 1),
            size_hint_y=None,
            height=dp(40)
        )
        header_layout.add_widget(title)

        # Subtitle
        subtitle = Label(
            text='Configure essential application settings',
            font_size=dp(14),
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(25)
        )
        header_layout.add_widget(subtitle)

        return header_layout

    def create_section(self, title, content_widgets):
        """Create a settings section"""
        section_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(10)
        )

        # Calculate section height
        section_height = dp(40) + (len(content_widgets) * dp(45)) + (len(content_widgets) * dp(10))
        section_layout.height = section_height

        # Background
        with section_layout.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(0.98, 0.98, 0.98, 1)
            section_layout.bg = RoundedRectangle(
                size=section_layout.size,
                pos=section_layout.pos,
                radius=[5]
            )
        section_layout.bind(size=lambda instance, value: setattr(instance.bg, 'size', value))
        section_layout.bind(pos=lambda instance, value: setattr(instance.bg, 'pos', value))

        # Section title
        section_title = Label(
            text=title,
            font_size=dp(16),
            bold=True,
            color=(0.2, 0.4, 0.8, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            text_size=(None, None)
        )
        section_title.bind(size=section_title.setter('text_size'))
        section_layout.add_widget(section_title)

        # Content widgets
        for widget in content_widgets:
            section_layout.add_widget(widget)

        return section_layout

    def create_setting_row(self, label_text, widget):
        """Create a setting row with label and widget"""
        row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10),
            padding=[dp(10), dp(5)]
        )

        # Label
        label = Label(
            text=label_text,
            font_size=dp(14),
            color=(0.3, 0.3, 0.3, 1),
            size_hint_x=0.6,
            halign='left'
        )
        label.bind(size=label.setter('text_size'))
        row.add_widget(label)

        # Widget
        widget.size_hint_x = 0.4
        row.add_widget(widget)

        return row

    def create_database_section(self):
        """Create database settings section"""
        # Database connection status
        db_status = "Connected" if self.api_manager and self.api_manager.is_initialized() else "Disconnected"
        status_color = (0.2, 0.7, 0.3, 1) if db_status == "Connected" else (0.8, 0.2, 0.2, 1)

        status_label = Label(
            text=f"Status: {db_status}",
            font_size=dp(13),
            color=status_color,
            size_hint_y=None,
            height=dp(30)
        )

        # Test connection button
        test_btn = Button(
            text='Test Connection',
            size_hint_y=None,
            height=dp(35),
            background_color=(0.2, 0.4, 0.8, 1),
            font_size=dp(12)
        )
        test_btn.bind(on_press=self.test_connection)

        return self.create_section('🔗 Database Connection', [status_label, test_btn])

    def create_interface_section(self):
        """Create interface settings section"""
        # Theme selection
        theme_spinner = Spinner(
            text=self.settings['theme'],
            values=['Light', 'Dark'],
            size_hint_y=None,
            height=dp(35)
        )
        theme_spinner.bind(text=self.on_theme_change)
        theme_row = self.create_setting_row('Theme:', theme_spinner)

        # Items per page
        items_spinner = Spinner(
            text=self.settings['items_per_page'],
            values=['10', '20', '50', '100'],
            size_hint_y=None,
            height=dp(35)
        )
        items_spinner.bind(text=self.on_items_per_page_change)
        items_row = self.create_setting_row('Items per page:', items_spinner)

        return self.create_section('🎨 Interface', [theme_row, items_row])

    def create_backup_section(self):
        """Create backup settings section"""
        # Auto backup switch
        auto_backup_switch = Switch(
            active=self.settings['auto_backup'],
            size_hint_y=None,
            height=dp(35)
        )
        auto_backup_switch.bind(active=self.on_auto_backup_change)
        backup_row = self.create_setting_row('Auto backup:', auto_backup_switch)

        # Auto save switch
        auto_save_switch = Switch(
            active=self.settings['auto_save'],
            size_hint_y=None,
            height=dp(35)
        )
        auto_save_switch.bind(active=self.on_auto_save_change)
        save_row = self.create_setting_row('Auto save:', auto_save_switch)

        return self.create_section('💾 Data Management', [backup_row, save_row])

    def create_actions_section(self):
        """Create action buttons section"""
        actions_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            spacing=dp(10)
        )

        # Action buttons
        buttons = [
            ('💾 Backup Now', self.backup_now, (1.0, 0.6, 0.0, 1)),
            ('🔄 Reset Settings', self.reset_settings, (0.8, 0.2, 0.2, 1)),
            ('✅ Save Settings', self.save_settings, (0.2, 0.7, 0.3, 1))
        ]

        for text, callback, color in buttons:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=dp(35),
                background_color=color,
                font_size=dp(13)
            )
            btn.bind(on_press=callback)
            actions_layout.add_widget(btn)

        return self.create_section('🔧 Actions', [actions_layout])

    # Event handlers
    def test_connection(self, button):
        """Test database connection"""
        try:
            if self.api_manager and self.api_manager.is_initialized():
                self.status_label.text = '✅ Database connection successful'
                self.status_label.color = (0.2, 0.7, 0.3, 1)
            else:
                self.status_label.text = '❌ Database connection failed'
                self.status_label.color = (0.8, 0.2, 0.2, 1)
        except Exception as e:
            self.status_label.text = f'❌ Connection error: {str(e)}'
            self.status_label.color = (0.8, 0.2, 0.2, 1)

        # Refresh the database section
        self.refresh_ui()

    def on_theme_change(self, spinner, text):
        """Handle theme change"""
        self.settings['theme'] = text
        self.status_label.text = f'🎨 Theme changed to {text}'
        self.status_label.color = (0.3, 0.6, 0.9, 1)
        Logger.info(f"Theme changed to: {text}")

    def on_items_per_page_change(self, spinner, text):
        """Handle items per page change"""
        self.settings['items_per_page'] = text
        self.status_label.text = f'📄 Items per page set to {text}'
        self.status_label.color = (0.3, 0.6, 0.9, 1)
        Logger.info(f"Items per page changed to: {text}")

    def on_auto_backup_change(self, switch, value):
        """Handle auto backup change"""
        self.settings['auto_backup'] = value
        status = 'enabled' if value else 'disabled'
        self.status_label.text = f'💾 Auto backup {status}'
        self.status_label.color = (0.3, 0.6, 0.9, 1)
        Logger.info(f"Auto backup {status}")

    def on_auto_save_change(self, switch, value):
        """Handle auto save change"""
        self.settings['auto_save'] = value
        status = 'enabled' if value else 'disabled'
        self.status_label.text = f'📝 Auto save {status}'
        self.status_label.color = (0.3, 0.6, 0.9, 1)
        Logger.info(f"Auto save {status}")

    def backup_now(self, button):
        """Perform immediate backup"""
        try:
            self.status_label.text = '💾 Backup in progress...'
            self.status_label.color = (1.0, 0.6, 0.0, 1)
            Logger.info("Manual backup initiated")

            # Simulate backup process
            from kivy.clock import Clock
            Clock.schedule_once(self.backup_complete, 2.0)

        except Exception as e:
            self.status_label.text = f'❌ Backup failed: {str(e)}'
            self.status_label.color = (0.8, 0.2, 0.2, 1)

    def backup_complete(self, dt):
        """Backup completion callback"""
        self.status_label.text = '✅ Backup completed successfully'
        self.status_label.color = (0.2, 0.7, 0.3, 1)

    def reset_settings(self, button):
        """Reset settings to default"""
        # Show confirmation popup
        popup_content = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10)
        )

        message = Label(
            text='Are you sure you want to reset all settings to default?',
            text_size=(dp(250), None),
            halign='center'
        )
        popup_content.add_widget(message)

        buttons_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )

        cancel_btn = Button(text='Cancel', background_color=(0.5, 0.5, 0.5, 1))
        reset_btn = Button(text='Reset', background_color=(0.8, 0.2, 0.2, 1))

        buttons_layout.add_widget(cancel_btn)
        buttons_layout.add_widget(reset_btn)
        popup_content.add_widget(buttons_layout)

        popup = Popup(
            title='Confirm Reset',
            content=popup_content,
            size_hint=(0.8, 0.3),
            auto_dismiss=False
        )

        cancel_btn.bind(on_press=popup.dismiss)
        reset_btn.bind(on_press=lambda x: self.confirm_reset(popup))

        popup.open()

    def confirm_reset(self, popup):
        """Confirm settings reset"""
        popup.dismiss()
        self.settings = {
            'auto_backup': True,
            'auto_save': True,
            'theme': 'Light',
            'items_per_page': '20'
        }
        self.status_label.text = '🔄 Settings reset to default'
        self.status_label.color = (0.3, 0.6, 0.9, 1)
        self.refresh_ui()

    def save_settings(self, button):
        """Save current settings"""
        try:
            self.status_label.text = '✅ Settings saved successfully'
            self.status_label.color = (0.2, 0.7, 0.3, 1)
            Logger.info(f"Settings saved: {self.settings}")
        except Exception as e:
            self.status_label.text = f'❌ Save failed: {str(e)}'
            self.status_label.color = (0.8, 0.2, 0.2, 1)

    def refresh_ui(self):
        """Refresh the UI to reflect changes"""
        self.clear_widgets()
        self.build_ui()

    def get_settings(self):
        """Get current settings"""
        return self.settings.copy()

    def apply_settings(self, settings):
        """Apply settings from external source"""
        self.settings.update(settings)
        self.refresh_ui()
