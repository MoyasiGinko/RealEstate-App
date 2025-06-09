"""
Dashboard Screen - Main working area with API integration
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.logger import Logger
from kivy.clock import Clock


class DashboardScreen(BoxLayout):
    """Dashboard screen with main application features"""

    def __init__(self, api_manager=None, main_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.api_manager = api_manager
        self.main_screen = main_screen
        self.company_data = []
        self.maincode_data = []
        self.build_ui()
        self.refresh_data()

    def build_ui(self):
        """Build dashboard UI"""
        # Header
        header = Label(
            text='Developer Dashboard',
            font_size=24,
            size_hint_y=None,
            height=60,
            bold=True
        )
        self.add_widget(header)

        # Main content area
        content_layout = BoxLayout(orientation='horizontal', spacing=20)

        # Left panel - Quick actions
        left_panel = self.create_left_panel()
        content_layout.add_widget(left_panel)

        # Center panel - Main workspace
        center_panel = self.create_center_panel()
        content_layout.add_widget(center_panel)

        # Right panel - Information
        right_panel = self.create_right_panel()
        content_layout.add_widget(right_panel)

        self.add_widget(content_layout)

    def create_left_panel(self):
        """Create left panel with quick actions"""
        panel = BoxLayout(
            orientation='vertical',
            size_hint_x=0.25,
            spacing=10
        )

        # Panel title
        title = Label(
            text='Quick Actions',
            font_size=16,
            size_hint_y=None,
            height=40,
            bold=True
        )
        panel.add_widget(title)        # Action buttons
        actions = [
            ('MainCode CRUD', self.on_maincode_crud),
            ('CompanyInfo CRUD', self.on_company_crud),
            ('Database Tools', self.on_database_tools),
            ('Export Data', self.on_export_data),
            ('Import Data', self.on_import_data)
        ]

        for action_text, callback in actions:
            btn = Button(
                text=action_text,
                size_hint_y=None,
                height=40
            )
            btn.bind(on_press=callback)
            panel.add_widget(btn)

        # Spacer
        panel.add_widget(Label())

        return panel

    def create_center_panel(self):
        """Create center panel with main workspace"""
        panel = BoxLayout(
            orientation='vertical',
            size_hint_x=0.5,
            spacing=10
        )

        # Panel title
        title = Label(
            text='Workspace',
            font_size=16,
            size_hint_y=None,
            height=40,
            bold=True
        )
        panel.add_widget(title)

        # Text area for content
        scroll = ScrollView()
        self.text_area = TextInput(
            text='Loading...',
            multiline=True,
            font_size=14
        )
        scroll.add_widget(self.text_area)
        panel.add_widget(scroll)

        return panel

    def create_right_panel(self):
        """Create right panel with information"""
        panel = BoxLayout(
            orientation='vertical',
            size_hint_x=0.25,
            spacing=10
        )

        # Panel title
        title = Label(
            text='Information',
            font_size=16,
            size_hint_y=None,
            height=40,
            bold=True
        )
        panel.add_widget(title)

        # Information grid
        info_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        info_layout.bind(minimum_height=info_layout.setter('height'))

        self.info_labels = {}
        info_items = [
            ('status', 'Status: Connecting...'),
            ('projects', 'Projects: 0'),
            ('companies', 'Companies: 0'),
            ('maincodes', 'Main Codes: 0'),
            ('last_update', 'Last Update: Never')
        ]

        for key, initial_text in info_items:
            label = Label(
                text=initial_text,
                size_hint_y=None,
                height=30,
                text_size=(None, None),
                halign='left'
            )
            self.info_labels[key] = label
            info_layout.add_widget(label)

        scroll = ScrollView()
        scroll.add_widget(info_layout)
        panel.add_widget(scroll)

        return panel

    def refresh_data(self):
        """Refresh data from database"""
        if not self.api_manager or not self.api_manager.is_initialized():
            self.update_info_label('status', 'Status: No Database Connection')
            self.text_area.text = "Database not connected.\n\nPlease check your database settings."
            return

        try:            # Get company data
            company_response = self.api_manager.company.get_all_companies()
            if company_response.success:
                self.company_data = company_response.data
                Logger.info(f"Loaded {len(self.company_data)} company records")
                self.update_info_label('companies', f'Companies: {len(self.company_data)}')
            else:
                Logger.error(f"Failed to load company data: {company_response.error}")
                self.update_info_label('companies', 'Companies: Error')

            # Get maincode data
            maincode_response = self.api_manager.maincode.get_all_main_codes()
            if maincode_response.success:
                self.maincode_data = maincode_response.data
                Logger.info(f"Loaded {len(self.maincode_data)} maincode records")
                self.update_info_label('maincodes', f'Main Codes: {len(self.maincode_data)}')
            else:
                Logger.error(f"Failed to load maincode data: {maincode_response.error}")
                self.update_info_label('maincodes', 'Main Codes: Error')

            # Update UI with fresh data
            self.update_data_display()
            self.update_info_label('status', 'Status: Connected')
            self.update_info_label('last_update', f'Last Update: {Clock.get_time():.0f}s')

        except Exception as e:
            Logger.error(f"Error refreshing data: {str(e)}")
            self.update_info_label('status', 'Status: Error')
            self.text_area.text = f"Error loading data: {str(e)}"

    def update_info_label(self, key, text):
        """Update an info label"""
        if key in self.info_labels:
            self.info_labels[key].text = text

    def update_data_display(self):
        """Update the text area with current data"""
        if not self.api_manager or not self.api_manager.is_initialized():
            self.text_area.text = "Database not connected.\n\nPlease check your database settings."
            return

        content = "=== Developer App Dashboard ===\n\n"
        content += f"📊 Data Summary:\n"
        content += f"• Company Records: {len(self.company_data)}\n"
        content += f"• Main Code Records: {len(self.maincode_data)}\n\n"

        if self.company_data:
            content += "🏢 Recent Company Records:\n"
            for i, company in enumerate(self.company_data[:5]):  # Show first 5
                content += f"  {i+1}. {getattr(company, 'company_name', 'N/A')} ({getattr(company, 'company_code', 'N/A')})\n"
            if len(self.company_data) > 5:
                content += f"  ... and {len(self.company_data) - 5} more\n"
            content += "\n"

        if self.maincode_data:
            content += "🔧 Recent Main Code Records:\n"
            for i, maincode in enumerate(self.maincode_data[:5]):  # Show first 5
                content += f"  {i+1}. {getattr(maincode, 'name', 'N/A')} ({getattr(maincode, 'code', 'N/A')})\n"
            if len(self.maincode_data) > 5:
                content += f"  ... and {len(self.maincode_data) - 5} more\n"
            content += "\n"

        content += "🔧 Available Actions:\n"
        content += "• Use 'Database Tools' to manage records\n"
        content += "• Use 'Export Data' to backup your data\n"
        content += "• Use 'Import Data' to restore data\n"

        self.text_area.text = content

    def on_maincode_crud(self, button):
        """Handle MainCode CRUD operations"""
        Logger.info("MainCode CRUD requested")
        if self.api_manager and self.api_manager.is_initialized():
            if self.main_screen:
                self.main_screen.show_maincode_crud()
            else:
                self.text_area.text = "Navigation not available"
        else:
            self.text_area.text = "Database not connected. Please check settings."

    def on_company_crud(self, button):
        """Handle CompanyInfo CRUD operations"""
        Logger.info("CompanyInfo CRUD requested")
        if self.api_manager and self.api_manager.is_initialized():
            if self.main_screen:
                self.main_screen.show_companyinfo_crud()
            else:
                self.text_area.text = "Navigation not available"
        else:
            self.text_area.text = "Database not connected. Please check settings."

    def on_database_tools(self, button):
        """Handle database tools action"""
        Logger.info("Database tools requested")
        if self.api_manager and self.api_manager.is_initialized():
            self.show_database_dialog()
        else:
            self.text_area.text = "Database not connected. Please check settings."

    def on_export_data(self, button):
        """Handle export data action"""
        Logger.info("Export data requested")
        if self.api_manager and self.api_manager.is_initialized():
            self.export_data()
        else:
            self.text_area.text = "Database not connected. Cannot export data."    def on_import_data(self, button):
        """Handle import data action"""
        Logger.info("Import data requested")
        if self.api_manager and self.api_manager.is_initialized():
            self.show_import_dialog()
        else:
            self.text_area.text = "Database not connected. Cannot import data."

    def show_database_dialog(self):
        """Show database management dialog"""
        self.text_area.text = "Database Management Tools:\n\n"
        self.text_area.text += "Available Actions:\n"
        self.text_area.text += "• Manage Companies - Navigate to CompanyInfo CRUD\n"
        self.text_area.text += "• Manage Main Codes - Navigate to MainCode CRUD\n"
        self.text_area.text += "• Test Connection - Verify database connectivity\n"
        self.text_area.text += "• Refresh Data - Reload all data from database\n\n"
        self.text_area.text += "Use the Quick Actions panel on the left to access these features."

    def show_company_management(self):
        """Show company management interface"""
        self.text_area.text = "Company Management:\n\n"
        if self.company_data:
            for i, company in enumerate(self.company_data):
                # Fix: Use attribute access instead of .get() method
                company_name = getattr(company, 'company_name', 'N/A')
                company_code = getattr(company, 'company_code', 'N/A')
                self.text_area.text += f"{i+1}. {company_name} - {company_code}\n"
        else:
            self.text_area.text += "No company records found."

    def show_maincode_management(self):
        """Show maincode management interface"""
        self.text_area.text = "Main Code Management:\n\n"
        if self.maincode_data:
            for i, maincode in enumerate(self.maincode_data):
                # Fix: Use attribute access instead of .get() method
                maincode_name = getattr(maincode, 'name', 'N/A')
                maincode_code = getattr(maincode, 'code', 'N/A')
                self.text_area.text += f"{i+1}. {maincode_name} - {maincode_code}\n"
        else:
            self.text_area.text += "No main code records found."

    def test_database_connection(self):
        """Test database connection"""
        if not self.api_manager:
            self.text_area.text = "API Manager not available"
            return

        test_result = self.api_manager.test_connection()
        if test_result.success:
            self.text_area.text = "✅ Database connection successful!"
            self.update_info_label('status', 'Status: Connected')
        else:
            self.text_area.text = f"❌ Database connection failed: {test_result.error}"
            self.update_info_label('status', 'Status: Connection Failed')

    def export_data(self):
        """Export data to file"""
        try:
            if not self.api_manager or not self.api_manager.is_initialized():
                self.text_area.text = "Database not connected"
                return

            export_data = {
                'companies': self.company_data,
                'maincodes': self.maincode_data,
                'export_timestamp': Clock.get_time()
            }            # In a real app, you'd save this to a file
            self.text_area.text = f"Export completed!\n\nData summary:\n• Companies: {len(self.company_data)}\n• Main Codes: {len(self.maincode_data)}\n\nIn a production app, this data would be saved to a file."

        except Exception as e:
            self.text_area.text = f"Export failed: {str(e)}"

    def show_import_dialog(self):
        """Show import data dialog"""
        self.text_area.text = "Import functionality will be implemented here.\n\nThis would allow you to:\n• Select import file\n• Preview data\n• Choose import options\n• Import data to database\n• Validate data integrity"

    def show_company_management(self):
        """Show company management interface"""
        self.text_area.text = "Company Management:\n\n"
        if self.company_data:
            for i, company in enumerate(self.company_data):
                # Fix: Use attribute access instead of .get() method
                company_name = getattr(company, 'company_name', 'N/A')
                company_code = getattr(company, 'company_code', 'N/A')
                self.text_area.text += f"{i+1}. {company_name} - {company_code}\n"
        else:
            self.text_area.text += "No company records found."

    def show_maincode_management(self):
        """Show maincode management interface"""
        self.text_area.text = "Main Code Management:\n\n"
        if self.maincode_data:
            for i, maincode in enumerate(self.maincode_data):
                # Fix: Use attribute access instead of .get() method
                maincode_name = getattr(maincode, 'name', 'N/A')
                maincode_code = getattr(maincode, 'code', 'N/A')
                self.text_area.text += f"{i+1}. {maincode_name} - {maincode_code}\n"
        else:
            self.text_area.text += "No main code records found."

    def test_database_connection(self):
        """Test database connection"""
        if not self.api_manager:
            self.text_area.text = "API Manager not available"
            return

        test_result = self.api_manager.test_connection()
        if test_result.success:
            self.text_area.text = "✅ Database connection successful!"
            self.update_info_label('status', 'Status: Connected')
        else:
            self.text_area.text = f"❌ Database connection failed: {test_result.error}"
            self.update_info_label('status', 'Status: Connection Failed')
