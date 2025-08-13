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
import datetime
import os
import csv

# Load the KV file
Builder.load_file('assets/kv/browse_gui.kv')

class PropertyRow(BoxLayout):
    """Widget representing a property row in the search results."""

    def __init__(self, property_data, on_view_callback, on_export_callback, **kwargs):
        super(PropertyRow, self).__init__(**kwargs)
        self.property_data = property_data
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(40)
        self.spacing = dp(5)
        self.padding = dp(5)

        # Add background - lighter gray for contrast
        with self.canvas.before:
            Color(0.98, 0.98, 0.98, 1)  # Very light gray
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

        # Property code
        property_code = property_data.get('realstatecode', 'N/A')
        if property_code is None:
            property_code = 'N/A'
        self.add_widget(Label(
            text=str(property_code),
            size_hint_x=0.15,
            color=(0, 0, 0, 1)  # Black text
        ))

        # Property type
        property_type = property_data.get('property_type', 'Unknown')
        if property_type is None:
            property_type = 'Unknown'
        self.add_widget(Label(
            text=str(property_type),
            size_hint_x=0.15,
            color=(0, 0, 0, 1)  # Black text
        ))

        # Area
        area = property_data.get('Property-area', '0')
        if area is None:
            area = '0'
        self.add_widget(Label(
            text=str(area),
            size_hint_x=0.1,
            color=(0, 0, 0, 1)  # Black text
        ))

        # Bedrooms
        bedrooms = property_data.get('N-of-bedrooms', '0')
        if bedrooms is None:
            bedrooms = '0'
        self.add_widget(Label(
            text=str(bedrooms),
            size_hint_x=0.1,
            color=(0, 0, 0, 1)  # Black text
        ))

        # Owner name
        owner_name = property_data.get('ownername', 'Unknown')
        if owner_name is None:
            owner_name = 'Unknown'
        self.add_widget(Label(
            text=str(owner_name),
            size_hint_x=0.2,
            color=(0, 0, 0, 1)  # Black text
        ))

        # Address
        address = property_data.get('Property-address', 'Not specified')
        if address is None:
            address = 'Not specified'
        self.add_widget(Label(
            text=str(address),
            size_hint_x=0.2,
            color=(0, 0, 0, 1)  # Black text
        ))

        # Action buttons
        actions = BoxLayout(size_hint_x=0.1, spacing=dp(5))

        view_button = Button(
            text='View',
            background_color=(0.2, 0.6, 1, 1),  # Blue button
            color=(1, 1, 1, 1)  # White text
        )
        view_button.bind(on_press=lambda x: on_view_callback(property_data))
        actions.add_widget(view_button)

        self.add_widget(actions)

    def update_rect(self, instance, value):
        """Update the rectangle position and size."""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

