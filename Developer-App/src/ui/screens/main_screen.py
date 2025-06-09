"""
Main Screen of the Application
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.logger import Logger
from kivy.app import App

from ..widgets.status_bar import StatusBar
from .dashboard_screen import DashboardScreen
from .settings_screen import SettingsScreen
from .maincode_crud_screen import MainCodeCRUDScreen
from .companyinfo_crud_screen import CompanyInfoCRUDScreen


class MainScreen(BoxLayout):
    """Main application screen with navigation"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.build_ui()

    def build_ui(self):
        """Build the main UI components"""
        # Get the app instance to access API manager
        self.app = App.get_running_app()

        # Add toolbar
        self.toolbar = self.create_simple_toolbar()
        self.add_widget(self.toolbar)

        # Add screen manager for different views
        self.screen_manager = ScreenManager()        # Create screens with API access
        self.dashboard_screen = Screen(name='dashboard')
        self.dashboard_widget = DashboardScreen(api_manager=getattr(self.app, 'api_manager', None), main_screen=self)
        self.dashboard_screen.add_widget(self.dashboard_widget)

        self.settings_screen = Screen(name='settings')
        self.settings_widget = SettingsScreen(api_manager=getattr(self.app, 'api_manager', None))
        self.settings_screen.add_widget(self.settings_widget)

        # Create CRUD screens
        self.maincode_crud_screen = Screen(name='maincode_crud')
        self.maincode_crud_widget = MainCodeCRUDScreen(api_manager=getattr(self.app, 'api_manager', None), main_screen=self)
        self.maincode_crud_screen.add_widget(self.maincode_crud_widget)

        self.companyinfo_crud_screen = Screen(name='companyinfo_crud')
        self.companyinfo_crud_widget = CompanyInfoCRUDScreen(api_manager=getattr(self.app, 'api_manager', None), main_screen=self)
        self.companyinfo_crud_screen.add_widget(self.companyinfo_crud_widget)

        # Add screens to manager
        self.screen_manager.add_widget(self.dashboard_screen)
        self.screen_manager.add_widget(self.settings_screen)
        self.screen_manager.add_widget(self.maincode_crud_screen)
        self.screen_manager.add_widget(self.companyinfo_crud_screen)

        # Set default screen
        self.screen_manager.current = 'dashboard'

        self.add_widget(self.screen_manager)

        # Add status bar with API connection monitoring
        self.status_bar = StatusBar(api_manager=getattr(self.app, 'api_manager', None))
        self.add_widget(self.status_bar)

        Logger.info("Main screen initialized")

    def create_simple_toolbar(self):
        """Create a simple toolbar with basic navigation"""
        toolbar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)

        # Dashboard button
        dashboard_btn = Button(text="Dashboard", size_hint=(0.2, 1))
        dashboard_btn.bind(on_press=lambda x: self.on_menu_select(None, 'dashboard'))
        toolbar.add_widget(dashboard_btn)

        # Settings button
        settings_btn = Button(text="Settings", size_hint=(0.2, 1))
        settings_btn.bind(on_press=lambda x: self.on_menu_select(None, 'settings'))
        toolbar.add_widget(settings_btn)

        # Spacer
        toolbar.add_widget(Label(text="Developer App", size_hint=(0.6, 1)))

        return toolbar

    def on_menu_select(self, toolbar, menu_item):
        """Handle menu selection from toolbar"""
        Logger.info(f"Menu selected: {menu_item}")

        if menu_item == 'dashboard':
            self.screen_manager.current = 'dashboard'
        elif menu_item == 'settings':
            self.screen_manager.current = 'settings'
        elif menu_item == 'exit':
            self.exit_app()

    def show_dashboard(self):
        """Show dashboard screen"""
        self.screen_manager.current = 'dashboard'
        # Refresh data when returning to dashboard
        if hasattr(self.dashboard_widget, 'refresh_data'):
            self.dashboard_widget.refresh_data()

    def show_maincode_crud(self):
        """Show MainCode CRUD screen"""
        self.screen_manager.current = 'maincode_crud'
        # Refresh data when entering CRUD screen
        if hasattr(self.maincode_crud_widget, 'refresh_data'):
            self.maincode_crud_widget.refresh_data()

    def show_companyinfo_crud(self):
        """Show CompanyInfo CRUD screen"""
        self.screen_manager.current = 'companyinfo_crud'
        # Refresh data when entering CRUD screen
        if hasattr(self.companyinfo_crud_widget, 'refresh_data'):
            self.companyinfo_crud_widget.refresh_data()

    def exit_app(self):
        """Exit the application"""
        from kivy.app import App
        App.get_running_app().stop()
