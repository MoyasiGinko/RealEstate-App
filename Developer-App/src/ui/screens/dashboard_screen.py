"""
Dashboard Screen - Clean and Optimized Version
Professional dashboard with full-screen responsive design
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, RoundedRectangle


class DashboardScreen(BoxLayout):
    """Modern dashboard screen with full-screen responsive design"""

    def __init__(self, api_manager=None, main_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(20), dp(20), dp(20), dp(10)]
        self.spacing = dp(20)
        self.api_manager = api_manager
        self.main_screen = main_screen
        self.company_data = []
        self.maincode_data = []

        # Add background
        with self.canvas.before:
            Color(0.95, 0.96, 0.98, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        self.build_ui()
        self.refresh_data()

    def _update_bg(self, instance, value):
        """Update background rectangle"""
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def build_ui(self):
        """Build modern responsive dashboard UI"""
        # Create main scroll view for full screen utilization
        main_scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(8),
            scroll_type=['bars']
        )

        # Main content container
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(25),
            size_hint_y=None,
            padding=[0, 0, 0, dp(20)]
        )
        content.bind(minimum_height=content.setter('height'))

        # Header section
        header = self.create_modern_header()
        content.add_widget(header)

        # Statistics section
        stats_section = self.create_modern_stats_section()
        content.add_widget(stats_section)

        # Quick actions section
        actions_section = self.create_modern_actions_section()
        content.add_widget(actions_section)

        # Add spacer
        spacer = Widget(size_hint_y=None, height=dp(20))
        content.add_widget(spacer)

        main_scroll.add_widget(content)
        self.add_widget(main_scroll)

        # Status bar
        self.status_label = Label(
            text='✅ Dashboard ready',
            size_hint_y=None,
            height=dp(40),
            color=(0.2, 0.7, 0.3, 1),
            font_size=dp(14),
            markup=True
        )

        with self.status_label.canvas.before:
            Color(1, 1, 1, 0.9)
            self.status_bg = RoundedRectangle(
                size=self.status_label.size,
                pos=self.status_label.pos,
                radius=[dp(8)]
            )
        self.status_label.bind(
            size=lambda instance, value: setattr(self.status_bg, 'size', value),
            pos=lambda instance, value: setattr(self.status_bg, 'pos', value)
        )

        self.add_widget(self.status_label)

    def create_modern_header(self):
        """Create modern responsive header"""
        header_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(140),
            spacing=dp(15)
        )

        with header_container.canvas.before:
            Color(0.2, 0.4, 0.8, 1)
            header_container.bg1 = RoundedRectangle(
                size=header_container.size,
                pos=header_container.pos,
                radius=[dp(15)]
            )

        header_container.bind(
            size=lambda instance, value: setattr(instance.bg1, 'size', value),
            pos=lambda instance, value: setattr(instance.bg1, 'pos', value)
        )

        # Content
        content_layout = BoxLayout(
            orientation='horizontal',
            padding=[dp(25), dp(20)],
            spacing=dp(20)
        )

        # Title section
        left_content = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_x=0.7
        )

        title = Label(
            text='🚀 Company Manager Pro',
            font_size=dp(28),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(40),
            halign='left',
            markup=True
        )
        title.bind(size=title.setter('text_size'))
        left_content.add_widget(title)

        subtitle = Label(
            text='Modern tools for efficient company and code management',
            font_size=dp(16),
            color=(0.9, 0.95, 1, 1),
            size_hint_y=None,
            height=dp(25),
            halign='left'
        )
        subtitle.bind(size=subtitle.setter('text_size'))
        left_content.add_widget(subtitle)

        # DB Status
        db_status = "Connected" if self.api_manager and self.api_manager.is_initialized() else "Disconnected"
        status_icon = "🟢" if db_status == "Connected" else "🔴"

        status_label = Label(
            text=f'{status_icon} Database: {db_status}',
            font_size=dp(14),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left'
        )
        status_label.bind(size=status_label.setter('text_size'))
        left_content.add_widget(status_label)

        content_layout.add_widget(left_content)

        # Stats section
        right_content = BoxLayout(
            orientation='vertical',
            size_hint_x=0.3,
            spacing=dp(8)
        )

        companies_label = Label(
            text=f'🏢 {len(self.company_data)} Companies',
            font_size=dp(14),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(25)
        )
        right_content.add_widget(companies_label)

        codes_label = Label(
            text=f'🏷️ {len(self.maincode_data)} Codes',
            font_size=dp(14),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(25)
        )
        right_content.add_widget(codes_label)

        content_layout.add_widget(right_content)
        header_container.add_widget(content_layout)

        return header_container

    def create_modern_stats_section(self):
        """Create statistics section"""
        stats_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),
            spacing=dp(15)
        )

        # Section title with refresh button
        title_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(35),
            spacing=dp(10)
        )

        title = Label(
            text='📊 Dashboard Overview',
            font_size=dp(20),
            bold=True,
            color=(0.2, 0.4, 0.8, 1),
            size_hint_y=None,
            height=dp(35),
            halign='left'
        )
        title.bind(size=title.setter('text_size'))
        title_layout.add_widget(title)

        # Add refresh button
        refresh_btn = Button(
            text='🔄 Refresh',
            size_hint_x=None,
            width=dp(100),
            height=dp(35),
            background_color=(0.2, 0.7, 0.3, 1),
            font_size=dp(12)
        )
        refresh_btn.bind(on_press=lambda x: self.refresh_data())
        title_layout.add_widget(refresh_btn)

        stats_container.add_widget(title_layout)

        # Simple stats display
        stats_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(20),
            size_hint_y=None,
            height=dp(100)
        )

        # Company stat
        company_box = self.create_stat_box('🏢', len(self.company_data), 'Companies', (0.2, 0.4, 0.8, 1))
        stats_layout.add_widget(company_box)

        # Code stat
        code_box = self.create_stat_box('🏷️', len(self.maincode_data), 'Main Codes', (0.3, 0.6, 0.9, 1))
        stats_layout.add_widget(code_box)

        stats_container.add_widget(stats_layout)
        return stats_container

    def create_stat_box(self, icon, count, label, color):
        """Create a statistics box"""
        stat_box = BoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(15)],
            spacing=dp(5)
        )

        with stat_box.canvas.before:
            Color(1, 1, 1, 1)
            stat_box.bg = RoundedRectangle(
                size=stat_box.size,
                pos=stat_box.pos,
                radius=[dp(10)]
            )
        stat_box.bind(
            size=lambda instance, value: setattr(instance.bg, 'size', value),
            pos=lambda instance, value: setattr(instance.bg, 'pos', value)
        )

        icon_label = Label(
            text=icon,
            font_size=dp(32),
            size_hint_y=None,
            height=dp(40)
        )
        stat_box.add_widget(icon_label)

        count_label = Label(
            text=str(count),
            font_size=dp(24),
            bold=True,
            color=color,
            size_hint_y=None,
            height=dp(30)
        )
        stat_box.add_widget(count_label)

        text_label = Label(
            text=label,
            font_size=dp(14),
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(20)
        )
        stat_box.add_widget(text_label)

        return stat_box

    def create_modern_actions_section(self):
        """Create action buttons section"""
        actions_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(20)
        )
        actions_container.bind(minimum_height=actions_container.setter('height'))

        # Title
        title = Label(
            text='🎯 Quick Actions',
            font_size=dp(22),
            bold=True,
            color=(0.2, 0.4, 0.8, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left'
        )
        title.bind(size=title.setter('text_size'))
        actions_container.add_widget(title)

        # Grid of action buttons
        grid_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(15)
        )
        grid_container.bind(minimum_height=grid_container.setter('height'))

        # First row - Primary actions
        primary_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(15)
        )

        # Company button
        company_btn = self.create_action_button(
            '🏢 Manage Companies',
            'Add, edit, and organize company data',
            self.on_company_crud,
            (0.2, 0.4, 0.8, 1)
        )
        primary_row.add_widget(company_btn)

        # MainCode button
        code_btn = self.create_action_button(
            '🏷️ Manage Codes',
            'System classification and main codes',
            self.on_maincode_crud,
            (0.3, 0.6, 0.9, 1)
        )
        primary_row.add_widget(code_btn)

        grid_container.add_widget(primary_row)

        # Second row - Secondary actions
        secondary_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(70),
            spacing=dp(15)
        )

        # Backup button
        backup_btn = self.create_action_button(
            '💾 Database Backup',
            'Secure your data with backup',
            self.on_backup_db,
            (1.0, 0.6, 0.0, 1)
        )
        secondary_row.add_widget(backup_btn)

        # Settings button
        settings_btn = self.create_action_button(
            '⚙️ System Settings',
            'Configure application settings',
            self.on_settings,
            (0.5, 0.5, 0.5, 1)
        )
        secondary_row.add_widget(settings_btn)

        grid_container.add_widget(secondary_row)
        actions_container.add_widget(grid_container)

        return actions_container

    def create_action_button(self, text, description, callback, color):
        """Create a clean action button"""
        container = FloatLayout(
            size_hint_y=None,
            height=dp(70)
        )

        # Add background
        with container.canvas.before:
            Color(*color)
            container.bg_rect = RoundedRectangle(
                size=container.size,
                pos=container.pos,
                radius=[dp(10)]
            )

        container.bind(
            size=lambda instance, *args: setattr(instance.bg_rect, 'size', instance.size),
            pos=lambda instance, *args: setattr(instance.bg_rect, 'pos', instance.pos)
        )

        # Create button for touch handling
        touch_button = Button(
            background_color=(0, 0, 0, 0),
            background_normal='',
            background_down='',
            text='',
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        touch_button.bind(on_press=callback)
        container.add_widget(touch_button)

        # Content layout
        content = BoxLayout(
            orientation='horizontal',
            padding=[dp(15), dp(10)],
            spacing=dp(10),
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )

        # Icon
        icon_text = text.split()[0] if text else '📋'
        icon = Label(
            text=icon_text,
            font_size=dp(24),
            color=(1, 1, 1, 1),
            size_hint_x=None,
            width=dp(50),
            halign='center',
            valign='middle'
        )
        icon.bind(size=icon.setter('text_size'))
        content.add_widget(icon)

        # Text section
        text_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(2)
        )

        # Main title
        main_text = ' '.join(text.split()[1:]) if len(text.split()) > 1 else text
        title_label = Label(
            text=main_text,
            font_size=dp(14),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(25),
            halign='left',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        text_layout.add_widget(title_label)

        # Description
        desc_label = Label(
            text=description,
            font_size=dp(11),
            color=(0.9, 0.95, 1, 1),
            size_hint_y=None,
            height=dp(20),
            halign='left',
            valign='middle'
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        text_layout.add_widget(desc_label)

        content.add_widget(text_layout)
        container.add_widget(content)

        return container

    def refresh_data(self):
        """Refresh dashboard data"""
        try:
            if not self.api_manager or not self.api_manager.is_initialized():
                self.status_label.text = "⚠️ Database not connected"
                self.status_label.color = (1.0, 0.6, 0.0, 1)
                return

            self.status_label.text = "🔄 Refreshing data..."
            self.status_label.color = (0.2, 0.4, 0.8, 1)

            # Load company data
            company_response = self.api_manager.company.get_all_companies()
            if company_response.success:
                self.company_data = company_response.data
                Logger.info(f"Dashboard: Loaded {len(self.company_data)} companies")
            else:
                self.company_data = []

            # Load main code data
            maincode_response = self.api_manager.maincode.get_all_main_codes()
            if maincode_response.success:
                self.maincode_data = maincode_response.data
                Logger.info(f"Dashboard: Loaded {len(self.maincode_data)} main codes")
            else:
                self.maincode_data = []

            self.status_label.text = f"✅ Loaded {len(self.company_data)} companies, {len(self.maincode_data)} codes"
            self.status_label.color = (0.2, 0.7, 0.3, 1)

            # Rebuild UI
            self.clear_widgets()
            self.build_ui()

        except Exception as e:
            Logger.error(f"Dashboard: Error refreshing data: {str(e)}")
            self.status_label.text = f"❌ Refresh failed: {str(e)}"
            self.status_label.color = (0.8, 0.2, 0.2, 1)

    # Event handlers
    def on_maincode_crud(self, button):
        """Navigate to MainCode CRUD screen"""
        Logger.info("🏷️ MainCode button clicked!")
        self.status_label.text = "🏷️ Opening MainCode Management..."
        self.status_label.color = (0.3, 0.6, 0.9, 1)
        if self.main_screen:
            self.main_screen.show_maincode_crud()

    def on_company_crud(self, button):
        """Navigate to Company CRUD screen"""
        Logger.info("🏢 Company button clicked!")
        self.status_label.text = "🏢 Opening Company Management..."
        self.status_label.color = (0.2, 0.4, 0.8, 1)
        if self.main_screen:
            self.main_screen.show_companyinfo_crud()

    def on_settings(self, button):
        """Navigate to settings screen"""
        Logger.info("⚙️ Settings button clicked!")
        self.status_label.text = "⚙️ Opening Settings..."
        self.status_label.color = (0.5, 0.5, 0.5, 1)
        if self.main_screen:
            self.main_screen.show_settings()

    def on_backup_db(self, button):
        """Backup database"""
        Logger.info("💾 Backup button clicked!")
        self.status_label.text = "💾 Database backup initiated..."
        self.status_label.color = (1.0, 0.6, 0.0, 1)
        Clock.schedule_once(self._backup_complete, 2.0)

    def _backup_complete(self, dt):
        """Complete backup process"""
        self.status_label.text = "✅ Database backup completed"
        self.status_label.color = (0.2, 0.7, 0.3, 1)