class PropertyDetailPopup(Popup):
    """Popup to show property details."""

    def __init__(self, property_data, **kwargs):
        super(PropertyDetailPopup, self).__init__(**kwargs)
        property_code = property_data.get('realstatecode', 'Unknown')
        if property_code is None:
            property_code = 'Unknown'
        self.title = f"Property Details: {property_code}"
        
        # Add property details to the details_grid from KV file
        self.add_property_details(property_data)
        
        # Load and display photos
        self.load_property_photos(property_code)

    def add_property_details(self, property_data):
        """Add property details to the details grid."""
        details_grid = self.ids.details_grid
        details_grid.clear_widgets()        # Add property details
        fields = [
            ('Property Code', 'realstatecode'),
            ('Property Type', 'property_type'),
            ('Building Type', 'building_type'),
            ('Year Built', 'Yearmake'),
            ('Area (m²)', 'Property-area'),
            ('Facade (m)', 'Property-facade'),
            ('Depth (m)', 'Property-depth'),
            ('Bedrooms', 'N-of-bedrooms'),
            ('Bathrooms', 'N-of-bathrooms'),
            ('Floors', 'Property-floors'),
            ('Corner Property', 'Property-corner'),
            ('Price', 'Property-price'),
            ('Currency', 'Property-currency'),
            ('Address', 'Property-address'),
            ('Owner', 'ownername'),
            ('Owner Code', 'Ownercode'),
            ('Description', 'Descriptions'),
        ]

        for label, field in fields:
            details_grid.add_widget(Label(
                text=label + ':',
                size_hint_y=None,
                height=dp(40),
                halign='right',
                valign='middle',
                bold=True,
                text_size=(dp(200), dp(40)),
                color=(0.2, 0.2, 0.2, 1)
            ))

            value = property_data.get(field, 'Not specified')
            if field == 'Property-corner':
                value = 'Yes' if value else 'No'
            elif field == 'Property-price' and value:
                currency = property_data.get('Property-currency', '')
                value = f"{value} {currency}".strip()
            elif value is None:
                value = 'Not specified'

            details_grid.add_widget(Label(
                text=str(value),
                size_hint_y=None,
                height=dp(40),
                halign='left',
                valign='middle',
                text_size=(dp(300), dp(40)),
                color=(0, 0, 0, 1)
            ))

    def load_property_photos(self, property_code):
        """Load and display property photos."""
        try:
            photo_gallery = self.ids.photo_gallery
            photo_gallery.clear_widgets()
            
            api = get_api()
            photos = api.get_property_photos(property_code)

            if not photos or len(photos) == 0:
                photo_gallery.add_widget(Label(
                    text='No photos available\nfor this property',
                    size_hint_y=None,
                    height=dp(100),
                    color=(0.5, 0.5, 0.5, 1),
                    halign='center',
                    valign='middle'
                ))
                return

            for photo in photos:
                storage_path = photo.get('Storagepath', '')
                filename = photo.get('photofilename', '')

                if filename:
                    photo_path = os.path.join(storage_path, filename)

                    if os.path.exists(photo_path):
                        # Create image container
                        photo_container = BoxLayout(
                            orientation='vertical',
                            size_hint_y=None,
                            height=dp(200),
                            spacing=dp(5)
                        )

                        try:
                            from kivy.uix.image import Image
                            img = Image(
                                source=photo_path,
                                size_hint=(1, 1),
                                fit_mode='contain'
                            )
                            photo_container.add_widget(img)

                            # Add photo filename label
                            photo_container.add_widget(Label(
                                text=filename,
                                size_hint_y=None,
                                height=dp(30),
                                font_size=dp(12),
                                color=(0.4, 0.4, 0.4, 1),
                                halign='center'
                            ))

                            photo_gallery.add_widget(photo_container)

                        except Exception as e:
                            # Error loading specific image
                            photo_gallery.add_widget(Label(
                                text=f'Error loading: {filename}\n{str(e)}',
                                size_hint_y=None,
                                height=dp(60),
                                color=(0.8, 0.2, 0.2, 1),
                                halign='center'
                            ))
                    else:
                        # Photo file not found
                        photo_gallery.add_widget(Label(
                            text=f'Photo: {filename}\n(File not found)',
                            size_hint_y=None,
                            height=dp(60),
                            color=(0.8, 0.2, 0.2, 1),
                            halign='center'
                        ))

        except Exception as e:
            photo_gallery = self.ids.photo_gallery
            photo_gallery.add_widget(Label(
                text=f'Error loading photos:\n{str(e)}',
                size_hint_y=None,
                height=dp(60),
                color=(0.8, 0.2, 0.2, 1),
                halign='center'
            ))
                    text='No photos available\nfor this property',
                    size_hint_y=None,
                    height=dp(100),
                    color=(0.5, 0.5, 0.5, 1),
                    halign='center',
                    valign='middle'
                ))
                return

            for photo in photos:
                storage_path = photo.get('Storagepath', '')
                filename = photo.get('photofilename', '')

                if filename:
                    photo_path = os.path.join(storage_path, filename)

                    if os.path.exists(photo_path):
                        # Create image container
                        photo_container = BoxLayout(
                            orientation='vertical',
                            size_hint_y=None,
                            height=dp(200),
                            spacing=dp(5)
                        )

                        try:
                            from kivy.uix.image import Image
                            img = Image(
                                source=photo_path,
                                size_hint=(1, 1),
                                fit_mode='contain'
                            )
                            photo_container.add_widget(img)

                            # Add photo filename label
                            photo_container.add_widget(Label(
                                text=filename,
                                size_hint_y=None,
                                height=dp(30),
                                font_size=dp(12),
                                color=(0.4, 0.4, 0.4, 1),
                                halign='center'
                            ))

                            self.photo_gallery.add_widget(photo_container)
                        except Exception as e:
                            # If image loading fails, show filename
                            self.photo_gallery.add_widget(Label(
                                text=f'Photo: {filename}\n(Preview not available)',
                                size_hint_y=None,
                                height=dp(60),
                                color=(0.5, 0.5, 0.5, 1),
                                halign='center'
                            ))
                    else:
                        # Photo file not found
                        self.photo_gallery.add_widget(Label(
                            text=f'Photo: {filename}\n(File not found)',
                            size_hint_y=None,
                            height=dp(60),
                            color=(0.8, 0.2, 0.2, 1),
                            halign='center'
                        ))

        except Exception as e:
            self.photo_gallery.add_widget(Label(
                text=f'Error loading photos:\n{str(e)}',
                size_hint_y=None,
                height=dp(60),
                color=(0.8, 0.2, 0.2, 1),
                halign='center'
            ))

