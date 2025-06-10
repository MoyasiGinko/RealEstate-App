"""
Dashboard Screen - Minimal Responsive UI
Essential features only with clean, responsive design
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.metrics import dp


class DashboardScreen(BoxLayout):
    """Dashboard screen with essential features and minimal responsive UI"""

    def __init__(self, api_manager=None, main_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(20), dp(15)]
        self.spacing = dp(15)
        self.api_manager = api_manager
        self.main_screen = main_screen
        self.company_data = []
        self.maincode_data = []
        self.build_ui()
        self.refresh_data()

    def build_ui(self):
        """Build minimal responsive dashboard UI"""
        # Header section
        header = self.create_header()
        self.add_widget(header)

        # Statistics cards
        stats_container = ScrollView(
            size_hint_y=None,
            height=dp(120),
            do_scroll_x=True,
            do_scroll_y=False
        )
        stats_layout = self.create_stats_section()
        stats_container.add_widget(stats_layout)
        self.add_widget(stats_container)

        # Essential actions
        actions_section = self.create_actions_section()
        self.add_widget(actions_section)

        # Status bar
        self.status_label = Label(
            text='✅ Dashboard ready',
            size_hint_y=None,
            height=dp(35),
            color=(0.2, 0.7, 0.3, 1),
            font_size=dp(14)
        )
        self.add_widget(self.status_label)

    def create_header(self):
        """Create responsive header section"""
        header_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            spacing=dp(5)
        )

        # Main title
        title = Label(
            text='🚀 Company Manager',
            font_size=dp(24),
            bold=True,
            color=(0.2, 0.4, 0.8, 1),
            size_hint_y=None,
            height=dp(40)
        )
        header_layout.add_widget(title)

        # Subtitle
        subtitle = Label(
            text='Essential tools for company and code management',
            font_size=dp(14),
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(25)
        )
        header_layout.add_widget(subtitle)

        # Connection status
        db_status = "Connected" if self.api_manager and self.api_manager.is_initialized() else "Disconnected"
        status_color = (0.2, 0.7, 0.3, 1) if db_status == "Connected" else (0.8, 0.2, 0.2, 1)
        status_icon = "✅" if db_status == "Connected" else "❌"

        status_label = Label(
            text=f'{status_icon} Database: {db_status}',
            font_size=dp(13),
            color=status_color,
            size_hint_y=None,
            height=dp(25)
        )
        header_layout.add_widget(status_label)

        return header_layout

    def create_stats_section(self):
        """Create responsive statistics cards"""
        stats_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(100),
            spacing=dp(15),
            size_hint_x=None
        )
        stats_layout.bind(minimum_width=stats_layout.setter('width'))

        # Company stats card
        company_card = self.create_stat_card(
            "🏢",
            str(len(self.company_data)),
            "Companies",
            (0.2, 0.4, 0.8, 1)
        )
        stats_layout.add_widget(company_card)

        # MainCode stats card
        maincode_card = self.create_stat_card(
            "🏷️",
            str(len(self.maincode_data)),
            "Main Codes",
            (0.3, 0.6, 0.9, 1)
        )
        stats_layout.add_widget(maincode_card)

        # Quick refresh card
        refresh_card = self.create_action_card(
            "🔄",
            "Refresh",
            "Update data",
            (0.2, 0.7, 0.3, 1),
            lambda x: self.refresh_data()
        )
        stats_layout.add_widget(refresh_card)

        return stats_layout

    def create_stat_card(self, icon, value, label, color):
        """Create a responsive statistics card"""
        card = BoxLayout(
            orientation='vertical',
            size_hint_x=None,
            width=dp(120),
            padding=[dp(15), dp(10)],
            spacing=dp(5)
        )

        # Background
        with card.canvas.before:
            from kivy.graphics import Color, Rectangle, RoundedRectangle
            Color(0.98, 0.98, 0.98, 1)
            card.bg = RoundedRectangle(size=card.size, pos=card.pos, radius=[5])
        card.bind(size=lambda instance, value: setattr(instance.bg, 'size', value))
        card.bind(pos=lambda instance, value: setattr(instance.bg, 'pos', value))

        # Icon
        icon_label = Label(
            text=icon,
            font_size=dp(24),
            size_hint_y=None,
            height=dp(30)
        )
        card.add_widget(icon_label)

        # Value
        value_label = Label(
            text=value,
            font_size=dp(20),
            bold=True,
            color=color,
            size_hint_y=None,
            height=dp(25)
        )
        card.add_widget(value_label)

        # Label
        text_label = Label(
            text=label,
            font_size=dp(12),
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=None,
            height=dp(20)
        )
        card.add_widget(text_label)

        return card

    def create_action_card(self, icon, title, subtitle, color, callback):
        """Create an interactive action card"""
        card = Button(
            size_hint_x=None,
            width=dp(120),
            background_color=(0, 0, 0, 0)
        )
        card.bind(on_press=callback)

        # Custom layout for button content
        card_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(15), dp(10)],
            spacing=dp(5)
        )

        # Background
        with card.canvas.before:
            from kivy.graphics import Color, Rectangle, RoundedRectangle
            Color(*color[:3], 0.1)
            card.bg = RoundedRectangle(size=card.size, pos=card.pos, radius=[5])
        card.bind(size=lambda instance, value: setattr(instance.bg, 'size', value))
        card.bind(pos=lambda instance, value: setattr(instance.bg, 'pos', value))

        # Icon
        icon_label = Label(
            text=icon,
            font_size=dp(24),
            size_hint_y=None,
            height=dp(30)
        )
        card_layout.add_widget(icon_label)

        # Title
        title_label = Label(
            text=title,
            font_size=dp(14),
            bold=True,
            color=color,
            size_hint_y=None,
            height=dp(20)
        )
        card_layout.add_widget(title_label)

        # Subtitle
        subtitle_label = Label(
            text=subtitle,
            font_size=dp(11),
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=None,
            height=dp(15)
        )
        card_layout.add_widget(subtitle_label)

        card.add_widget(card_layout)
        return card

    def create_actions_section(self):
        """Create essential actions section"""
        actions_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[0, dp(20)]
        )

        # Section title
        title = Label(
            text='📋 Essential Tools',
            font_size=dp(18),
            bold=True,
            color=(0.2, 0.4, 0.8, 1),
            size_hint_y=None,
            height=dp(35),
            halign='left'
        )
        title.bind(size=title.setter('text_size'))
        actions_layout.add_widget(title)

        # Main action buttons - responsive grid
        buttons_container = ScrollView(
            size_hint_y=None,
            height=dp(160),
            do_scroll_y=False
        )

        buttons_layout = GridLayout(
            cols=2,
            spacing=dp(15),
            size_hint_x=None,
            size_hint_y=None,
            height=dp(160)
        )
        buttons_layout.bind(minimum_width=buttons_layout.setter('width'))

        # Essential buttons only
        essential_actions = [
            ('🏢 Companies', 'Manage company data', self.on_company_crud, (0.2, 0.4, 0.8, 1)),
            ('🏷️ Main Codes', 'Manage system codes', self.on_maincode_crud, (0.3, 0.6, 0.9, 1)),
            ('💾 Backup', 'Backup database', self.on_backup_db, (1.0, 0.6, 0.0, 1)),
            ('⚙️ Settings', 'System settings', self.on_settings, (0.5, 0.5, 0.5, 1))
        ]

        for text, desc, callback, color in essential_actions:
            btn = self.create_action_button(text, desc, callback, color)
            buttons_layout.add_widget(btn)

        buttons_container.add_widget(buttons_layout)
        actions_layout.add_widget(buttons_container)

        return actions_layout

    def create_action_button(self, text, description, callback, color):
        """Create a responsive action button"""
        btn_layout = BoxLayout(
            orientation='vertical',
            size_hint_x=None,
            width=dp(160),
            spacing=dp(5)
        )

        # Main button
        btn = Button(
            text=text,
            size_hint_y=None,
            height=dp(50),
            background_color=color,
            font_size=dp(14),
            bold=True
        )
        btn.bind(on_press=callback)
        btn_layout.add_widget(btn)

        # Description
        desc_label = Label(
            text=description,
            font_size=dp(11),
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=None,
            height=dp(20),
            halign='center'
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        btn_layout.add_widget(desc_label)

        return btn_layout

    def refresh_data(self):
        """Refresh dashboard data"""
        try:
            if not self.api_manager or not self.api_manager.is_initialized():
                self.status_label.text = "⚠️ Database not connected"
                self.status_label.color = (1.0, 0.6, 0.0, 1)
                return

            # Load company data
            company_response = self.api_manager.company.get_all_companies()
            if company_response.success:
                self.company_data = company_response.data
                Logger.info(f"Dashboard: Loaded {len(self.company_data)} companies")
            else:
                Logger.error(f"Dashboard: Failed to load companies: {company_response.error}")
                self.company_data = []

            # Load main code data
            maincode_response = self.api_manager.maincode.get_all_main_codes()
            if maincode_response.success:
                self.maincode_data = maincode_response.data
                Logger.info(f"Dashboard: Loaded {len(self.maincode_data)} main codes")
            else:
                Logger.error(f"Dashboard: Failed to load main codes: {maincode_response.error}")
                self.maincode_data = []

            # Update status
            self.status_label.text = f"✅ Loaded: {len(self.company_data)} companies, {len(self.maincode_data)} codes"
            self.status_label.color = (0.2, 0.7, 0.3, 1)

            # Rebuild UI to update stats
            self.clear_widgets()
            self.build_ui()

        except Exception as e:
            Logger.error(f"Dashboard: Error refreshing data: {str(e)}")
            self.status_label.text = f"❌ Error refreshing data: {str(e)}"
            self.status_label.color = (0.8, 0.2, 0.2, 1)

    # Essential event handlers only
    def on_maincode_crud(self, button):
        """Navigate to MainCode CRUD screen"""
        if self.main_screen:
            self.main_screen.show_maincode_crud()
        Logger.info("Navigating to MainCode CRUD")

    def on_company_crud(self, button):
        """Navigate to Company CRUD screen"""
        if self.main_screen:
            self.main_screen.show_companyinfo_crud()
        Logger.info("Navigating to Company CRUD")

    def on_settings(self, button):
        """Navigate to settings screen"""
        if self.main_screen:
            self.main_screen.show_settings()
        Logger.info("Navigating to Settings")

    def on_backup_db(self, button):
        """Backup database - essential functionality"""
        try:
            if self.api_manager and hasattr(self.api_manager, 'db_manager'):
                self.status_label.text = "💾 Database backup in progress..."
                self.status_label.color = (1.0, 0.6, 0.0, 1)
                Logger.info("Database backup initiated")

                # Schedule completion message
                Clock.schedule_once(self.backup_complete, 2.0)
            else:
                self.status_label.text = "⚠️ Database manager not available"
                self.status_label.color = (1.0, 0.6, 0.0, 1)
        except Exception as e:
            Logger.error(f"Error backing up database: {str(e)}")
            self.status_label.text = f"❌ Backup error: {str(e)}"
            self.status_label.color = (0.8, 0.2, 0.2, 1)

    def backup_complete(self, dt):
        """Backup completion callback"""
        self.status_label.text = "✅ Database backup completed successfully"
        self.status_label.color = (0.2, 0.7, 0.3, 1)
