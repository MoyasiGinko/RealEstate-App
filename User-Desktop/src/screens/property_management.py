from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.clock import Clock
from datetime import datetime
import os
from src.models.database_api import get_api

class PropertyForm(BoxLayout):
    """Form for adding or editing a property."""

    def __init__(self, save_callback, property_data=None, **kwargs):
        super(PropertyForm, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)

        # Set white background
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.api = get_api()
        self.save_callback = save_callback
        self.property_data = property_data
        self.property_code = property_data.get('realstatecode') if property_data else None
        self.selected_photos = []

        # Create a scrollview for the form
        scroll_view = ScrollView(do_scroll_x=False)
        form_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Title
        title = 'Edit Property' if property_data else 'Add New Property'
        title_label = Label(
            text=title,
            font_size=dp(24),
            size_hint_y=None,
            height=dp(40),
            color=(0.2, 0.2, 0.2, 1)  # Dark gray text
        )
        form_layout.add_widget(title_label)

        # Property type (dropdown from Maincode where recty = 03)
        property_types = self.api.get_property_types() or []

        # Safely handle property types - ensure it's a list even if None is returned
        property_type_values = []
        if property_types:
            try:
                property_type_values = [f"{t.get('Code', 'N/A')} - {t.get('Name', 'Unknown')}" for t in property_types]
            except (KeyError, TypeError, AttributeError) as e:
                print(f"Error processing property types: {e}")
                # Fallback to empty list if there's an error

        # Add a default option if the list is empty
        if not property_type_values:
            property_type_values = ['No property types available']

        property_type_layout = BoxLayout(size_hint_y=None, height=dp(40))
        property_type_layout.add_widget(Label(
            text='Property Type:',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.property_type_spinner = Spinner(
            text='Select Property Type',
            values=property_type_values,
            size_hint_x=0.7,
            background_color=(0.95, 0.95, 0.95, 1),
            color=(0.2, 0.2, 0.2, 1)
        )

        # Safely set the spinner value if we have property data
        if property_data and property_data.get('Rstatetcode') and property_type_values and property_type_values[0] != 'No property types available':
            try:
                for val in property_type_values:
                    if val.startswith(property_data['Rstatetcode']):
                        self.property_type_spinner.text = val
                        break
            except Exception as e:
                print(f"Error setting property type spinner: {e}")
                # Continue without setting the spinner value

        property_type_layout.add_widget(self.property_type_spinner)
        form_layout.add_widget(property_type_layout)

        # Building type (dropdown from Maincode where recty = 04)
        building_types = self.api.get_building_types() or []

        # Safely handle building types
        building_type_values = []
        if building_types:
            try:
                building_type_values = [f"{t.get('Code', 'N/A')} - {t.get('Name', 'Unknown')}" for t in building_types]
            except (KeyError, TypeError, AttributeError) as e:
                print(f"Error processing building types: {e}")
                # Fallback to empty list if there's an error

        # Add a default option if the list is empty
        if not building_type_values:
            building_type_values = ['No building types available']

        building_type_layout = BoxLayout(size_hint_y=None, height=dp(40))
        building_type_layout.add_widget(Label(
            text='Building Type:',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.building_type_spinner = Spinner(
            text='Select Building Type',
            values=building_type_values,
            size_hint_x=0.7,
            background_color=(0.95, 0.95, 0.95, 1),
            color=(0.2, 0.2, 0.2, 1)
        )

        # Safely set the spinner value if we have property data
        if property_data and property_data.get('Buildtcode') and building_type_values and building_type_values[0] != 'No building types available':
            try:
                for val in building_type_values:
                    if val.startswith(property_data['Buildtcode']):
                        self.building_type_spinner.text = val
                        break
            except Exception as e:
                print(f"Error setting building type spinner: {e}")
                # Continue without setting the spinner value

        building_type_layout.add_widget(self.building_type_spinner)
        form_layout.add_widget(building_type_layout)

        # Year built
        year_layout = BoxLayout(size_hint_y=None, height=dp(40))
        year_layout.add_widget(Label(
            text='Year Built:',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        current_year = datetime.now().year
        year_values = [str(y) for y in range(1950, current_year + 1)]

        self.year_spinner = Spinner(
            text='Select Year',
            values=year_values,
            size_hint_x=0.7,
            background_color=(0.95, 0.95, 0.95, 1),
            color=(0.2, 0.2, 0.2, 1)
        )
        if property_data and property_data.get('Yearmake'):
            year = property_data['Yearmake'].split('-')[0]  # Extract year from ISO format
            if year in year_values:
                self.year_spinner.text = year

        year_layout.add_widget(self.year_spinner)
        form_layout.add_widget(year_layout)

        # Area
        area_layout = BoxLayout(size_hint_y=None, height=dp(40))
        area_layout.add_widget(Label(
            text='Area (m²):',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.area_input = TextInput(
            hint_text='Property Area',
            text=str(property_data.get('Property-area', '')) if property_data else '',
            input_filter='float',
            multiline=False,
            size_hint_x=0.7,
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        area_layout.add_widget(self.area_input)
        form_layout.add_widget(area_layout)

        # Facade
        facade_layout = BoxLayout(size_hint_y=None, height=dp(40))
        facade_layout.add_widget(Label(
            text='Facade (m):',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.facade_input = TextInput(
            hint_text='Facade Length',
            text=str(property_data.get('Property-facade', '')) if property_data else '',
            input_filter='float',
            multiline=False,
            size_hint_x=0.7,
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        facade_layout.add_widget(self.facade_input)
        form_layout.add_widget(facade_layout)

        # Depth
        depth_layout = BoxLayout(size_hint_y=None, height=dp(40))
        depth_layout.add_widget(Label(
            text='Depth (m):',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.depth_input = TextInput(
            hint_text='Property Depth',
            text=str(property_data.get('Property-depth', '')) if property_data else '',
            input_filter='float',
            multiline=False,
            size_hint_x=0.7,
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        depth_layout.add_widget(self.depth_input)
        form_layout.add_widget(depth_layout)

        # Bedrooms
        bedrooms_layout = BoxLayout(size_hint_y=None, height=dp(40))
        bedrooms_layout.add_widget(Label(
            text='Bedrooms:',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.bedrooms_input = TextInput(
            hint_text='Number of Bedrooms',
            text=str(property_data.get('N-of-bedrooms', '')) if property_data else '',
            input_filter='int',
            multiline=False,
            size_hint_x=0.7,
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        bedrooms_layout.add_widget(self.bedrooms_input)
        form_layout.add_widget(bedrooms_layout)

        # Bathrooms
        bathrooms_layout = BoxLayout(size_hint_y=None, height=dp(40))
        bathrooms_layout.add_widget(Label(
            text='Bathrooms:',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.bathrooms_input = TextInput(
            hint_text='Number of Bathrooms',
            text=str(property_data.get('N-of-bathrooms', '')) if property_data else '',
            input_filter='int',
            multiline=False,
            size_hint_x=0.7,
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        bathrooms_layout.add_widget(self.bathrooms_input)
        form_layout.add_widget(bathrooms_layout)

        # Is Corner
        corner_layout = BoxLayout(size_hint_y=None, height=dp(40))
        corner_layout.add_widget(Label(
            text='Is Corner Property:',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.corner_checkbox = CheckBox()
        if property_data and property_data.get('Property-corner'):
            self.corner_checkbox.active = bool(property_data['Property-corner'])

        corner_layout.add_widget(self.corner_checkbox)
        form_layout.add_widget(corner_layout)

        # Offer Type (dropdown from Maincode where recty = 06)
        offer_types = self.api.get_offer_types() or []

        # Safely handle offer types
        offer_type_values = []
        if offer_types:
            try:
                offer_type_values = [f"{t.get('Code', 'N/A')} - {t.get('Name', 'Unknown')}" for t in offer_types]
            except (KeyError, TypeError, AttributeError) as e:
                print(f"Error processing offer types: {e}")

        # Add a default option if the list is empty
        if not offer_type_values:
            offer_type_values = ['No offer types available']

        offer_type_layout = BoxLayout(size_hint_y=None, height=dp(40))
        offer_type_layout.add_widget(Label(
            text='Offer Type:',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.offer_type_spinner = Spinner(
            text='Select Offer Type',
            values=offer_type_values,
            size_hint_x=0.7,
            background_color=(0.95, 0.95, 0.95, 1),
            color=(0.2, 0.2, 0.2, 1)
        )

        # Safely set the spinner value if we have property data
        if property_data and property_data.get('Offer-Type-Code') and offer_type_values and offer_type_values[0] != 'No offer types available':
            try:
                for val in offer_type_values:
                    if val.startswith(property_data['Offer-Type-Code']):
                        self.offer_type_spinner.text = val
                        break
            except Exception as e:
                print(f"Error setting offer type spinner: {e}")

        offer_type_layout.add_widget(self.offer_type_spinner)
        form_layout.add_widget(offer_type_layout)

        # Province (dropdown from Maincode)
        provinces = self.api.get_provinces() or []

        # Safely handle provinces
        province_values = []
        if provinces:
            try:
                province_values = [f"{p.get('Code', 'N/A')} - {p.get('Name', 'Unknown')}" for p in provinces]
            except (KeyError, TypeError, AttributeError) as e:
                print(f"Error processing provinces: {e}")

        # Add a default option if the list is empty
        if not province_values:
            province_values = ['No provinces available']

        province_layout = BoxLayout(size_hint_y=None, height=dp(40))
        province_layout.add_widget(Label(
            text='Province:',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.province_spinner = Spinner(
            text='Select Province',
            values=province_values,
            size_hint_x=0.7,
            background_color=(0.95, 0.95, 0.95, 1),
            color=(0.2, 0.2, 0.2, 1)
        )

        # Safely set the spinner value if we have property data
        if property_data and property_data.get('Province-code') and province_values and province_values[0] != 'No provinces available':
            try:
                for val in province_values:
                    if val.startswith(property_data['Province-code']):
                        self.province_spinner.text = val
                        break
            except Exception as e:
                print(f"Error setting province spinner: {e}")

        province_layout.add_widget(self.province_spinner)
        form_layout.add_widget(province_layout)

        # Region (dropdown from Maincode)
        cities = self.api.get_cities() or []

        # Safely handle cities
        city_values = []
        if cities:
            try:
                city_values = [f"{c.get('Code', 'N/A')} - {c.get('Name', 'Unknown')}" for c in cities]
            except (KeyError, TypeError, AttributeError) as e:
                print(f"Error processing cities: {e}")

        # Add a default option if the list is empty
        if not city_values:
            city_values = ['No regions available']

        region_layout = BoxLayout(size_hint_y=None, height=dp(40))
        region_layout.add_widget(Label(
            text='Region:',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.region_spinner = Spinner(
            text='Select Region',
            values=city_values,
            size_hint_x=0.7,
            background_color=(0.95, 0.95, 0.95, 1),
            color=(0.2, 0.2, 0.2, 1)
        )

        # Safely set the spinner value if we have property data
        if property_data and property_data.get('Region-code') and city_values and city_values[0] != 'No regions available':
            try:
                for val in city_values:
                    if val.startswith(property_data['Region-code']):
                        self.region_spinner.text = val
                        break
            except Exception as e:
                print(f"Error setting region spinner: {e}")

        region_layout.add_widget(self.region_spinner)
        form_layout.add_widget(region_layout)

        # Address
        address_layout = BoxLayout(size_hint_y=None, height=dp(80))
        address_layout.add_widget(Label(
            text='Address:',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.address_input = TextInput(
            hint_text='Property Address',
            text=property_data.get('Property-address', '') if property_data else '',
            multiline=True,
            size_hint_x=0.7,
            height=dp(80),
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        address_layout.add_widget(self.address_input)
        form_layout.add_widget(address_layout)

        # Owner selection
        owners = self.api.get_all_owners() or []

        # Safely handle owners
        owner_values = []
        if owners:
            try:
                owner_values = [f"{o.get('Ownercode', 'N/A')} - {o.get('ownername', 'Unknown')}" for o in owners]
            except (KeyError, TypeError, AttributeError) as e:
                print(f"Error processing owners: {e}")

        # Add a default option if the list is empty
        if not owner_values:
            owner_values = ['No owners available']

        owner_layout = BoxLayout(size_hint_y=None, height=dp(40))
        owner_layout.add_widget(Label(
            text='Owner:',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.owner_spinner = Spinner(
            text='Select Owner',
            values=owner_values,
            size_hint_x=0.5,
            background_color=(0.95, 0.95, 0.95, 1),
            color=(0.2, 0.2, 0.2, 1)
        )

        # Safely set the spinner value if we have property data
        if property_data and property_data.get('Ownercode') and owner_values and owner_values[0] != 'No owners available':
            try:
                for val in owner_values:
                    if val.startswith(property_data['Ownercode']):
                        self.owner_spinner.text = val
                        break
            except Exception as e:
                print(f"Error setting owner spinner: {e}")

        owner_layout.add_widget(self.owner_spinner)

        # Add owner button
        add_owner_button = Button(
            text='Add Owner',
            size_hint_x=0.2,
            background_color=(0.3, 0.6, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        add_owner_button.bind(on_press=self.show_add_owner_form)
        owner_layout.add_widget(add_owner_button)

        form_layout.add_widget(owner_layout)

        # Description
        description_layout = BoxLayout(size_hint_y=None, height=dp(100))
        description_layout.add_widget(Label(
            text='Description:',
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.description_input = TextInput(
            hint_text='Property Description',
            text=property_data.get('Descriptions', '') if property_data else '',
            multiline=True,
            size_hint_x=0.7,
            height=dp(100),
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        description_layout.add_widget(self.description_input)
        form_layout.add_widget(description_layout)

        # Photo Upload
        photo_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(200))
        photo_layout.add_widget(Label(
            text='Photos:',
            size_hint_y=None,
            height=dp(30),
            color=(0.2, 0.2, 0.2, 1)
        ))

        browse_button = Button(
            text='Browse Photos',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.6, 0.3, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        browse_button.bind(on_press=self.show_file_chooser)
        photo_layout.add_widget(browse_button)

        # Selected photos
        self.photos_grid = GridLayout(cols=4, spacing=dp(5), size_hint_y=None, height=dp(130))
        photo_layout.add_widget(self.photos_grid)

        form_layout.add_widget(photo_layout)

        # Buttons layout
        buttons_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))

        # Save button
        save_button = Button(
            text='Save',
            background_color=(0.2, 0.8, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        save_button.bind(on_press=self.save)
        buttons_layout.add_widget(save_button)

        # Cancel button
        self.cancel_button = Button(
            text='Cancel',
            background_color=(0.8, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        self.cancel_button.bind(on_press=self.cancel)
        buttons_layout.add_widget(self.cancel_button)

        form_layout.add_widget(buttons_layout)

        scroll_view.add_widget(form_layout)
        self.add_widget(scroll_view)

        # Load existing photos if editing
        if property_data and self.property_code:
            self.load_existing_photos()

    def _update_rect(self, instance, value):
        """Update the background rectangle."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def load_existing_photos(self):
        """Load existing photos for the property."""
        photos = self.api.get_property_photos(self.property_code)
        if photos:
            for photo in photos:
                # Create a label to display the photo filename
                photo_label = Label(
                    text=photo.get('photofilename', 'Unknown'),
                    size_hint_y=None,
                    height=dp(30),
                    color=(0.2, 0.2, 0.2, 1)
                )
                self.photos_grid.add_widget(photo_label)

    def show_file_chooser(self, instance):
        """Show file chooser to select photos."""
        content = BoxLayout(orientation='vertical')

        file_chooser = FileChooserListView(
            path=os.path.expanduser('~'),
            filters=['*.jpg', '*.jpeg', '*.png']
        )
        content.add_widget(file_chooser)

        buttons = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))

        select_button = Button(
            text='Select',
            background_color=(0.2, 0.8, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        select_button.bind(on_press=lambda x: self.select_photos(file_chooser.selection, file_chooser_popup))
        buttons.add_widget(select_button)

        cancel_button = Button(
            text='Cancel',
            background_color=(0.8, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        cancel_button.bind(on_press=lambda x: file_chooser_popup.dismiss())
        buttons.add_widget(cancel_button)

        content.add_widget(buttons)

        file_chooser_popup = Popup(
            title='Select Photos',
            content=content,
            size_hint=(0.9, 0.9)
        )
        file_chooser_popup.open()

    def select_photos(self, selection, popup):
        """Handle selected photos."""
        if selection:
            self.selected_photos.extend(selection)

            # Update the photos grid
            self.photos_grid.clear_widgets()

            for photo_path in self.selected_photos:
                # Get just the filename
                filename = os.path.basename(photo_path)

                # Create a label to display the photo filename
                photo_label = Label(
                    text=filename,
                    size_hint_y=None,
                    height=dp(30),
                    color=(0.2, 0.2, 0.2, 1)
                )
                self.photos_grid.add_widget(photo_label)

        popup.dismiss()

    def show_add_owner_form(self, instance):
        """Show the form for adding a new owner."""
        from src.screens.owner_management import OwnerForm

        content = OwnerForm(save_callback=self.add_owner)
        self.owner_popup = Popup(
            title='Add New Owner',
            content=content,
            size_hint=(0.8, 0.8)
        )
        self.owner_popup.open()

    def add_owner(self, owner_name, owner_phone, note, owner_code=None):
        """Add a new owner to the database."""
        owner_code = self.api.add_owner(owner_name, owner_phone, note)

        if owner_code:
            self.owner_popup.dismiss()

            # Refresh the owner dropdown
            owners = self.api.get_all_owners()
            owner_values = [f"{o.get('Ownercode', 'N/A')} - {o.get('ownername', 'Unknown')}" for o in owners]
            self.owner_spinner.values = owner_values

            # Select the newly added owner
            new_owner_value = f"{owner_code} - {owner_name}"
            self.owner_spinner.text = new_owner_value

            self.show_success(f"Owner '{owner_name}' added successfully!")
        else:
            self.show_error("Failed to add owner. Please try again.")

    def save(self, instance):
        """Save the property data."""
        # Validate required fields
        if not self.property_type_spinner.text or self.property_type_spinner.text == 'Select Property Type' or self.property_type_spinner.text == 'No property types available':
            self.show_error("Property type is required.")
            return

        if not self.building_type_spinner.text or self.building_type_spinner.text == 'Select Building Type' or self.building_type_spinner.text == 'No building types available':
            self.show_error("Building type is required.")
            return

        if not self.area_input.text:
            self.show_error("Property area is required.")
            return

        if not self.owner_spinner.text or self.owner_spinner.text == 'Select Owner' or self.owner_spinner.text == 'No owners available':
            self.show_error("Owner is required.")
            return

        try:
            # Extract values from UI
            property_type_code = self.property_type_spinner.text.split(' - ')[0] if self.property_type_spinner.text not in ['Select Property Type', 'No property types available'] else None
            building_type_code = self.building_type_spinner.text.split(' - ')[0] if self.building_type_spinner.text not in ['Select Building Type', 'No building types available'] else None
            year = f"{self.year_spinner.text}-01-01" if self.year_spinner.text != 'Select Year' else None
            area = float(self.area_input.text) if self.area_input.text else None
            facade = float(self.facade_input.text) if self.facade_input.text else None
            depth = float(self.depth_input.text) if self.depth_input.text else None
            bedrooms = int(self.bedrooms_input.text) if self.bedrooms_input.text else None
            bathrooms = int(self.bathrooms_input.text) if self.bathrooms_input.text else None
            is_corner = self.corner_checkbox.active
            offer_type_code = self.offer_type_spinner.text.split(' - ')[0] if self.offer_type_spinner.text not in ['Select Offer Type', 'No offer types available'] else None
            province_code = self.province_spinner.text.split(' - ')[0] if self.province_spinner.text not in ['Select Province', 'No provinces available'] else None
            region_code = self.region_spinner.text.split(' - ')[0] if self.region_spinner.text not in ['Select Region', 'No regions available'] else None
            address = self.address_input.text
            owner_code = self.owner_spinner.text.split(' - ')[0] if self.owner_spinner.text not in ['Select Owner', 'No owners available'] else None
            description = self.description_input.text

            # Prepare property data
            property_data = {
                'Rstatetcode': property_type_code,
                'Buildtcode': building_type_code,
                'Yearmake': year,
                'Property-area': area,
                'Unitm-code': '05001',  # Default to Square Meter
                'Property-facade': facade,
                'Property-depth': depth,
                'N-of-bedrooms': bedrooms,
                'N-of-bathrooms': bathrooms,
                'Property-corner': is_corner,
                'Offer-Type-Code': offer_type_code,
                'Province-code': province_code,
                'Region-code': region_code,
                'Property-address': address,
                'Ownercode': owner_code,
                'Descriptions': description
            }

            # Call the save callback with the property data and photos
            self.save_callback(property_data, self.selected_photos, self.property_code)
        except Exception as e:
            self.show_error(f"Error saving property: {str(e)}")

    def cancel(self, instance):
        """Cancel the form and close the popup."""
        if hasattr(self.parent, 'dismiss'):
            self.parent.dismiss()

    def show_success(self, message):
        """Show a success popup."""
        popup = Popup(
            title='Success',
            content=Label(text=message, color=(0.2, 0.2, 0.2, 1)),
            size_hint=(0.7, 0.3)
        )
        popup.open()

    def show_error(self, message):
        """Show an error popup."""
        popup = Popup(
            title='Error',
            content=Label(text=message, color=(0.8, 0.2, 0.2, 1)),
            size_hint=(0.7, 0.3)
        )
        popup.open()

class PropertyManagementScreen(Screen):
    """Screen for managing properties."""

    def __init__(self, **kwargs):
        super(PropertyManagementScreen, self).__init__(**kwargs)
        self.api = get_api()

        # Set white background for the screen
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header with title and add button
        header = BoxLayout(size_hint_y=None, height=dp(50))
        header.add_widget(Label(
            text='Property Management',
            font_size=dp(24),
            color=(0.2, 0.2, 0.2, 1)
        ))

        add_button = Button(
            text='Add Property',
            size_hint_x=None,
            width=dp(120),
            background_color=(0.2, 0.8, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        add_button.bind(on_press=self.show_add_property_form)
        header.add_widget(add_button)

        self.layout.add_widget(header)

        # Properties list header
        list_header = GridLayout(cols=5, size_hint_y=None, height=dp(40))
        list_header.add_widget(Label(text='Code', bold=True, color=(0.2, 0.2, 0.2, 1)))
        list_header.add_widget(Label(text='Type', bold=True, color=(0.2, 0.2, 0.2, 1)))
        list_header.add_widget(Label(text='Area', bold=True, color=(0.2, 0.2, 0.2, 1)))
        list_header.add_widget(Label(text='Owner', bold=True, color=(0.2, 0.2, 0.2, 1)))
        list_header.add_widget(Label(text='Actions', bold=True, color=(0.2, 0.2, 0.2, 1)))
        self.layout.add_widget(list_header)

        # Properties list in a scrollview
        self.properties_container = GridLayout(cols=1, spacing=dp(2), size_hint_y=None)
        self.properties_container.bind(minimum_height=self.properties_container.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        scroll_view.add_widget(self.properties_container)
        self.layout.add_widget(scroll_view)

        # Back button with better positioning
        footer_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), padding=[0, dp(10), 0, 0])
        back_button = Button(
            text='← Back to Dashboard',
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            background_color=(0.4, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        back_button.bind(on_press=self.go_to_dashboard)
        footer_layout.add_widget(back_button)
        footer_layout.add_widget(Label())  # Spacer
        self.layout.add_widget(footer_layout)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        """Update the background rectangle."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_enter(self):
        """Load the properties list when entering the screen."""
        self.load_properties()

    def load_properties(self):
        """Load properties from the database and display them."""
        self.properties_container.clear_widgets()

        properties = self.api.get_all_properties()

        if not properties:
            self.properties_container.add_widget(
                Label(
                    text='No properties found. Click "Add Property" to create one.',
                    size_hint_y=None,
                    height=dp(40),
                    color=(0.5, 0.5, 0.5, 1)
                )
            )
            return

        for prop in properties:
            property_row = GridLayout(cols=5, size_hint_y=None, height=dp(40))

            # Ensure none of the text values are None, replace with 'N/A' if they are
            property_row.add_widget(Label(text=str(prop.get('realstatecode', 'N/A')), color=(0.2, 0.2, 0.2, 1)))
            property_row.add_widget(Label(text=str(prop.get('property_type', 'N/A')), color=(0.2, 0.2, 0.2, 1)))
            property_row.add_widget(Label(text=f"{str(prop.get('Property-area', 'N/A'))} m²", color=(0.2, 0.2, 0.2, 1)))
            property_row.add_widget(Label(text=str(prop.get('ownername', 'N/A')), color=(0.2, 0.2, 0.2, 1)))

            actions = BoxLayout(spacing=dp(5))

            edit_button = Button(
                text='Edit',
                background_color=(0.3, 0.6, 0.9, 1),
                color=(1, 1, 1, 1)
            )
            edit_button.bind(on_press=lambda x, p=prop: self.show_edit_property_form(p))
            actions.add_widget(edit_button)

            delete_button = Button(
                text='Delete',
                background_color=(0.8, 0.3, 0.3, 1),
                color=(1, 1, 1, 1)
            )
            delete_button.bind(on_press=lambda x, code=prop.get('realstatecode', ''): self.confirm_delete_property(code))
            actions.add_widget(delete_button)

            property_row.add_widget(actions)

            self.properties_container.add_widget(property_row)

    def show_add_property_form(self, instance):
        """Show the form for adding a new property."""
        content = PropertyForm(save_callback=self.add_property)
        self.popup = Popup(
            title='Add New Property',
            content=content,
            size_hint=(0.9, 0.9)
        )
        content.cancel_button.unbind(on_press=content.cancel)  # Remove old binding
        content.cancel_button.bind(on_press=lambda x: self.popup.dismiss())
        self.popup.open()

    def show_edit_property_form(self, property_data):
        """Show the form for editing a property."""
        content = PropertyForm(save_callback=self.update_property, property_data=property_data)
        self.popup = Popup(
            title='Edit Property',
            content=content,
            size_hint=(0.9, 0.9)
        )
        content.cancel_button.unbind(on_press=content.cancel)
        content.cancel_button.bind(on_press=lambda x: self.popup.dismiss())
        self.popup.open()

    def add_property(self, property_data, photos, property_code=None):
        """Add a new property to the database."""
        property_code = self.api.add_property(property_data)

        if property_code:
            # Upload photos
            if photos:
                self.upload_photos(property_code, photos)

            self.popup.dismiss()
            self.show_success(f"Property '{property_code}' added successfully!")
            self.load_properties()
        else:
            self.show_error("Failed to add property. Please try again.")

    def update_property(self, property_data, photos, property_code):
        """Update an existing property in the database."""
        if self.api.update_property(property_code, property_data):
            # Upload new photos
            if photos:
                self.upload_photos(property_code, photos)

            self.popup.dismiss()
            self.show_success(f"Property '{property_code}' updated successfully!")
            self.load_properties()
        else:
            self.show_error("Failed to update property. Please try again.")

    def upload_photos(self, property_code, photo_paths):
        """Upload photos for a property."""
        for photo_path in photo_paths:
            # Get the filename and extension
            filename = os.path.basename(photo_path)
            name, ext = os.path.splitext(filename)

            # Add to database
            storage_path = f"/photos/{self.api.company_code}/"
            self.api.add_property_photo(property_code, storage_path, name, ext)

    def confirm_delete_property(self, property_code):
        """Show confirmation dialog for deleting a property."""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text='Are you sure you want to delete this property?', color=(0.2, 0.2, 0.2, 1)))

        buttons = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))

        yes_button = Button(
            text='Yes',
            background_color=(0.8, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        yes_button.bind(on_press=lambda x: self.delete_property(property_code))
        buttons.add_widget(yes_button)

        no_button = Button(
            text='No',
            background_color=(0.6, 0.6, 0.6, 1),
            color=(1, 1, 1, 1)
        )
        no_button.bind(on_press=lambda x: self.confirm_popup.dismiss())
        buttons.add_widget(no_button)

        content.add_widget(buttons)

        self.confirm_popup = Popup(
            title='Confirm Delete',
            content=content,
            size_hint=(0.6, 0.3),
            auto_dismiss=False
        )
        self.confirm_popup.open()

    def delete_property(self, property_code):
        """Delete a property from the database."""
        if self.api.delete_property(property_code):
            self.confirm_popup.dismiss()
            self.show_success("Property deleted successfully!")
            self.load_properties()
        else:
            self.confirm_popup.dismiss()
            self.show_error("Failed to delete property. Please try again.")

    def show_success(self, message):
        """Show a success popup."""
        popup = Popup(
            title='Success',
            content=Label(text=message, color=(0.2, 0.8, 0.3, 1)),
            size_hint=(0.7, 0.3)
        )
        popup.open()

    def show_error(self, message):
        """Show an error popup."""
        popup = Popup(
            title='Error',
            content=Label(text=message, color=(0.8, 0.2, 0.2, 1)),
            size_hint=(0.7, 0.3)
        )
        popup.open()

    def go_to_dashboard(self, instance=None):
        """Navigate back to the dashboard."""
        self.manager.current = 'dashboard'
