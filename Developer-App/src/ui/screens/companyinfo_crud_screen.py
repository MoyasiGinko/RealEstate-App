"""
CompanyInfo CRUD Screen
Provides full Create, Read, Update, Delete operations for CompanyInfo table
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.logger import Logger
from src.api.models import CompanyInfo


class CompanyInfoCRUDScreen(BoxLayout):
    """CompanyInfo CRUD operations screen"""

    def __init__(self, api_manager=None, main_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.api_manager = api_manager
        self.main_screen = main_screen
        self.company_data = []
        self.selected_company = None
        self.build_ui()
        self.refresh_data()

    def build_ui(self):
        """Build the CRUD interface"""
        # Header with back button
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)

        back_btn = Button(text='← Back to Dashboard', size_hint_x=None, width=200)
        back_btn.bind(on_press=self.go_back)
        header_layout.add_widget(back_btn)

        title = Label(text='CompanyInfo CRUD Operations', font_size=24, bold=True)
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
        title = Label(text='Company Records', font_size=18, size_hint_y=None, height=40, bold=True)
        panel.add_widget(title)

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
        title = Label(text='Edit/Create Company', font_size=18, size_hint_y=None, height=40, bold=True)
        panel.add_widget(title)

        # Form fields in scroll view
        form_scroll = ScrollView(size_hint=(1, 0.7))
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=500)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Create input fields
        self.inputs = {}
        fields = [
            ('company_code', 'Company Code', 'e.g., E901'),
            ('company_name', 'Company Name', 'e.g., Best Real Estate'),
            ('city_code', 'City Code', 'e.g., 02001'),
            ('company_address', 'Address', 'e.g., 123 King St.'),
            ('phone_number', 'Phone Number', 'e.g., 07901234567'),
            ('username', 'Username', 'e.g., admin'),
            ('password', 'Password', 'e.g., pass1234'),
            ('subscription_code', 'Subscription Code', 'e.g., 1'),
            ('subscription_duration', 'Duration (months)', 'e.g., 12'),
            ('descriptions', 'Description', 'Optional notes')
        ]

        for field_key, field_label, hint in fields:
            form_layout.add_widget(Label(text=f'{field_label}:'))
            input_widget = TextInput(
                multiline=(field_key == 'descriptions'),
                hint_text=hint,
                size_hint_y=None,
                height=80 if field_key == 'descriptions' else 40
            )
            self.inputs[field_key] = input_widget
            form_layout.add_widget(input_widget)

        form_scroll.add_widget(form_layout)
        panel.add_widget(form_scroll)

        # Action buttons
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=120)

        self.create_btn = Button(text='Create New', background_color=(0.2, 0.8, 0.2, 1))
        self.create_btn.bind(on_press=self.create_company)
        btn_layout.add_widget(self.create_btn)

        self.update_btn = Button(text='Update Selected', background_color=(0.2, 0.2, 0.8, 1))
        self.update_btn.bind(on_press=self.update_company)
        self.update_btn.disabled = True
        btn_layout.add_widget(self.update_btn)

        self.delete_btn = Button(text='Delete Selected', background_color=(0.8, 0.2, 0.2, 1))
        self.delete_btn.bind(on_press=self.delete_company)
        self.delete_btn.disabled = True
        btn_layout.add_widget(self.delete_btn)

        clear_btn = Button(text='Clear Form', background_color=(0.5, 0.5, 0.5, 1))
        clear_btn.bind(on_press=self.clear_form)
        btn_layout.add_widget(clear_btn)

        panel.add_widget(btn_layout)

        # Status area
        self.status_label = Label(
            text='Ready to create new Company record',
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
            response = self.api_manager.company.get_all_companies()
            if response.success:
                self.company_data = response.data
                self.display_data()
                self.status_label.text = f"Loaded {len(self.company_data)} Company records"
                Logger.info(f"Loaded {len(self.company_data)} Company records")
            else:
                self.status_label.text = f"Error loading data: {response.error}"
                Logger.error(f"Failed to load Company data: {response.error}")
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"
            Logger.error(f"Error refreshing Company data: {str(e)}")

    def display_data(self):
        """Display data in the list"""
        self.data_layout.clear_widgets()

        if not self.company_data:
            no_data_label = Label(
                text='No company records found',
                size_hint_y=None,
                height=40,
                italic=True
            )
            self.data_layout.add_widget(no_data_label)
            return

        for company in self.company_data:
            self.create_data_row(company)

    def create_data_row(self, company):
        """Create a row for displaying company data"""
        row_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100, spacing=5)

        # Main info row
        main_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

        # Company info
        info_text = f"Code: {getattr(company, 'company_code', 'N/A')} | "
        info_text += f"Name: {getattr(company, 'company_name', 'N/A')}"

        info_label = Label(
            text=info_text,
            text_size=(None, None),
            halign='left',
            valign='middle',
            bold=True
        )
        main_row.add_widget(info_label)

        # Select button
        select_btn = Button(text='Select', size_hint_x=None, width=80)
        select_btn.bind(on_press=lambda x, comp=company: self.select_company(comp))
        main_row.add_widget(select_btn)

        row_layout.add_widget(main_row)

        # Details row
        details_text = f"Phone: {getattr(company, 'phone_number', 'N/A')} | "
        details_text += f"City: {getattr(company, 'city_code', 'N/A')} | "
        details_text += f"User: {getattr(company, 'username', 'N/A')}"

        details_label = Label(
            text=details_text,
            text_size=(None, None),
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=30,
            color=(0.7, 0.7, 0.7, 1)
        )
        row_layout.add_widget(details_label)

        # Address row
        address_text = f"Address: {getattr(company, 'company_address', 'N/A')}"
        address_label = Label(
            text=address_text,
            text_size=(None, None),
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=30,
            color=(0.7, 0.7, 0.7, 1)
        )
        row_layout.add_widget(address_label)

        self.data_layout.add_widget(row_layout)

    def select_company(self, company):
        """Select a company for editing"""
        self.selected_company = company

        # Populate form
        self.inputs['company_code'].text = getattr(company, 'company_code', '')
        self.inputs['company_name'].text = getattr(company, 'company_name', '')
        self.inputs['city_code'].text = getattr(company, 'city_code', '')
        self.inputs['company_address'].text = getattr(company, 'company_address', '')
        self.inputs['phone_number'].text = getattr(company, 'phone_number', '')
        self.inputs['username'].text = getattr(company, 'username', '')
        self.inputs['password'].text = getattr(company, 'password', '')
        self.inputs['subscription_code'].text = getattr(company, 'subscription_code', '')
        self.inputs['subscription_duration'].text = getattr(company, 'subscription_duration', '')
        self.inputs['descriptions'].text = getattr(company, 'descriptions', '')

        # Enable update/delete buttons
        self.update_btn.disabled = False
        self.delete_btn.disabled = False

        self.status_label.text = f"Selected: {getattr(company, 'company_name', 'N/A')}"

    def create_company(self, button):
        """Create new company"""
        try:
            if not self.validate_form():
                return

            company = CompanyInfo(
                company_code=self.inputs['company_code'].text,
                company_name=self.inputs['company_name'].text or None,
                city_code=self.inputs['city_code'].text or None,
                company_address=self.inputs['company_address'].text or None,
                phone_number=self.inputs['phone_number'].text or None,
                username=self.inputs['username'].text or None,
                password=self.inputs['password'].text or None,
                subscription_code=self.inputs['subscription_code'].text or None,
                subscription_duration=self.inputs['subscription_duration'].text or None,
                descriptions=self.inputs['descriptions'].text or None
            )

            response = self.api_manager.company.create_company(company)
            if response.success:
                self.status_label.text = "Company created successfully!"
                self.clear_form()
                self.refresh_data()
            else:
                self.status_label.text = f"Error creating Company: {response.error}"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

    def update_company(self, button):
        """Update selected company"""
        if not self.selected_company:
            self.status_label.text = "No Company selected"
            return

        try:
            if not self.validate_form():
                return

            # Update the selected company object
            self.selected_company.company_code = self.inputs['company_code'].text
            self.selected_company.company_name = self.inputs['company_name'].text or None
            self.selected_company.city_code = self.inputs['city_code'].text or None
            self.selected_company.company_address = self.inputs['company_address'].text or None
            self.selected_company.phone_number = self.inputs['phone_number'].text or None
            self.selected_company.username = self.inputs['username'].text or None
            self.selected_company.password = self.inputs['password'].text or None
            self.selected_company.subscription_code = self.inputs['subscription_code'].text or None
            self.selected_company.subscription_duration = self.inputs['subscription_duration'].text or None
            self.selected_company.descriptions = self.inputs['descriptions'].text or None

            response = self.api_manager.company.update_company(
                getattr(self.selected_company, 'company_code', ''),
                self.selected_company
            )

            if response.success:
                self.status_label.text = "Company updated successfully!"
                self.clear_form()
                self.refresh_data()
            else:
                self.status_label.text = f"Error updating Company: {response.error}"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

    def delete_company(self, button):
        """Delete selected company"""
        if not self.selected_company:
            self.status_label.text = "No Company selected"
            return

        try:
            company_code = getattr(self.selected_company, 'company_code', '')
            response = self.api_manager.company.delete_company(company_code)

            if response.success:
                self.status_label.text = "Company deleted successfully!"
                self.clear_form()
                self.refresh_data()
            else:
                self.status_label.text = f"Error deleting Company: {response.error}"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

    def validate_form(self):
        """Validate form inputs"""
        if not self.inputs['company_code'].text.strip():
            self.status_label.text = "Please enter a company code"
            return False

        if not self.inputs['company_name'].text.strip():
            self.status_label.text = "Please enter a company name"
            return False

        return True

    def clear_form(self, button=None):
        """Clear the form"""
        for input_widget in self.inputs.values():
            input_widget.text = ''

        self.selected_company = None
        self.update_btn.disabled = True
        self.delete_btn.disabled = True
        self.status_label.text = 'Ready to create new Company record'

    def go_back(self, button):
        """Go back to dashboard"""
        if self.main_screen:
            self.main_screen.show_dashboard()
