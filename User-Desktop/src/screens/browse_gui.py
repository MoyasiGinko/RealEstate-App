from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from src.models.database_api import get_api
from configs.arabic_fonts import apply_arabic_font
from configs.language_manager import get_language_manager, get_text
import datetime
import os
import csv

# Load the KV file
Builder.load_file('assets/kv/browse_gui.kv')

class PropertyDetailContent(BoxLayout):
    """Content widget for property details popup."""

    def __init__(self, property_data, popup_instance, **kwargs):
        super(PropertyDetailContent, self).__init__(**kwargs)
        self.property_data = property_data
        self.popup = popup_instance  # Reference to the popup for dismiss functionality
        self.language_manager = get_language_manager()

        # Set up the layout
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(15)

        # Set white background
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Create the UI immediately
        self.build_ui()
        self.populate_data()

    def update_rect(self, instance, value):
        """Update background rectangle when widget size/position changes."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def build_ui(self):
        """Build the UI components programmatically."""
        # Main content area
        main_layout = BoxLayout(orientation='horizontal', spacing=dp(20))

        # Property details on the left (60% width)
        details_scroll = ScrollView(size_hint=(0.6, 1))
        self.details_grid = GridLayout(
            cols=2,
            spacing=dp(30),
            size_hint_y=None,
            padding=dp(10)
        )
        self.details_grid.bind(minimum_height=self.details_grid.setter('height'))
        details_scroll.add_widget(self.details_grid)
        main_layout.add_widget(details_scroll)

        # Photo gallery on the right (40% width)
        photo_layout = BoxLayout(orientation='vertical', size_hint=(0.4, 1))

        # Photo section title
        photo_title_text = get_text('property_photos', 'Property Photos')
        photo_title = Label(
            text=photo_title_text,
            size_hint_y=None,
            height=dp(40),
            font_size=dp(18),
            color=(0.2, 0.2, 0.2, 1),
            bold=True
        )
        if self.language_manager.current_language == 'ar':
            apply_arabic_font(photo_title, photo_title_text)
        photo_layout.add_widget(photo_title)

        # Photo gallery scroll view
        photo_scroll = ScrollView()
        self.photo_gallery = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None,
            padding=dp(10)
        )
        self.photo_gallery.bind(minimum_height=self.photo_gallery.setter('height'))
        photo_scroll.add_widget(self.photo_gallery)
        photo_layout.add_widget(photo_scroll)

        main_layout.add_widget(photo_layout)
        self.add_widget(main_layout)

        # Close button
        close_button_text = get_text('close', 'Close')
        close_button = Button(
            text=close_button_text,
            size_hint_y=None,
            height=dp(50),
            background_color=(0.6, 0.6, 0.6, 1),
            color=(1, 1, 1, 1)
        )
        if self.language_manager.current_language == 'ar':
            apply_arabic_font(close_button, close_button_text)
        close_button.bind(on_press=lambda x: self.popup.dismiss())
        self.add_widget(close_button)

    def populate_data(self):
        """Populate the content with data."""
        try:
            # Add property details
            self.add_property_details(self.property_data)

            # Load and display photos
            property_code = self.property_data.get('realstatecode', 'Unknown')
            self.load_property_photos(property_code)
        except Exception as e:
            print(f"Error populating popup data: {e}")

    def add_property_details(self, property_data):
        """Add property details to the details grid."""
        try:
            self.details_grid.clear_widgets()

            # Add property details with localized labels
            fields = [
                ('property_code_label', 'realstatecode'),
                ('property_type_label', 'property_type'),
                ('building_type_label', 'building_type'),
                ('year_built', 'Yearmake'),
                ('area_m2', 'Property-area'),
                ('facade_m', 'Property-facade'),
                ('depth_m', 'Property-depth'),
                ('bedrooms_label', 'N-of-bedrooms'),
                ('bathrooms_label', 'N-of-bathrooms'),
                ('floors_label', 'Property-floors'),
                ('corner_property_label', 'Property-corner'),
                ('price_label', 'Property-price'),
                ('currency_label', 'Property-currency'),
                ('province_label', 'province_name'),
                ('region_label', 'region_name'),
                ('address_label', 'Property-address'),
                ('owner_label', 'ownername'),
                ('owner_code_label', 'Ownercode'),
                ('description_label', 'Descriptions'),
            ]

            for label_key, field in fields:
                # Get localized label text
                label_text = get_text(label_key, label_key.replace('_', ' ').title())

                label_widget = Label(
                    text=label_text + ':',
                    size_hint_y=None,
                    height=dp(40),
                    halign='right',
                    valign='middle',
                    bold=True,
                    text_size=(dp(200), dp(40)),
                    color=(0.2, 0.2, 0.2, 1)
                )

                # Apply Arabic font if needed
                if self.language_manager.current_language == 'ar':
                    apply_arabic_font(label_widget, label_text)

                self.details_grid.add_widget(label_widget)

                value = property_data.get(field, get_text('not_specified', 'Not specified'))
                if value is None:
                    value = get_text('not_specified', 'Not specified')

                # Format special fields with localized values
                if field == 'Property-corner' and value == 1:
                    value = get_text('yes', 'Yes')
                elif field == 'Property-corner' and value == 0:
                    value = get_text('no', 'No')
                elif field == 'Property-price' and value != get_text('not_specified', 'Not specified'):
                    try:
                        price_float = float(value)
                        value = f"{price_float:,.2f}"
                    except (ValueError, TypeError):
                        pass

                value_widget = Label(
                    text=str(value),
                    size_hint_y=None,
                    height=dp(40),
                    halign='left',
                    valign='middle',
                    text_size=(dp(300), dp(40)),
                    color=(0.4, 0.4, 0.4, 1)
                )

                # Apply Arabic font if needed
                if self.language_manager.current_language == 'ar':
                    apply_arabic_font(value_widget, str(value))

                self.details_grid.add_widget(value_widget)

        except Exception as e:
            print(f"Error adding property details: {e}")

    def load_property_photos(self, property_code):
        """Load and display property photos."""
        try:
            self.photo_gallery.clear_widgets()

            # Get photos from database API
            api = get_api()
            photos = api.get_property_photos(property_code)

            if photos:
                for photo in photos:
                    storage_path = photo.get('Storagepath', '')
                    filename = photo.get('photofilename', '')

                    if filename and storage_path:
                        photo_path = os.path.join(storage_path, filename)

                        if os.path.exists(photo_path):
                            # Create image widget
                            img = Image(
                                source=photo_path,
                                size_hint_y=None,
                                height=dp(200),
                                allow_stretch=True,
                                keep_ratio=True
                            )
                            self.photo_gallery.add_widget(img)
                        else:
                            print(f"Photo not found: {photo_path}")

            if not photos or not any(
                photo.get('photofilename') and photo.get('Storagepath') and
                os.path.exists(os.path.join(photo.get('Storagepath', ''), photo.get('photofilename', '')))
                for photo in photos
            ):
                # No photos available - localized message
                no_photo_text = get_text('no_photos_available', 'No photos available for this property')
                no_photo_label = Label(
                    text=no_photo_text,
                    size_hint_y=None,
                    height=dp(100),
                    color=(0.5, 0.5, 0.5, 1)
                )
                if self.language_manager.current_language == 'ar':
                    apply_arabic_font(no_photo_label, no_photo_text)
                self.photo_gallery.add_widget(no_photo_label)

        except Exception as e:
            print(f"Error loading property photos: {e}")
            # Add error message - localized
            error_text = get_text('error_loading_photos', 'Error loading photos')
            error_label = Label(
                text=error_text,
                size_hint_y=None,
                height=dp(100),
                color=(1, 0, 0, 1)
            )
            if self.language_manager.current_language == 'ar':
                apply_arabic_font(error_label, error_text)
            self.photo_gallery.add_widget(error_label)

class PropertyRow(BoxLayout):
    """Widget representing a property row in the search results."""

    def __init__(self, property_data, on_view_callback, on_export_callback, **kwargs):
        super(PropertyRow, self).__init__(**kwargs)
        self.property_data = property_data
        self.language_manager = get_language_manager()
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.spacing = dp(5)

        # Set alternating row colors with a subtle background
        with self.canvas.before:
            Color(0.98, 0.98, 0.98, 1)  # Light gray background
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Property code
        code_label = Label(
            text=str(property_data.get('realstatecode', 'N/A')),
            size_hint_x=0.12,
            color=(0, 0, 0, 1),
            halign='center',
            font_size=dp(12)
        )
        code_label.bind(size=code_label.setter('text_size'))
        self.add_widget(code_label)

        # Property type
        property_type = str(property_data.get('property_type', 'N/A'))
        type_label = Label(
            text=property_type,
            size_hint_x=0.12,
            color=(0, 0, 0, 1),
            halign='center',
            font_size=dp(12)
        )
        type_label.bind(size=type_label.setter('text_size'))
        self.add_widget(type_label)

        # Area
        area = str(property_data.get('Property-area', 'N/A'))
        area_label = Label(
            text=area,
            size_hint_x=0.08,
            color=(0, 0, 0, 1),
            halign='center',
            font_size=dp(12)
        )
        area_label.bind(size=area_label.setter('text_size'))
        self.add_widget(area_label)

        # Bedrooms
        bedrooms = str(property_data.get('N-of-bedrooms', 'N/A'))
        bedrooms_label = Label(
            text=bedrooms,
            size_hint_x=0.08,
            color=(0, 0, 0, 1),
            halign='center',
            font_size=dp(12)
        )
        bedrooms_label.bind(size=bedrooms_label.setter('text_size'))
        self.add_widget(bedrooms_label)

        # Province
        province = str(property_data.get('province_name', 'N/A'))
        province_label = Label(
            text=province,
            size_hint_x=0.1,
            color=(0, 0, 0, 1),
            halign='center',
            font_size=dp(12)
        )
        province_label.bind(size=province_label.setter('text_size'))
        self.add_widget(province_label)

        # Owner name
        owner = str(property_data.get('ownername', 'N/A'))[:15] + '...' if len(str(property_data.get('ownername', 'N/A'))) > 15 else str(property_data.get('ownername', 'N/A'))
        owner_label = Label(
            text=owner,
            size_hint_x=0.15,
            color=(0, 0, 0, 1),
            halign='center',
            font_size=dp(12)
        )
        owner_label.bind(size=owner_label.setter('text_size'))
        self.add_widget(owner_label)

        # Address (truncated)
        address = str(property_data.get('Property-address', 'N/A'))[:25] + '...' if len(str(property_data.get('Property-address', 'N/A'))) > 25 else str(property_data.get('Property-address', 'N/A'))
        address_label = Label(
            text=address,
            size_hint_x=0.25,
            color=(0, 0, 0, 1),
            halign='center',
            font_size=dp(12)
        )
        address_label.bind(size=address_label.setter('text_size'))
        self.add_widget(address_label)

        # Action buttons
        actions_layout = BoxLayout(size_hint_x=0.1, spacing=dp(5))

        # View button
        view_button_text = get_text('view', 'View')
        view_button = Button(
            text=view_button_text,
            size_hint=(1, 1),
            background_color=(0.2, 0.7, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=dp(10)
        )
        if self.language_manager.current_language == 'ar':
            apply_arabic_font(view_button, view_button_text)
        view_button.bind(on_press=lambda x: on_view_callback(property_data))
        actions_layout.add_widget(view_button)

        self.add_widget(actions_layout)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class PropertyDetailPopup(Popup):
    """Popup to show property details."""

    def __init__(self, property_data, **kwargs):
        super(PropertyDetailPopup, self).__init__(**kwargs)
        property_code = property_data.get('realstatecode', get_text('unknown', 'Unknown'))
        if property_code is None:
            property_code = get_text('unknown', 'Unknown')

        # Localized title
        details_text = get_text( 'Property Details')
        self.title = f"{details_text}: {property_code}"
        self.size_hint = (0.9, 0.9)
        self.separator_color = (0.7, 0.7, 0.7, 1)

        # Create and set the content widget
        content = PropertyDetailContent(property_data, self)
        self.content = content


class SearchReportScreen(Screen):
    """Screen for searching properties and generating reports."""

    def __init__(self, **kwargs):
        super(SearchReportScreen, self).__init__(**kwargs)
        self.api = get_api()
        self.language_manager = get_language_manager()
        self.language_manager.register_observer(self)
        self.bind(on_enter=self.setup_arabic_fonts)

    def show_language_switcher(self):
        """Show language switcher popup"""
        from configs.language_switcher import LanguageSwitcherPopup
        popup = LanguageSwitcherPopup()
        popup.open()

    def setup_arabic_fonts(self, *args):
        """Apply Arabic fonts to all text widgets"""
        try:
            for widget in self.walk(restrict=True):
                if hasattr(widget, 'text') and widget.text:
                    apply_arabic_font(widget, widget.text)
        except Exception as e:
            print(f"Error setting up Arabic fonts: {e}")

    def on_language_changed(self):
        """Called when language is changed"""
        try:
            # Update static text elements
            self.update_texts()
            # Reload dynamic content with new language
            if hasattr(self, 'ids'):
                self.load_property_types()
                self.load_building_types()
                # Reload the current search results to apply new language
                self.refresh_results()
                self.setup_arabic_fonts()
        except Exception as e:
            print(f"Error handling language change: {e}")

    def refresh_results(self):
        """Refresh the current search results with new language settings."""
        try:
            # Get current search criteria and re-run the search
            if hasattr(self, 'ids') and hasattr(self.ids, 'results_layout'):
                # Check if we have active search criteria
                has_criteria = (
                    (self.ids.property_type_spinner.text != 'All Types' and self.ids.property_type_spinner.text != get_text('all_types', 'All Types')) or
                    (self.ids.building_type_spinner.text != 'All Types' and self.ids.building_type_spinner.text != get_text('all_types', 'All Types')) or
                    self.ids.min_bedrooms.text or
                    self.ids.max_bedrooms.text or
                    self.ids.min_price.text or
                    self.ids.max_price.text or
                    self.ids.corner_property.active
                )

                if has_criteria:
                    # Re-run the current search
                    self.perform_search(None)
                else:
                    # Load all properties if no search criteria
                    self.load_all_properties()
        except Exception as e:
            print(f"Error refreshing results: {e}")
            # Fallback to loading all properties
            self.load_all_properties()

    def update_texts(self):
        """Update all text widgets with current language"""
        try:
            # Define the mapping of IDs to translation keys
            text_mappings = {
                'screen_title': 'property_search_reports',
                'search_criteria_label': 'search_criteria',
                'results_title': 'search_results',
                'search_btn': 'search',
                'clear_search_btn': 'clear_search',
                'export_results_btn': 'export_results',
                'go_back_btn': 'go_back',
                'property_type_label': 'property_type',
                'building_type_label': 'building_type',
                'min_bedrooms_label': 'min_bedrooms',
                'max_bedrooms_label': 'max_bedrooms',
                'min_price_label': 'min_price',
                'max_price_label': 'max_price',
                'corner_property_label': 'corner_property'
            }

            # Update each widget using its ID
            for widget_id, text_key in text_mappings.items():
                try:
                    widget = self.ids.get(widget_id)
                    if widget:
                        new_text = get_text(text_key)
                        widget.text = new_text
                        # Apply Arabic font if needed
                        if self.language_manager.current_language == 'ar':
                            apply_arabic_font(widget, new_text)
                except Exception as e:
                    print(f"Error updating widget {widget_id}: {e}")

            # Update spinner default values
            try:
                all_types_text = get_text('all_types')
                if hasattr(self.ids, 'property_type_spinner'):
                    if self.ids.property_type_spinner.text in ['All Types', 'All Types', 'All Types']:
                        self.ids.property_type_spinner.text = all_types_text
                if hasattr(self.ids, 'building_type_spinner'):
                    if self.ids.building_type_spinner.text in ['All Types', 'All Types', 'All Types']:
                        self.ids.building_type_spinner.text = all_types_text
            except Exception as e:
                print(f"Error updating spinners: {e}")

        except Exception as e:
            print(f"Error updating texts: {e}")

    def update_localized_texts(self):
        """Update the KV file text elements"""
        try:
            self.update_texts()
        except Exception as e:
            print(f"Error updating localized texts: {e}")

    def on_enter(self):
        """Called when the screen is entered."""
        self.load_property_types()
        self.load_building_types()
        # Load all properties initially
        self.load_all_properties()
        # Update texts with current language
        self.update_texts()

    def load_all_properties(self):
        """Load and display all properties."""
        try:
            properties = self.api.search_properties({})
            self.display_results(properties)
        except Exception as e:
            print(f"Error loading properties: {e}")

    def load_property_types(self):
        """Load property types from the database."""
        property_types = self.api.get_property_types() or []

        try:
            if property_types:
                all_types_text = get_text('all_types')
                values = [all_types_text] + [f"{pt.get('code', 'N/A')} - {pt.get('name', 'Unknown')}" for pt in property_types]
                self.ids.property_type_spinner.values = values
                self.ids.property_type_spinner.text = all_types_text
            else:
                all_types_text = get_text('all_types')
                self.ids.property_type_spinner.values = [all_types_text]
                self.ids.property_type_spinner.text = all_types_text
        except Exception as e:
            print(f"Error loading property types: {e}")
            all_types_text = get_text('all_types')
            self.ids.property_type_spinner.values = [all_types_text]

    def load_building_types(self):
        """Load building types from the database."""
        building_types = self.api.get_building_types() or []

        try:
            if building_types:
                all_types_text = get_text('all_types')
                values = [all_types_text] + [f"{bt.get('code', 'N/A')} - {bt.get('name', 'Unknown')}" for bt in building_types]
                self.ids.building_type_spinner.values = values
                self.ids.building_type_spinner.text = all_types_text
            else:
                all_types_text = get_text('all_types')
                self.ids.building_type_spinner.values = [all_types_text]
                self.ids.building_type_spinner.text = all_types_text
        except Exception as e:
            print(f"Error loading building types: {e}")
            all_types_text = get_text('all_types')
            self.ids.building_type_spinner.values = [all_types_text]

    def perform_search(self, instance):
        """Perform property search based on criteria."""
        search_criteria = {}

        # Property type
        if self.ids.property_type_spinner.text != 'All Types':
            code = self.ids.property_type_spinner.text.split(' - ')[0]
            search_criteria['Rstatetcode'] = code

        # Building type
        if self.ids.building_type_spinner.text != 'All Types':
            code = self.ids.building_type_spinner.text.split(' - ')[0]
            search_criteria['Buildtcode'] = code

        # Bedrooms
        if self.ids.min_bedrooms.text and self.ids.max_bedrooms.text:
            # We'll handle min/max in the client side filtering
            pass
        elif self.ids.min_bedrooms.text:
            search_criteria['N-of-bedrooms'] = int(self.ids.min_bedrooms.text)
        elif self.ids.max_bedrooms.text:
            # Just use max as exact for now (refine later)
            search_criteria['N-of-bedrooms'] = int(self.ids.max_bedrooms.text)

        # Price range
        if self.ids.min_price.text and self.ids.max_price.text:
            # We'll handle min/max in the client side filtering
            pass
        elif self.ids.min_price.text:
            search_criteria['Property-price'] = float(self.ids.min_price.text)
        elif self.ids.max_price.text:
            # Just use max as exact for now
            search_criteria['Property-price'] = float(self.ids.max_price.text)

        # Corner property
        if self.ids.corner_property.active:
            search_criteria['Property-corner'] = 1

        try:
            # Get results from database
            results = self.api.search_properties(search_criteria)

            # Client-side filtering for range queries
            filtered_results = []
            for result in results:
                # Filter by bedroom range
                if self.ids.min_bedrooms.text and self.ids.max_bedrooms.text:
                    bedrooms = result.get('N-of-bedrooms', 0)
                    if not (int(self.ids.min_bedrooms.text) <= bedrooms <= int(self.ids.max_bedrooms.text)):
                        continue

                # Filter by price range
                if self.ids.min_price.text and self.ids.max_price.text:
                    price = result.get('Property-price', 0)
                    if not (float(self.ids.min_price.text) <= price <= float(self.ids.max_price.text)):
                        continue

                filtered_results.append(result)

            self.display_results(filtered_results)

        except Exception as e:
            print(f"Error performing search: {e}")

    def display_results(self, results):
        """Display search results."""
        # Clear existing results
        self.ids.results_layout.clear_widgets()

        if not results:
            no_results_text = get_text('no_results_found', 'No properties found matching your criteria.')
            no_results = Label(
                text=no_results_text,
                size_hint_y=None,
                height=dp(50),
                color=(0.5, 0.5, 0.5, 1),
                font_size=dp(14)
            )
            if self.language_manager.current_language == 'ar':
                apply_arabic_font(no_results, no_results_text)
            self.ids.results_layout.add_widget(no_results)
            return

        # Add header row
        results_header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(5))

        # Set background for header
        with results_header.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            results_header.rect = Rectangle(pos=results_header.pos, size=results_header.size)
        results_header.bind(pos=lambda instance, value: setattr(results_header.rect, 'pos', instance.pos))
        results_header.bind(size=lambda instance, value: setattr(results_header.rect, 'size', instance.size))

        headers = [
            ('code', 0.12),
            ('type', 0.12),
            ('area', 0.08),
            ('bedrooms', 0.08),
            ('province', 0.1),
            ('owner_name', 0.15),
            ('address', 0.25),
            ('actions', 0.1)
        ]

        for header_key, size in headers:
            header_text = get_text(header_key, header_key.title())
            header_label = Label(
                text=header_text,
                size_hint_x=size,
                bold=True,
                color=(0.1, 0.1, 0.1, 1),
                font_size=dp(14)
            )
            if self.language_manager.current_language == 'ar':
                apply_arabic_font(header_label, header_text)
            results_header.add_widget(header_label)

        self.ids.results_layout.add_widget(results_header)

        # Add property rows
        for i, property_data in enumerate(results):
            if i % 2 == 0:
                property_row = PropertyRow(property_data, self.view_property_details, self.export_property)
            else:
                property_row = PropertyRow(property_data, self.view_property_details, self.export_property)
                # Alternate row color
                with property_row.canvas.before:
                    Color(0.95, 0.95, 0.95, 1)
                    property_row.rect = Rectangle(pos=property_row.pos, size=property_row.size)

            self.ids.results_layout.add_widget(property_row)

    def view_property_details(self, property_data):
        """Open property details popup."""
        popup = PropertyDetailPopup(property_data)
        popup.open()

    def export_property(self, property_data):
        """Export single property to CSV."""
        self.export_to_csv([property_data])

    def export_results(self, instance):
        """Export all current search results."""
        # Get all displayed properties
        properties = []
        for child in self.ids.results_layout.children:
            if isinstance(child, PropertyRow):
                properties.append(child.property_data)

        if properties:
            self.export_to_csv(properties)
        else:
            # Show message that no results to export
            no_export_message = get_text('no_results_to_export', 'No results to export')
            print(no_export_message)

    def export_to_csv(self, properties):
        """Export properties to CSV file."""
        try:
            # Create data/csv directory if it doesn't exist
            csv_dir = os.path.join("data", "csv")
            os.makedirs(csv_dir, exist_ok=True)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(csv_dir, f"property_report_{timestamp}.csv")

            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'Property Code', 'Property Type', 'Building Type', 'Year Built',
                    'Area (m²)', 'Facade (m)', 'Depth (m)', 'Bedrooms', 'Bathrooms',
                    'Floors', 'Corner Property', 'Price', 'Currency', 'Province',
                    'Region', 'Address', 'Owner Name', 'Owner Code', 'Description'
                ]

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for prop in properties:
                    writer.writerow({
                        'Property Code': prop.get('realstatecode', ''),
                        'Property Type': prop.get('property_type', ''),
                        'Building Type': prop.get('building_type', ''),
                        'Year Built': prop.get('Yearmake', ''),
                        'Area (m²)': prop.get('Property-area', ''),
                        'Facade (m)': prop.get('Property-facade', ''),
                        'Depth (m)': prop.get('Property-depth', ''),
                        'Bedrooms': prop.get('N-of-bedrooms', ''),
                        'Bathrooms': prop.get('N-of-bathrooms', ''),
                        'Floors': prop.get('Property-floors', ''),
                        'Corner Property': 'Yes' if prop.get('Property-corner') else 'No',
                        'Price': prop.get('Property-price', ''),
                        'Currency': prop.get('Property-currency', ''),
                        'Province': prop.get('province_name', ''),
                        'Region': prop.get('region_name', ''),
                        'Address': prop.get('Property-address', ''),
                        'Owner Name': prop.get('ownername', ''),
                        'Owner Code': prop.get('Ownercode', ''),
                        'Description': prop.get('Descriptions', '')
                    })

            print(f"Report exported successfully: {filename}")

        except Exception as e:
            print(f"Error exporting CSV: {e}")

    def clear_search(self, instance):
        """Clear all search criteria."""
        self.ids.property_type_spinner.text = 'All Types'
        self.ids.building_type_spinner.text = 'All Types'
        self.ids.min_bedrooms.text = ''
        self.ids.max_bedrooms.text = ''
        self.ids.min_price.text = ''
        self.ids.max_price.text = ''
        self.ids.corner_property.active = False

        # Load all properties again
        self.load_all_properties()

    def go_to_main_gui(self, instance=None):
        """Navigate back to main GUI."""
        if hasattr(self.manager, 'current'):
            self.manager.current = 'main_gui'
