"""
MainCode CRUD Screen
Provides full Create, Read, Update, Delete operations for MainCode table
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.logger import Logger
from src.api.models import MainCode


class MainCodeCRUDScreen(BoxLayout):
    """MainCode CRUD operations screen"""

    def __init__(self, api_manager=None, main_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.api_manager = api_manager
        self.main_screen = main_screen
        self.maincode_data = []
        self.selected_maincode = None
        self.build_ui()
        self.refresh_data()

    def build_ui(self):
        """Build the CRUD interface"""
        # Header with back button
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)

        back_btn = Button(text='← Back to Dashboard', size_hint_x=None, width=200)
        back_btn.bind(on_press=self.go_back)
        header_layout.add_widget(back_btn)

        title = Label(text='MainCode CRUD Operations', font_size=24, bold=True)
        header_layout.add_widget(title)

        refresh_btn = Button(text='🔄 Refresh', size_hint_x=None, width=100)
        refresh_btn.bind(on_press=lambda x: self.refresh_data())
        header_layout.add_widget(refresh_btn)

        self.add_widget(header_layout)

        # Main content area
        content_layout = BoxLayout(orientation='horizontal', spacing=20)

        # Left panel - Data list
        left_panel = self.create_data_panel()
        content_layout.add_widget(left_panel)

        # Right panel - Form
        right_panel = self.create_form_panel()
        content_layout.add_widget(right_panel)

        self.add_widget(content_layout)

    def create_data_panel(self):
        """Create the data list panel"""
        panel = BoxLayout(orientation='vertical', size_hint_x=0.6, spacing=10)

        # Panel title
        title = Label(text='MainCode Records', font_size=18, size_hint_y=None, height=40, bold=True)
        panel.add_widget(title)

        # Filter section
        filter_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

        filter_layout.add_widget(Label(text='Filter by Type:', size_hint_x=None, width=100))
        self.type_filter = Spinner(
            text='All Types',
            values=['All Types', '01 - Countries', '02 - Cities', '03 - Property Types',
                   '04 - Building Types', '05 - Unit Measures', '06 - Offer Types'],
            size_hint_x=None,
            width=200
        )
        self.type_filter.bind(text=self.on_filter_change)
        filter_layout.add_widget(self.type_filter)

        panel.add_widget(filter_layout)

        # Data display area
        scroll = ScrollView()
        self.data_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.data_layout.bind(minimum_height=self.data_layout.setter('height'))
        scroll.add_widget(self.data_layout)
        panel.add_widget(scroll)

        return panel

    def create_form_panel(self):
        """Create the form panel"""
        panel = BoxLayout(orientation='vertical', size_hint_x=0.4, spacing=10)

        # Panel title
        title = Label(text='Edit/Create MainCode', font_size=18, size_hint_y=None, height=40, bold=True)
        panel.add_widget(title)

        # Form fields
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=200)

        form_layout.add_widget(Label(text='Record Type:'))
        self.record_type_input = Spinner(
            text='Select Type',
            values=['01', '02', '03', '04', '05', '06'],
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.record_type_input)

        form_layout.add_widget(Label(text='Code:'))
        self.code_input = TextInput(multiline=False, size_hint_y=None, height=40)
        form_layout.add_widget(self.code_input)

        form_layout.add_widget(Label(text='Name:'))
        self.name_input = TextInput(multiline=False, size_hint_y=None, height=40)
        form_layout.add_widget(self.name_input)

        form_layout.add_widget(Label(text='Description:'))
        self.description_input = TextInput(multiline=True, size_hint_y=None, height=80)
        form_layout.add_widget(self.description_input)

        panel.add_widget(form_layout)

        # Action buttons
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=120)

        self.create_btn = Button(text='Create New', background_color=(0.2, 0.8, 0.2, 1))
        self.create_btn.bind(on_press=self.create_maincode)
        btn_layout.add_widget(self.create_btn)

        self.update_btn = Button(text='Update Selected', background_color=(0.2, 0.2, 0.8, 1))
        self.update_btn.bind(on_press=self.update_maincode)
        self.update_btn.disabled = True
        btn_layout.add_widget(self.update_btn)

        self.delete_btn = Button(text='Delete Selected', background_color=(0.8, 0.2, 0.2, 1))
        self.delete_btn.bind(on_press=self.delete_maincode)
        self.delete_btn.disabled = True
        btn_layout.add_widget(self.delete_btn)

        clear_btn = Button(text='Clear Form', background_color=(0.5, 0.5, 0.5, 1))
        clear_btn.bind(on_press=self.clear_form)
        btn_layout.add_widget(clear_btn)

        panel.add_widget(btn_layout)

        # Status area
        self.status_label = Label(
            text='Ready to create new MainCode record',
            size_hint_y=None,
            height=60,
            text_size=(None, None),
            halign='center'
        )
        panel.add_widget(self.status_label)

        return panel

    def refresh_data(self):
        """Refresh data from database"""
        if not self.api_manager or not self.api_manager.is_initialized():
            self.status_label.text = "Database not connected"
            return

        try:
            response = self.api_manager.maincode.get_all_main_codes()
            if response.success:
                self.maincode_data = response.data
                self.display_data()
                self.status_label.text = f"Loaded {len(self.maincode_data)} MainCode records"
                Logger.info(f"Loaded {len(self.maincode_data)} MainCode records")
            else:
                self.status_label.text = f"Error loading data: {response.error}"
                Logger.error(f"Failed to load MainCode data: {response.error}")
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"
            Logger.error(f"Error refreshing MainCode data: {str(e)}")

    def display_data(self):
        """Display data in the list"""
        self.data_layout.clear_widgets()

        # Filter data based on selected type
        filtered_data = self.maincode_data
        if self.type_filter.text != 'All Types':
            filter_type = self.type_filter.text.split(' - ')[0]
            filtered_data = [mc for mc in self.maincode_data
                           if getattr(mc, 'record_type', '') == filter_type]

        if not filtered_data:
            no_data_label = Label(
                text='No records found',
                size_hint_y=None,
                height=40,
                italic=True
            )
            self.data_layout.add_widget(no_data_label)
            return

        for maincode in filtered_data:
            self.create_data_row(maincode)

    def create_data_row(self, maincode):
        """Create a row for displaying maincode data"""
        row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

        # Data display
        info_text = f"Type: {getattr(maincode, 'record_type', 'N/A')} | "
        info_text += f"Code: {getattr(maincode, 'code', 'N/A')} | "
        info_text += f"Name: {getattr(maincode, 'name', 'N/A')}"

        info_label = Label(
            text=info_text,
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        row_layout.add_widget(info_label)

        # Select button
        select_btn = Button(text='Select', size_hint_x=None, width=80)
        select_btn.bind(on_press=lambda x, mc=maincode: self.select_maincode(mc))
        row_layout.add_widget(select_btn)

        self.data_layout.add_widget(row_layout)

    def select_maincode(self, maincode):
        """Select a maincode for editing"""
        self.selected_maincode = maincode

        # Populate form
        record_type = getattr(maincode, 'record_type', '')
        if record_type and record_type in self.record_type_input.values:
            self.record_type_input.text = record_type
        else:
            self.record_type_input.text = 'Select Type'

        self.code_input.text = getattr(maincode, 'code', '')
        self.name_input.text = getattr(maincode, 'name', '')
        self.description_input.text = getattr(maincode, 'description', '') or ''        # Enable update/delete buttons
        self.update_btn.disabled = False
        self.delete_btn.disabled = False

        self.status_label.text = f"Selected: {getattr(maincode, 'name', 'N/A')}"

        def create_maincode(self, button):
        """Create new maincode"""
        try:
            if not self.validate_form():
                return

            # Create dictionary data for API call
            maincode_data = {
                'record_type': self.record_type_input.text,
                'code': self.code_input.text,
                'name': self.name_input.text,
                'description': self.description_input.text or None
            }

            response = self.api_manager.maincode.create_main_code(maincode_data)
            if response.success:
                self.status_label.text = "MainCode created successfully!"
                self.clear_form()
                self.refresh_data()
            else:
                self.status_label.text = f"Error creating MainCode: {response.error}"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

    def update_maincode(self, button):
        """Update selected maincode"""
        if not self.selected_maincode:
            self.status_label.text = "No MainCode selected"
            return

        try:
            if not self.validate_form():
                return

            # Create dictionary with updated data for API call
            update_data = {
                'record_type': self.record_type_input.text,
                'code': self.code_input.text,
                'name': self.name_input.text,
                'description': self.description_input.text or None
            }

            # Get original code for the update operation
            original_code = getattr(self.selected_maincode, 'code', '')
            original_record_type = getattr(self.selected_maincode, 'record_type', '')

            response = self.api_manager.maincode.update_main_code(
                original_code,
                update_data,
                original_record_type
            )

            if response.success:
                self.status_label.text = "MainCode updated successfully!"
                self.clear_form()
                self.refresh_data()
            else:
                self.status_label.text = f"Error updating MainCode: {response.error}"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

    def delete_maincode(self, button):
        """Delete selected maincode"""
        if not self.selected_maincode:
            self.status_label.text = "No MainCode selected"
            return

        try:
            code = getattr(self.selected_maincode, 'code', '')
            response = self.api_manager.maincode.delete_main_code(code)

            if response.success:
                self.status_label.text = "MainCode deleted successfully!"
                self.clear_form()
                self.refresh_data()
            else:
                self.status_label.text = f"Error deleting MainCode: {response.error}"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

    def validate_form(self):
        """Validate form inputs"""
        if not self.record_type_input.text or self.record_type_input.text == 'Select Type':
            self.status_label.text = "Please select a record type"
            return False

        if not self.code_input.text.strip():
            self.status_label.text = "Please enter a code"
            return False

        if not self.name_input.text.strip():
            self.status_label.text = "Please enter a name"
            return False

        return True

    def clear_form(self, button=None):
        """Clear the form"""
        self.record_type_input.text = 'Select Type'
        self.code_input.text = ''
        self.name_input.text = ''
        self.description_input.text = ''
        self.selected_maincode = None
        self.update_btn.disabled = True
        self.delete_btn.disabled = True
        self.status_label.text = 'Ready to create new MainCode record'

    def on_filter_change(self, spinner, text):
        """Handle filter change"""
        self.display_data()

    def go_back(self, button):
        """Go back to dashboard"""
        if self.main_screen:
            self.main_screen.show_dashboard()