class SearchReportScreen(Screen):
    """Screen for searching properties and generating reports."""

    def __init__(self, **kwargs):
        super(SearchReportScreen, self).__init__(**kwargs)
        self.api = get_api()

        # Set white background for the screen
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # Main layout with better spacing
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Screen title with better styling
        title = Label(
            text='Property Search & Reports',
            font_size=dp(28),
            size_hint_y=None,
            height=dp(50),
            color=(0.1, 0.1, 0.1, 1),  # Dark gray text
            bold=True
        )
        self.layout.add_widget(title)

        # Search criteria section with better organization
        search_section = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(320), spacing=dp(10))

        # Section title
        search_title = Label(
            text='Search Criteria',
            font_size=dp(18),
            size_hint_y=None,
            height=dp(30),
            color=(0.2, 0.2, 0.2, 1),
            bold=True,
            halign='left'
        )
        search_title.bind(size=search_title.setter('text_size'))
        search_section.add_widget(search_title)

        # Search form with better grid layout
        search_form = GridLayout(cols=4, spacing=dp(15), size_hint_y=None, height=dp(280), row_default_height=dp(60))

        # Property type
        search_form.add_widget(Label(
            text='Property Type:',
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle'
        ))
        self.property_type_spinner = Spinner(
            text='All Types',
            values=['All Types'],
            size_hint_y=None,
            height=dp(45),
            background_color=(0.98, 0.98, 0.98, 1),
            color=(0, 0, 0, 1)
        )
        search_form.add_widget(self.property_type_spinner)

        # Building type
        search_form.add_widget(Label(
            text='Building Type:',
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle'
        ))
        self.building_type_spinner = Spinner(
            text='All Types',
            values=['All Types'],
            size_hint_y=None,
            height=dp(45),
            background_color=(0.98, 0.98, 0.98, 1),
            color=(0, 0, 0, 1)
        )
        search_form.add_widget(self.building_type_spinner)

        # Bedrooms range
        search_form.add_widget(Label(
            text='Bedrooms:',
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle'
        ))
        bedrooms_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(45))
        self.min_bedrooms = TextInput(
            hint_text='Min',
            multiline=False,
            input_filter='int',
            size_hint_x=0.5,
            size_hint_y=None,
            height=dp(45),
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0, 0, 0, 1),
            font_size=dp(14)
        )
        bedrooms_layout.add_widget(self.min_bedrooms)
        self.max_bedrooms = TextInput(
            hint_text='Max',
            multiline=False,
            input_filter='int',
            size_hint_x=0.5,
            size_hint_y=None,
            height=dp(45),
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0, 0, 0, 1),
            font_size=dp(14)
        )
        bedrooms_layout.add_widget(self.max_bedrooms)
        search_form.add_widget(bedrooms_layout)

        # Area range
        search_form.add_widget(Label(
            text='Area (m²):',
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle'
        ))
        area_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(45))
        self.min_area = TextInput(
            hint_text='Min',
            multiline=False,
            input_filter='float',
            size_hint_x=0.5,
            size_hint_y=None,
            height=dp(45),
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0, 0, 0, 1),
            font_size=dp(14)
        )
        area_layout.add_widget(self.min_area)
        self.max_area = TextInput(
            hint_text='Max',
            multiline=False,
            input_filter='float',
            size_hint_x=0.5,
            size_hint_y=None,
            height=dp(45),
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0, 0, 0, 1),
            font_size=dp(14)
        )
        area_layout.add_widget(self.max_area)
        search_form.add_widget(area_layout)

        # Address
        search_form.add_widget(Label(
            text='Address:',
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle'
        ))
        self.address_input = TextInput(
            hint_text='Enter address',
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0, 0, 0, 1),
            font_size=dp(14)
        )
        search_form.add_widget(self.address_input)

        # Owner name
        search_form.add_widget(Label(
            text='Owner Name:',
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle'
        ))
        self.owner_input = TextInput(
            hint_text='Enter owner name',
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0, 0, 0, 1),
            font_size=dp(14)
        )
        search_form.add_widget(self.owner_input)

        # Corner property
        search_form.add_widget(Label(
            text='Corner Property:',
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle'
        ))
        corner_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(45))
        self.corner_checkbox = CheckBox(size_hint=(None, None), size=(dp(30), dp(30)))
        corner_layout.add_widget(self.corner_checkbox)
        corner_layout.add_widget(Label(text='Yes', color=(0, 0, 0, 1), size_hint_x=None, width=dp(50)))
        corner_layout.add_widget(Label(text='', size_hint_x=1))  # Spacer
        search_form.add_widget(corner_layout)

        search_section.add_widget(search_form)
        self.layout.add_widget(search_section)

        # Search buttons with better styling
        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(15),
            padding=[dp(50), 0, dp(50), 0]
        )

        search_button = Button(
            text='Search Properties',
            size_hint_x=0.3,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        search_button.bind(on_press=self.perform_search)
        buttons_layout.add_widget(search_button)

        clear_button = Button(
            text='Clear All',
            size_hint_x=0.2,
            background_color=(0.7, 0.7, 0.7, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        clear_button.bind(on_press=self.clear_search)
        buttons_layout.add_widget(clear_button)

        export_button = Button(
            text='Export Results',
            size_hint_x=0.3,
            background_color=(0.2, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        export_button.bind(on_press=self.export_results)
        buttons_layout.add_widget(export_button)

        self.layout.add_widget(buttons_layout)

        # Results section with better spacing
        results_section = BoxLayout(orientation='vertical', spacing=dp(10))

        # Results count with better styling
        self.results_count = Label(
            text='0 properties found',
            size_hint_y=None,
            height=dp(35),
            color=(0.2, 0.2, 0.2, 1),
            font_size=dp(16),
            bold=True,
            halign='left'
        )
        self.results_count.bind(size=self.results_count.setter('text_size'))
        results_section.add_widget(self.results_count)

        # Results header with better proportions
        results_header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(5),
            padding=dp(10)
        )

        # Set background for header
        with results_header.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            results_header.rect = Rectangle(pos=results_header.pos, size=results_header.size)
        results_header.bind(pos=lambda instance, value: setattr(results_header.rect, 'pos', instance.pos))
        results_header.bind(size=lambda instance, value: setattr(results_header.rect, 'size', instance.size))

        headers = [
            ('Code', 0.15),
            ('Type', 0.15),
            ('Area', 0.1),
            ('Bedrooms', 0.1),
            ('Owner', 0.2),
            ('Address', 0.2),
            ('Actions', 0.1)
        ]

        for header, size in headers:
            results_header.add_widget(Label(
                text=header,
                size_hint_x=size,
                bold=True,
                color=(0.1, 0.1, 0.1, 1),
                font_size=dp(14)
            ))

        results_section.add_widget(results_header)

        # Results container with scroll
        self.results_container = GridLayout(cols=1, spacing=dp(2), size_hint_y=None)
        self.results_container.bind(minimum_height=self.results_container.setter('height'))

        results_scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        results_scroll.add_widget(self.results_container)
        results_section.add_widget(results_scroll)

        self.layout.add_widget(results_section)

        # Back button with better positioning
        footer_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), padding=[0, dp(10), 0, 0])
        back_button = Button(
            text='← Back to Main',
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            background_color=(0.4, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        back_button.bind(on_press=self.go_to_main_gui)
        footer_layout.add_widget(back_button)
        footer_layout.add_widget(Label())  # Spacer
        self.layout.add_widget(footer_layout)

        # Store search results
        self.search_results = []

        self.add_widget(self.layout)

    def update_bg(self, instance, value):
        """Update the background rectangle."""
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_enter(self):
        """Load the property types and building types when entering the screen."""
        self.load_property_types()
        self.load_building_types()
        # Load all properties initially
        self.load_all_properties()

    def load_all_properties(self):
        """Load and display all properties initially."""
        try:
            all_properties = self.api.get_all_properties()
            self.search_results = all_properties or []
            self.display_results(self.search_results)
        except Exception as e:
            self.results_count.text = f"Error loading properties: {str(e)}"

    def load_property_types(self):
        """Load property types from the database."""
        property_types = self.api.get_property_types() or []

        try:
            if property_types:
                values = ['All Types'] + [f"{pt.get('code', 'N/A')} - {pt.get('name', 'Unknown')}" for pt in property_types]
                self.property_type_spinner.values = values
            else:
                self.property_type_spinner.values = ['All Types']
        except Exception as e:
            print(f"Error loading property types: {e}")
            self.property_type_spinner.values = ['All Types']

    def load_building_types(self):
        """Load building types from the database."""
        building_types = self.api.get_building_types() or []

        try:
            if building_types:
                values = ['All Types'] + [f"{bt.get('code', 'N/A')} - {bt.get('name', 'Unknown')}" for bt in building_types]
                self.building_type_spinner.values = values
            else:
                self.building_type_spinner.values = ['All Types']
        except Exception as e:
            print(f"Error loading building types: {e}")
            self.building_type_spinner.values = ['All Types']

    def perform_search(self, instance):
        """Perform property search based on criteria."""
        search_criteria = {}

        # Property type
        if self.property_type_spinner.text != 'All Types':
            code = self.property_type_spinner.text.split(' - ')[0]
            search_criteria['Rstatetcode'] = code

        # Building type
        if self.building_type_spinner.text != 'All Types':
            code = self.building_type_spinner.text.split(' - ')[0]
            search_criteria['Buildtcode'] = code

        # Bedrooms
        if self.min_bedrooms.text and self.max_bedrooms.text:
            # We'll handle min/max in the client side filtering
            pass
        elif self.min_bedrooms.text:
            search_criteria['N-of-bedrooms'] = int(self.min_bedrooms.text)
        elif self.max_bedrooms.text:
            # Just use max as exact for now (refine later)
            search_criteria['N-of-bedrooms'] = int(self.max_bedrooms.text)

        # Area - handle in client side filtering

        # Address
        if self.address_input.text:
            search_criteria['Property-address'] = '%' + self.address_input.text + '%'

        # Owner name - search in joined table
        # We'll handle this in client side filtering

        # Corner property
        if self.corner_checkbox.active:
            search_criteria['Property-corner'] = True

        # Perform the search
        results = self.api.search_properties(search_criteria)

        # Apply client-side filtering for complex criteria
        filtered_results = []
        for prop in results:
            # Filter by area range if specified
            if self.min_area.text and self.max_area.text:
                min_area = float(self.min_area.text)
                max_area = float(self.max_area.text)
                if 'Property-area' not in prop or prop['Property-area'] < min_area or prop['Property-area'] > max_area:
                    continue
            elif self.min_area.text:
                min_area = float(self.min_area.text)
                if 'Property-area' not in prop or prop['Property-area'] < min_area:
                    continue
            elif self.max_area.text:
                max_area = float(self.max_area.text)
                if 'Property-area' not in prop or prop['Property-area'] > max_area:
                    continue

            # Filter by bedroom range if both min and max specified
            if self.min_bedrooms.text and self.max_bedrooms.text:
                min_bedrooms = int(self.min_bedrooms.text)
                max_bedrooms = int(self.max_bedrooms.text)
                if 'N-of-bedrooms' not in prop or prop['N-of-bedrooms'] < min_bedrooms or prop['N-of-bedrooms'] > max_bedrooms:
                    continue

            # Filter by owner name
            if self.owner_input.text:
                owner_name = self.owner_input.text.lower()
                if 'ownername' not in prop or owner_name not in prop['ownername'].lower():
                    continue

            filtered_results.append(prop)

        # Store and display results
        self.search_results = filtered_results
        self.display_results(filtered_results)

    def display_results(self, results):
        """Display the search results."""
        self.results_container.clear_widgets()
        self.results_count.text = f"{len(results)} properties found"

        if not results:
            self.results_container.add_widget(Label(
                text="No properties found matching your criteria.",
                size_hint_y=None,
                height=dp(60),
                color=(0.5, 0.5, 0.5, 1),
                font_size=dp(16)
            ))
            return

        for prop in results:
            self.results_container.add_widget(PropertyRow(
                prop,
                self.view_property_details,
                self.export_property
            ))

    def view_property_details(self, property_data):
        """Show detailed view of a property."""
        popup = PropertyDetailPopup(property_data)
        popup.open()

    def export_property(self, property_data):
        """Export a single property to CSV."""
        self.export_to_csv([property_data])

    def export_results(self, instance):
        """Export all search results to CSV."""
        if not self.search_results:
            popup = Popup(
                title='Export Error',
                content=Label(text='No search results to export.', color=(0, 0, 0, 1)),
                size_hint=(0.6, 0.3)
            )
            popup.open()
            return

        self.export_to_csv(self.search_results)

    def export_to_csv(self, properties):
        """Export properties to a CSV file."""
        try:
            # Create exports directory if it doesn't exist
            export_dir = os.path.join(os.path.expanduser('~'), 'property_exports')
            os.makedirs(export_dir, exist_ok=True)

            # Generate filename with timestamp
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(export_dir, f'property_export_{timestamp}.csv')

            # Define CSV headers
            headers = [
                'Property Code', 'Property Type', 'Building Type', 'Area',
                'Bedrooms', 'Bathrooms', 'Corner Property', 'Address',
                'Owner Name', 'Owner Code', 'Description'
            ]

            # Write to CSV
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)

                for prop in properties:
                    writer.writerow([
                        prop.get('realstatecode', ''),
                        prop.get('property_type', ''),
                        prop.get('building_type', ''),
                        prop.get('Property-area', ''),
                        prop.get('N-of-bedrooms', ''),
                        prop.get('N-of-bathrooms', ''),
                        'Yes' if prop.get('Property-corner', False) else 'No',
                        prop.get('Property-address', ''),
                        prop.get('ownername', ''),
                        prop.get('Ownercode', ''),
                        prop.get('Descriptions', '')
                    ])

            # Show success message
            popup = Popup(
                title='Export Successful',
                content=Label(text=f'Properties exported to:\n{filename}', color=(0, 0, 0, 1)),
                size_hint=(0.7, 0.3)
            )
            popup.open()

        except Exception as e:
            # Show error message
            popup = Popup(
                title='Export Error',
                content=Label(text=f'Failed to export properties: {str(e)}', color=(0, 0, 0, 1)),
                size_hint=(0.7, 0.3)
            )
            popup.open()

    def clear_search(self, instance):
        """Clear all search criteria."""
        self.property_type_spinner.text = 'All Types'
        self.building_type_spinner.text = 'All Types'
        self.min_bedrooms.text = ''
        self.max_bedrooms.text = ''
        self.min_area.text = ''
        self.max_area.text = ''
        self.address_input.text = ''
        self.owner_input.text = ''
        self.corner_checkbox.active = False

        # Clear results
        self.search_results = []
        self.results_container.clear_widgets()
        self.results_count.text = '0 properties found'

    def go_to_main_gui(self, instance=None):
        """Navigate back to the main GUI."""
        self.manager.current = 'main_gui'
