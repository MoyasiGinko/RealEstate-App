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
from kivy.uix.spinner import Spinner
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

        # Company Code with auto-generation
        form_layout.add_widget(Label(text='Company Code:'))
        company_code_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.inputs['company_code'] = TextInput(
            hint_text='e.g., E901',
            size_hint_y=None,
            height=40
        )
        company_code_layout.add_widget(self.inputs['company_code'])

        auto_company_btn = Button(
            text='Auto',
            size_hint_x=None,
            width=60,
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        auto_company_btn.bind(on_press=self.generate_company_code)
        company_code_layout.add_widget(auto_company_btn)
        form_layout.add_widget(company_code_layout)

        # Company Name
        form_layout.add_widget(Label(text='Company Name:'))
        self.inputs['company_name'] = TextInput(
            hint_text='e.g., Best Real Estate',
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['company_name'])

        # City Code with dropdown
        form_layout.add_widget(Label(text='City:'))
        self.inputs['city_code'] = Spinner(
            text='Select City',
            values=['Select City'],
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['city_code'])

        # Company Address
        form_layout.add_widget(Label(text='Address:'))
        self.inputs['company_address'] = TextInput(
            hint_text='e.g., 123 King St.',
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['company_address'])

        # Phone Number
        form_layout.add_widget(Label(text='Phone Number:'))
        self.inputs['phone_number'] = TextInput(
            hint_text='e.g., 07901234567',
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['phone_number'])

        # Username
        form_layout.add_widget(Label(text='Username:'))
        self.inputs['username'] = TextInput(
            hint_text='e.g., admin',
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['username'])

        # Password
        form_layout.add_widget(Label(text='Password:'))
        self.inputs['password'] = TextInput(
            hint_text='e.g., pass1234',
            password=True,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['password'])        # Subscription Code dropdown
        form_layout.add_widget(Label(text='Subscription Type:'))
        self.inputs['subscription_code'] = Spinner(
            text='Select Subscription Type',
            values=[
                'Select Subscription Type',
                '1 - Trail for 5 days',
                '2 - Active',
                '3 - Not active'
            ],
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['subscription_code'])

        # Subscription Duration dropdown
        form_layout.add_widget(Label(text='Subscription Duration:'))
        self.inputs['subscription_duration'] = Spinner(
            text='Select Duration',
            values=[
                'Select Duration',
                '1 - 1 month',
                '2 - 3 months',
                '3 - 6 months',
                '4 - 12 months'
            ],
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['subscription_duration'])

        # Descriptions
        form_layout.add_widget(Label(text='Description:'))
        self.inputs['descriptions'] = TextInput(
            hint_text='Optional notes',
            multiline=True,
            size_hint_y=None,
            height=80
        )
        form_layout.add_widget(self.inputs['descriptions'])

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
            # Load company data
            response = self.api_manager.company.get_all_companies()
            if response.success:
                self.company_data = response.data
                self.display_data()
                self.status_label.text = f"Loaded {len(self.company_data)} Company records"
                Logger.info(f"Loaded {len(self.company_data)} Company records")
            else:
                self.status_label.text = f"Error loading data: {response.error}"
                Logger.error(f"Failed to load Company data: {response.error}")

            # Load cities for dropdown
            self.load_cities()

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
        self.inputs['company_code'].text = getattr(company, 'company_code', '') or ''
        self.inputs['company_name'].text = getattr(company, 'company_name', '') or ''

        # Handle city code - find matching display format in dropdown
        city_code = getattr(company, 'city_code', '')
        if city_code:
            # Find the matching city display format in the dropdown values
            city_found = False
            for city_option in self.inputs['city_code'].values:
                if city_option.startswith(city_code + ' - '):
                    self.inputs['city_code'].text = city_option
                    city_found = True
                    break
            if not city_found:
                self.inputs['city_code'].text = city_code  # Fallback to just the code        else:
            self.inputs['city_code'].text = 'Select City'

        self.inputs['company_address'].text = getattr(company, 'company_address', '') or ''
        self.inputs['phone_number'].text = getattr(company, 'phone_number', '') or ''
        self.inputs['username'].text = getattr(company, 'username', '') or ''
        self.inputs['password'].text = getattr(company, 'password', '') or ''

        # Handle subscription code dropdown selection
        subscription_code = getattr(company, 'subscription_code', '') or ''
        if subscription_code:
            subscription_mapping = {
                '1': '1 - Trail for 5 days',
                '2': '2 - Active',
                '3': '3 - Not active'
            }
            self.inputs['subscription_code'].text = subscription_mapping.get(subscription_code, 'Select Subscription Type')
        else:
            self.inputs['subscription_code'].text = 'Select Subscription Type'

        # Handle subscription duration dropdown selection
        duration_code = getattr(company, 'subscription_duration', '') or ''
        if duration_code:
            duration_mapping = {
                '1': '1 - 1 month',
                '2': '2 - 3 months',
                '3': '3 - 6 months',
                '4': '4 - 12 months'
            }
            self.inputs['subscription_duration'].text = duration_mapping.get(duration_code, 'Select Duration')
        else:
            self.inputs['subscription_duration'].text = 'Select Duration'

        self.inputs['descriptions'].text = getattr(company, 'descriptions', '') or ''

        # Enable update/delete buttons
        self.update_btn.disabled = False
        self.delete_btn.disabled = False

        self.status_label.text = f"Selected: {getattr(company, 'company_name', 'N/A')}"

    def create_company(self, button):
        """Create new company"""
        try:
            if not self.validate_form():
                return

            # Extract city code from dropdown selection (format: "00101 - Baghdad" -> "00101")
            city_text = self.inputs['city_code'].text
            city_code = None
            if city_text and city_text != 'Select City' and ' - ' in city_text:
                city_code = city_text.split(' - ')[0]
            elif city_text and city_text != 'Select City':
                city_code = city_text

            # Extract subscription code from dropdown selection (format: "1 - Trail for 5 days" -> "1")
            subscription_text = self.inputs['subscription_code'].text
            subscription_code = None
            if subscription_text and subscription_text != 'Select Subscription Type' and ' - ' in subscription_text:
                subscription_code = subscription_text.split(' - ')[0]
            elif subscription_text and subscription_text != 'Select Subscription Type':
                subscription_code = subscription_text

            # Extract duration code from dropdown selection (format: "1 - 1 month" -> "1")
            duration_text = self.inputs['subscription_duration'].text
            duration_code = None
            if duration_text and duration_text != 'Select Duration' and ' - ' in duration_text:
                duration_code = duration_text.split(' - ')[0]
            elif duration_text and duration_text != 'Select Duration':
                duration_code = duration_text

            # Create dictionary for API call
            company_data = {
                'company_code': self.inputs['company_code'].text,
                'company_name': self.inputs['company_name'].text or None,
                'city_code': city_code,
                'company_address': self.inputs['company_address'].text or None,
                'phone_number': self.inputs['phone_number'].text or None,
                'username': self.inputs['username'].text or None,
                'password': self.inputs['password'].text or None,
                'subscription_code': subscription_code,
                'subscription_duration': duration_code,
                'descriptions': self.inputs['descriptions'].text or None
            }

            response = self.api_manager.company.create_company(company_data)
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
                return            # Extract city code from dropdown selection (format: "00101 - Baghdad" -> "00101")
            city_text = self.inputs['city_code'].text
            city_code = None
            if city_text and city_text != 'Select City' and ' - ' in city_text:
                city_code = city_text.split(' - ')[0]
            elif city_text and city_text != 'Select City':
                city_code = city_text

            # Extract subscription code from dropdown selection (format: "1 - Trail for 5 days" -> "1")
            subscription_text = self.inputs['subscription_code'].text
            subscription_code = None
            if subscription_text and subscription_text != 'Select Subscription Type' and ' - ' in subscription_text:
                subscription_code = subscription_text.split(' - ')[0]
            elif subscription_text and subscription_text != 'Select Subscription Type':
                subscription_code = subscription_text

            # Extract duration code from dropdown selection (format: "1 - 1 month" -> "1")
            duration_text = self.inputs['subscription_duration'].text
            duration_code = None
            if duration_text and duration_text != 'Select Duration' and ' - ' in duration_text:
                duration_code = duration_text.split(' - ')[0]
            elif duration_text and duration_text != 'Select Duration':
                duration_code = duration_text

            # Create update data dictionary
            update_data = {
                'company_name': self.inputs['company_name'].text or None,
                'city_code': city_code,
                'company_address': self.inputs['company_address'].text or None,
                'phone_number': self.inputs['phone_number'].text or None,
                'username': self.inputs['username'].text or None,
                'password': self.inputs['password'].text or None,
                'subscription_code': subscription_code,
                'subscription_duration': duration_code,
                'descriptions': self.inputs['descriptions'].text or None
            }

            response = self.api_manager.company.update_company(
                getattr(self.selected_company, 'company_code', ''),
                update_data
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

        return True    def clear_form(self, button=None):
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

    def generate_company_code(self, button):
        """Generate next available company code"""
        try:
            if self.api_manager and self.api_manager.company:
                response = self.api_manager.company.get_next_company_code()
                if response.success:
                    self.inputs['company_code'].text = response.data['code']
                    self.status_label.text = f'Generated company code: {response.data["code"]}'
                else:
                    self.status_label.text = f'Error generating company code: {response.message}'
            else:
                self.status_label.text = 'API not available'
        except Exception as e:
            Logger.error(f"Error generating company code: {str(e)}")
            self.status_label.text = f'Error generating company code: {str(e)}'

    def load_cities(self):
        """Load cities for the city dropdown"""
        try:
            if self.api_manager and self.api_manager.company:
                response = self.api_manager.company.get_cities()
                if response.success:
                    cities = response.data
                    city_options = ['Select City'] + [city['display'] for city in cities]
                    self.inputs['city_code'].values = city_options
                    self.status_label.text = f'Loaded {len(cities)} cities'
                else:
                    self.status_label.text = f'Error loading cities: {response.message}'
            else:
                self.status_label.text = 'API not available'
        except Exception as e:
            Logger.error(f"Error loading cities: {str(e)}")
            self.status_label.text = f'Error loading cities: {str(e)}'
