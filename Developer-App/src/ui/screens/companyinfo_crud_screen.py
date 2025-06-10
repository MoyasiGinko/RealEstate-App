"""
CompanyInfo CRUD Screen - Simplified Functional Version
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
from kivy.clock import Clock
from src.api.models import CompanyInfo


class CompanyInfoCRUDScreen(BoxLayout):
    """CompanyInfo CRUD operations screen - Functional version"""

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

        back_btn = Button(
            text='← Back to Dashboard',
            size_hint_x=None,
            width=200,
            background_color=(0.3, 0.6, 0.9, 1)
        )
        back_btn.bind(on_press=self.go_back)
        header_layout.add_widget(back_btn)

        title = Label(
            text='🏢 Company Management',
            font_size=24,
            bold=True,
            color=(0.2, 0.4, 0.8, 1)
        )
        header_layout.add_widget(title)

        refresh_btn = Button(
            text='🔄 Refresh',
            size_hint_x=None,
            width=100,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        refresh_btn.bind(on_press=lambda x: self.refresh_data())
        header_layout.add_widget(refresh_btn)

        self.add_widget(header_layout)

        # Main content area
        content_layout = BoxLayout(orientation='horizontal', spacing=20)

        # Left panel - Data list with search
        left_panel = self.create_data_panel()
        content_layout.add_widget(left_panel)

        # Right panel - Form
        right_panel = self.create_form_panel()
        content_layout.add_widget(right_panel)

        self.add_widget(content_layout)

        # Status bar
        self.status_label = Label(
            text='Ready to create new Company record',
            size_hint_y=None,
            height=30,
            color=(0.6, 0.6, 0.6, 1)
        )
        self.add_widget(self.status_label)

    def create_data_panel(self):
        """Create the data list panel"""
        panel = BoxLayout(orientation='vertical', size_hint_x=0.6, spacing=10)

        # Panel header with search
        header_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100, spacing=10)

        title = Label(
            text='📋 Company Records',
            font_size=18,
            bold=True,
            size_hint_y=None,
            height=40,
            color=(0.2, 0.4, 0.8, 1)
        )
        header_layout.add_widget(title)

        # Search bar
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

        self.search_input = TextInput(
            hint_text='🔍 Search companies...',
            size_hint_y=None,
            height=40,
            multiline=False
        )
        self.search_input.bind(text=self.on_search_text)
        search_layout.add_widget(self.search_input)

        search_btn = Button(
            text='Search',
            size_hint_x=None,
            width=80,
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.4, 0.8, 1)
        )
        search_btn.bind(on_press=self.perform_search)
        search_layout.add_widget(search_btn)

        clear_btn = Button(
            text='Clear',
            size_hint_x=None,
            width=60,
            size_hint_y=None,
            height=40,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        clear_btn.bind(on_press=self.clear_search)
        search_layout.add_widget(clear_btn)

        header_layout.add_widget(search_layout)
        panel.add_widget(header_layout)

        # Data display area
        self.data_scroll = ScrollView()
        self.data_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.data_layout.bind(minimum_height=self.data_layout.setter('height'))
        self.data_scroll.add_widget(self.data_layout)
        panel.add_widget(self.data_scroll)

        return panel

    def create_form_panel(self):
        """Create the form panel"""
        panel = BoxLayout(orientation='vertical', size_hint_x=0.4, spacing=10)

        form_header = Label(
            text='📝 Company Form',
            font_size=18,
            bold=True,
            size_hint_y=None,
            height=40,
            color=(0.2, 0.4, 0.8, 1)
        )
        panel.add_widget(form_header)

        # Form scroll view
        form_scroll = ScrollView()
        form_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=[10, 10])
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Input fields
        self.inputs = {}

        # Company Code with auto-generation
        form_layout.add_widget(Label(text='🏷️ Company Code:', size_hint_y=None, height=30, halign='left'))
        company_code_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.inputs['company_code'] = TextInput(
            hint_text='e.g., E001',
            size_hint_y=None,
            height=40
        )
        company_code_layout.add_widget(self.inputs['company_code'])

        auto_company_btn = Button(
            text='🎲 Auto',
            size_hint_x=None,
            width=80,
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        auto_company_btn.bind(on_press=self.generate_company_code)
        company_code_layout.add_widget(auto_company_btn)
        form_layout.add_widget(company_code_layout)

        # Company Name
        form_layout.add_widget(Label(text='🏢 Company Name:', size_hint_y=None, height=30, halign='left'))
        self.inputs['company_name'] = TextInput(
            hint_text='e.g., Best Real Estate Ltd.',
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['company_name'])

        # City Code with dropdown
        form_layout.add_widget(Label(text='🌆 City:', size_hint_y=None, height=30, halign='left'))
        self.inputs['city_code'] = Spinner(
            text='Select City',
            values=['Select City'],
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['city_code'])

        # Company Address
        form_layout.add_widget(Label(text='📍 Address:', size_hint_y=None, height=30, halign='left'))
        self.inputs['company_address'] = TextInput(
            hint_text='e.g., 123 Main Street',
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['company_address'])

        # Phone Number
        form_layout.add_widget(Label(text='📞 Phone Number:', size_hint_y=None, height=30, halign='left'))
        self.inputs['phone_number'] = TextInput(
            hint_text='e.g., +964 770 123 4567',
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['phone_number'])

        # Username
        form_layout.add_widget(Label(text='👤 Username:', size_hint_y=None, height=30, halign='left'))
        self.inputs['username'] = TextInput(
            hint_text='e.g., admin',
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['username'])

        # Password
        form_layout.add_widget(Label(text='🔒 Password:', size_hint_y=None, height=30, halign='left'))
        self.inputs['password'] = TextInput(
            hint_text='Enter secure password',
            password=True,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['password'])

        # Subscription Code dropdown
        form_layout.add_widget(Label(text='💼 Subscription Type:', size_hint_y=None, height=30, halign='left'))
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
        form_layout.add_widget(Label(text='⏰ Subscription Duration:', size_hint_y=None, height=30, halign='left'))
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
        form_layout.add_widget(Label(text='📄 Description:', size_hint_y=None, height=30, halign='left'))
        self.inputs['descriptions'] = TextInput(
            hint_text='e.g., Leading real estate company...',
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.inputs['descriptions'])

        # Action Buttons
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=10)

        # Primary buttons
        primary_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

        create_btn = Button(
            text='✅ Create Company',
            background_color=(0.2, 0.7, 0.3, 1)
        )
        create_btn.bind(on_press=self.create_company)
        primary_layout.add_widget(create_btn)

        self.update_btn = Button(
            text='📝 Update Company',
            background_color=(0.2, 0.4, 0.8, 1),
            disabled=True
        )
        self.update_btn.bind(on_press=self.update_company)
        primary_layout.add_widget(self.update_btn)

        button_layout.add_widget(primary_layout)

        # Secondary buttons
        secondary_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

        self.delete_btn = Button(
            text='🗑️ Delete Company',
            background_color=(0.8, 0.2, 0.2, 1),
            disabled=True
        )
        self.delete_btn.bind(on_press=self.delete_company)
        secondary_layout.add_widget(self.delete_btn)

        clear_btn = Button(
            text='🧹 Clear Form',
            background_color=(0.5, 0.5, 0.5, 1)
        )
        clear_btn.bind(on_press=self.clear_form)
        secondary_layout.add_widget(clear_btn)

        button_layout.add_widget(secondary_layout)
        form_layout.add_widget(button_layout)

        form_scroll.add_widget(form_layout)
        panel.add_widget(form_scroll)

        return panel

    def refresh_data(self):
        """Refresh data from database"""
        if not self.api_manager or not self.api_manager.is_initialized():
            self.status_label.text = "❌ Database not connected"
            return

        try:
            # Load company data
            response = self.api_manager.company.get_all_companies()
            if response.success:
                self.company_data = response.data
                self.display_data()
                self.status_label.text = f"✅ Loaded {len(self.company_data)} company records"
                Logger.info(f"Loaded {len(self.company_data)} Company records")
            else:
                self.status_label.text = f"❌ Error loading data: {response.error}"
                Logger.error(f"Failed to load Company data: {response.error}")

            # Load cities for dropdown
            self.load_cities()

        except Exception as e:
            self.status_label.text = f"❌ Error: {str(e)}"
            Logger.error(f"Error refreshing Company data: {str(e)}")

    def display_data(self):
        """Display data in the list"""
        self.data_layout.clear_widgets()

        if not self.company_data:
            no_data_label = Label(
                text='📭 No company records found\nCreate your first company to get started!',
                size_hint_y=None,
                height=80,
                halign='center',
                color=(0.6, 0.6, 0.6, 1)
            )
            self.data_layout.add_widget(no_data_label)
            return

        for company in self.company_data:
            self.create_data_row(company)

    def create_data_row(self, company):
        """Create a row for displaying company data"""
        row_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=120,
            spacing=5,
            padding=[10, 5, 10, 5]
        )

        # Add subtle background
        with row_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.98, 0.98, 0.98, 1)
            row_layout.bg = Rectangle(size=row_layout.size, pos=row_layout.pos)
        row_layout.bind(size=lambda instance, value: setattr(instance.bg, 'size', value))
        row_layout.bind(pos=lambda instance, value: setattr(instance.bg, 'pos', value))

        # Main info row
        main_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

        # Company info
        company_name = getattr(company, 'company_name', 'N/A')
        company_code = getattr(company, 'company_code', 'N/A')
        subscription_code = getattr(company, 'subscription_code', '')

        # Status indicator
        status_text = {'1': '🟡 Trial', '2': '🟢 Active', '3': '🔴 Inactive'}.get(subscription_code, '⚪ Unknown')

        info_text = f"🏢 {company_name} ({company_code}) - {status_text}"

        info_label = Label(
            text=info_text,
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=40,
            color=(0.2, 0.2, 0.2, 1)
        )
        info_label.bind(size=info_label.setter('text_size'))
        main_row.add_widget(info_label)

        # Select button
        select_btn = Button(
            text='📝 Select',
            size_hint_x=None,
            width=100,
            size_hint_y=None,
            height=35,
            background_color=(0.2, 0.4, 0.8, 1)
        )
        select_btn.bind(on_press=lambda x: self.select_company(company))
        main_row.add_widget(select_btn)

        row_layout.add_widget(main_row)

        # Details row
        phone = getattr(company, 'phone_number', 'N/A')
        city = getattr(company, 'city_code', 'N/A')
        username = getattr(company, 'username', 'N/A')

        details_text = f"📞 {phone} | 🌆 {city} | 👤 {username}"

        details_label = Label(
            text=details_text,
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=25,
            color=(0.5, 0.5, 0.5, 1)
        )
        details_label.bind(size=details_label.setter('text_size'))
        row_layout.add_widget(details_label)

        # Address row
        address = getattr(company, 'company_address', 'No address provided')
        address_text = f"📍 {address}"

        address_label = Label(
            text=address_text,
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=25,
            color=(0.5, 0.5, 0.5, 1)
        )
        address_label.bind(size=address_label.setter('text_size'))
        row_layout.add_widget(address_label)

        self.data_layout.add_widget(row_layout)

    def on_search_text(self, instance, text):
        """Handle search text changes"""
        # Simple debouncing with Clock
        if hasattr(self, 'search_event'):
            self.search_event.cancel()
        self.search_event = Clock.schedule_once(lambda dt: self.perform_search(), 0.5)

    def perform_search(self, button=None):
        """Perform search"""
        search_text = self.search_input.text.strip().lower()

        if not search_text:
            self.display_data()
            return

        # Filter data
        filtered_data = []
        for company in self.company_data:
            company_name = getattr(company, 'company_name', '').lower()
            company_code = getattr(company, 'company_code', '').lower()
            city_code = getattr(company, 'city_code', '').lower()
            phone = getattr(company, 'phone_number', '').lower()

            if (search_text in company_name or
                search_text in company_code or
                search_text in city_code or
                search_text in phone):
                filtered_data.append(company)

        # Display filtered results
        self.data_layout.clear_widgets()

        if not filtered_data:
            no_results = Label(
                text=f'🔍 No results found for "{search_text}"',
                size_hint_y=None,
                height=60,
                halign='center',
                color=(0.6, 0.6, 0.6, 1)
            )
            self.data_layout.add_widget(no_results)
        else:
            for company in filtered_data:
                self.create_data_row(company)

        self.status_label.text = f"🔍 Found {len(filtered_data)} results for '{search_text}'"

    def clear_search(self, button):
        """Clear search"""
        self.search_input.text = ''
        self.display_data()
        self.status_label.text = f"✅ Showing all {len(self.company_data)} companies"

    def select_company(self, company):
        """Select a company for editing"""
        self.selected_company = company

        # Populate form
        self.inputs['company_code'].text = getattr(company, 'company_code', '') or ''
        self.inputs['company_name'].text = getattr(company, 'company_name', '') or ''

        # Handle city code
        city_code = getattr(company, 'city_code', '')
        if city_code:
            city_found = False
            for city_option in self.inputs['city_code'].values:
                if city_option.startswith(city_code + ' - '):
                    self.inputs['city_code'].text = city_option
                    city_found = True
                    break
            if not city_found:
                self.inputs['city_code'].text = city_code
        else:
            self.inputs['city_code'].text = 'Select City'

        self.inputs['company_address'].text = getattr(company, 'company_address', '') or ''
        self.inputs['phone_number'].text = getattr(company, 'phone_number', '') or ''
        self.inputs['username'].text = getattr(company, 'username', '') or ''
        self.inputs['password'].text = getattr(company, 'password', '') or ''

        # Handle subscription dropdowns
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

        # Enable buttons
        self.update_btn.disabled = False
        self.delete_btn.disabled = False

        company_name = getattr(company, 'company_name', 'N/A')
        self.status_label.text = f"📝 Selected: {company_name}"

    def create_company(self, button):
        """Create new company"""
        try:
            if not self.validate_form():
                return

            # Extract data
            company_data = self.extract_form_data()

            response = self.api_manager.company.create_company(company_data)
            if response.success:
                self.status_label.text = "✅ Company created successfully!"
                self.clear_form()
                self.refresh_data()
            else:
                self.status_label.text = f"❌ Error creating company: {response.error}"
        except Exception as e:
            self.status_label.text = f"❌ Error: {str(e)}"

    def update_company(self, button):
        """Update selected company"""
        if not self.selected_company:
            self.status_label.text = "⚠️ No company selected"
            return

        try:
            if not self.validate_form():
                return

            update_data = self.extract_form_data(exclude_code=True)

            response = self.api_manager.company.update_company(
                getattr(self.selected_company, 'company_code', ''),
                update_data
            )

            if response.success:
                self.status_label.text = "✅ Company updated successfully!"
                self.clear_form()
                self.refresh_data()
            else:
                self.status_label.text = f"❌ Error updating company: {response.error}"
        except Exception as e:
            self.status_label.text = f"❌ Error: {str(e)}"

    def delete_company(self, button):
        """Delete selected company"""
        if not self.selected_company:
            self.status_label.text = "⚠️ No company selected"
            return

        try:
            company_code = getattr(self.selected_company, 'company_code', '')
            response = self.api_manager.company.delete_company(company_code)

            if response.success:
                self.status_label.text = "✅ Company deleted successfully!"
                self.clear_form()
                self.refresh_data()
            else:
                self.status_label.text = f"❌ Error deleting company: {response.error}"
        except Exception as e:
            self.status_label.text = f"❌ Error: {str(e)}"

    def validate_form(self):
        """Validate form inputs"""
        if not self.inputs['company_code'].text.strip():
            self.status_label.text = "⚠️ Please enter a company code"
            return False

        if not self.inputs['company_name'].text.strip():
            self.status_label.text = "⚠️ Please enter a company name"
            return False

        if self.inputs['city_code'].text == 'Select City':
            self.status_label.text = "⚠️ Please select a city"
            return False

        if self.inputs['subscription_code'].text == 'Select Subscription Type':
            self.status_label.text = "⚠️ Please select a subscription type"
            return False

        if self.inputs['subscription_duration'].text == 'Select Duration':
            self.status_label.text = "⚠️ Please select a subscription duration"
            return False

        return True

    def extract_form_data(self, exclude_code=False):
        """Extract form data"""
        # Extract city code
        city_text = self.inputs['city_code'].text
        city_code = None
        if city_text and city_text != 'Select City' and ' - ' in city_text:
            city_code = city_text.split(' - ')[0]
        elif city_text and city_text != 'Select City':
            city_code = city_text

        # Extract subscription code
        subscription_text = self.inputs['subscription_code'].text
        subscription_code = None
        if subscription_text and subscription_text != 'Select Subscription Type' and ' - ' in subscription_text:
            subscription_code = subscription_text.split(' - ')[0]

        # Extract duration code
        duration_text = self.inputs['subscription_duration'].text
        duration_code = None
        if duration_text and duration_text != 'Select Duration' and ' - ' in duration_text:
            duration_code = duration_text.split(' - ')[0]

        # Build data
        data = {
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

        if not exclude_code:
            data['company_code'] = self.inputs['company_code'].text

        return data

    def clear_form(self, button=None):
        """Clear the form"""
        for input_widget in self.inputs.values():
            if hasattr(input_widget, 'text'):
                input_widget.text = ''

        # Reset dropdowns
        self.inputs['city_code'].text = 'Select City'
        self.inputs['subscription_code'].text = 'Select Subscription Type'
        self.inputs['subscription_duration'].text = 'Select Duration'

        # Reset state
        self.selected_company = None
        self.update_btn.disabled = True
        self.delete_btn.disabled = True
        self.status_label.text = '🆕 Ready to create new company record'
        self.search_input.text = ''

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
                    self.status_label.text = f'🎲 Generated company code: {response.data["code"]}'
                else:
                    self.status_label.text = f'❌ Error generating code: {response.message}'
            else:
                self.status_label.text = '❌ API not available'
        except Exception as e:
            Logger.error(f"Error generating company code: {str(e)}")
            self.status_label.text = f'❌ Error generating code: {str(e)}'

    def load_cities(self):
        """Load cities for the city dropdown"""
        try:
            if self.api_manager and self.api_manager.company:
                response = self.api_manager.company.get_cities()
                if response.success:
                    cities = response.data
                    city_options = ['Select City'] + [city['display'] for city in cities]
                    self.inputs['city_code'].values = city_options
                    Logger.info(f'Loaded {len(cities)} cities for dropdown')
                else:
                    self.status_label.text = f'⚠️ Error loading cities: {response.message}'
        except Exception as e:
            Logger.error(f"Error loading cities: {str(e)}")
            self.status_label.text = f'❌ Error loading cities: {str(e)}'
