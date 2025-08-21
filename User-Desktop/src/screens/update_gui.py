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
from kivy.lang import Builder
from datetime import datetime
import os
import shutil
import uuid
import tkinter as tk
from tkinter import filedialog
from src.models.database_api import get_api
from configs.language_manager import get_language_manager, get_text
from configs.arabic_fonts import apply_arabic_font, apply_font_to_all_widgets
from configs.language_switcher import show_language_switcher
from src.models.database_api import get_api

# Load KV file
Builder.load_file('assets/kv/update_gui.kv')

class PropertyForm(BoxLayout):
    def open_photo_chooser(self):
        """Open Windows File Explorer to add new photos."""
        try:
            # Hide the Kivy window temporarily to show native dialog
            root = tk.Tk()
            root.withdraw()  # Hide the main tkinter window
            root.wm_attributes('-topmost', 1)  # Bring dialog to front

            # Open Windows File Explorer dialog for multiple files
            file_paths = filedialog.askopenfilenames(
                title="Select Property Photos",
                filetypes=[
                    ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                    ("JPEG files", "*.jpg *.jpeg"),
                    ("PNG files", "*.png"),
                    ("Bitmap files", "*.bmp"),
                    ("All files", "*.*")
                ],
                initialdir=os.path.expanduser("~\\Pictures")  # Start from Pictures folder
            )

            root.destroy()  # Clean up tkinter

            if file_paths:
                # Add selected files to the selection, avoiding duplicates
                for file_path in file_paths:
                    if file_path not in self.selected_photos:
                        self.selected_photos.append(file_path)

                self.update_photo_gallery()

        except Exception as e:
            print(f"File chooser error: {str(e)}")  # Debug
            if hasattr(self, 'show_error'):
                self.show_error(f"Failed to open file chooser:\n{str(e)}")

    def update_photo_gallery(self):
        """Update the photo gallery UI with current selected_photos."""
        gallery = self.ids.photo_gallery
        gallery.clear_widgets()

        # Update photo count with localized text
        self.update_photo_count()

        for photo_path in self.selected_photos:
            box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(100, 100), spacing=2)
            try:
                from kivy.uix.image import Image
                img = Image(source=photo_path, size_hint=(1, 0.8), fit_mode='contain')
            except Exception:
                img = Label(text='[Image]', size_hint=(1, 0.8))
            remove_btn = Button(text='X', size_hint=(1, 0.2), background_color=(0.8,0.2,0.2,1), color=(1,1,1,1))
            remove_btn.bind(on_press=lambda btn, p=photo_path: self.remove_photo(p))
            box.add_widget(img)
            box.add_widget(remove_btn)
            gallery.add_widget(box)

    def remove_photo(self, photo_path):
        """Remove a photo from the gallery and selection."""
        if photo_path in self.selected_photos:
            self.selected_photos.remove(photo_path)

            # If this is an existing photo (either starts with data/realstateimages/ or is in existing_photos list),
            # mark it for deletion from database
            is_existing = (photo_path.startswith("data/realstateimages") or
                          (hasattr(self, 'existing_photos') and photo_path in self.existing_photos))

            if is_existing and hasattr(self, 'property_code') and self.property_code:
                if not hasattr(self, 'photos_to_delete'):
                    self.photos_to_delete = []
                self.photos_to_delete.append(photo_path)

            self.update_photo_gallery()
    def on_kv_post(self, base_widget):
        # Set API
        self.api = get_api()

        # Initialize language manager
        self.language_manager = get_language_manager()
        self.language_manager.register_observer(self)

        # Populate dropdown values
        self.property_type_values = [f"{x['code']} - {x['name']}" for x in self.api.get_property_types() or []]
        self.building_type_values = [f"{x['code']} - {x['name']}" for x in self.api.get_building_types() or []]
        self.year_values = [str(y) for y in range(1980, datetime.now().year + 1)]
        self.offer_type_values = [f"{x['code']} - {x['name']}" for x in self.api.get_offer_types() or []]
        self.province_values = [f"{x['code']} - {x['name']}" for x in self.api.get_provinces() or []]
        self.region_values = []  # Will be set when province is selected
        self.owner_values = [f"{x['Ownercode']} - {x['ownername']}" for x in self.api.get_all_owners() or []]
        self.currency_values = ['IQD - Iraqi Dinar', 'USD - US Dollar', 'EUR - Euro']  # Example, adjust as needed
        self.unit_values = [f"{x['code']} - {x['name']}" for x in self.api.get_unit_measures() or []]

        # Bind all widget references to their ids for kv linkage
        self.property_type_spinner = self.ids.property_type
        self.building_type_spinner = self.ids.building_type
        self.year_spinner = self.ids.year_spinner
        self.area_input = self.ids.area
        self.facade_input = self.ids.facade
        self.depth_input = self.ids.depth
        self.bedrooms_input = self.ids.bedrooms
        self.bathrooms_input = self.ids.bathrooms
        self.corner_checkbox = self.ids.corner
        self.offer_type_spinner = self.ids.offer_type
        self.province_spinner = self.ids.province
        self.region_spinner = self.ids.region
        self.address_input = self.ids.address
        self.owner_spinner = self.ids.owner
        self.description_input = self.ids.description
        # New fields for updated DB
        self.floors_input = self.ids.floors
        self.price_input = self.ids.price
        self.currency_spinner = self.ids.currency
        self.unit_spinner = self.ids.unit
        # Photo-related widgets
        self.photo_count = self.ids.photo_count
        # Optionally, connect save/cancel buttons if needed
        if 'save_btn' in self.ids:
            self.ids.save_btn.bind(on_press=self.save)
        if 'cancel_btn' in self.ids:
            self.ids.cancel_btn.bind(on_press=self.cancel)
        # Always define selected_photos and property_code to avoid attribute errors
        self.selected_photos = []
        self.existing_photos = []  # Track existing photos separately from new ones
        self.photos_to_delete = []  # Track photos marked for deletion
        self.property_code = None

        # Update texts after initialization
        Clock.schedule_once(lambda dt: self.update_texts(), 0.1)

        # Populate fields if editing - delay this to ensure UI is ready
        if self.property_data:
            Clock.schedule_once(self._delayed_populate_fields, 0.1)
        else:
            # Always update photo gallery on form open
            self.update_photo_gallery()

    def _delayed_populate_fields(self, dt):
        """Populate fields after a small delay to ensure UI is ready."""
        self.populate_fields()

    def update_texts(self):
        """Update all text elements in the form with current language"""
        try:
            # Update form title
            if hasattr(self.ids, 'form_title_label'):
                self.ids.form_title_label.text = get_text('property_form', 'Property Form')

            # Update all field labels
            label_mappings = {
                'property_type_label': ('property_type', 'Property Type:'),
                'building_type_label': ('building_type', 'Building Type:'),
                'year_built_label': ('year_construction', 'Year Built:'),
                'area_label': ('area', 'Area:'),
                'facade_label': ('facade', 'Facade:'),
                'depth_label': ('depth', 'Depth:'),
                'bedrooms_label': ('bedrooms', 'Bedrooms:'),
                'bathrooms_label': ('bathrooms', 'Bathrooms:'),
                'corner_label': ('is_corner_property', 'Is Corner Property:'),
                'offer_type_label': ('offer_type', 'Offer Type:'),
                'province_label': ('governorate', 'Province:'),
                'region_label': ('neighborhood', 'Region:'),
                'address_label': ('address', 'Address:'),
                'owner_label': ('owner', 'Owner:'),
                'description_label': ('notes', 'Description:'),
                'floors_label': ('floors', 'Floors:'),
                'price_label': ('price', 'Price:'),
                'currency_label': ('offer_type', 'Currency:'),  # Using existing key
                'unit_label': ('unit_measurement', 'Unit:'),
                'photos_label': ('photos', 'Photos:')
            }

            for widget_id, (text_key, fallback) in label_mappings.items():
                if hasattr(self.ids, widget_id):
                    widget = getattr(self.ids, widget_id)
                    widget.text = get_text(text_key, fallback)

            # Update spinner texts
            spinner_mappings = {
                'property_type': ('select_property_type', 'Select Property Type'),
                'building_type': ('select_building_type', 'Select Building Type'),
                'year_spinner': ('select_year', 'Select Year'),
                'offer_type': ('select_offer_type', 'Select Offer Type'),
                'province': ('select_province', 'Select Province'),
                'region': ('select_region', 'Select Region'),
                'owner': ('select_owner', 'Select Owner'),
                'currency': ('select_currency', 'Select Currency'),
                'unit': ('select_unit', 'Select Unit')
            }

            for widget_id, (text_key, fallback) in spinner_mappings.items():
                if hasattr(self.ids, widget_id):
                    widget = getattr(self.ids, widget_id)
                    widget.text = get_text(text_key, fallback)

            # Update hint texts for TextInputs
            hint_mappings = {
                'area': ('property_area_hint', 'Property Area'),
                'facade': ('facade_length_hint', 'Facade Length'),
                'depth': ('property_depth_hint', 'Property Depth'),
                'bedrooms': ('num_bedrooms_hint', 'Number of Bedrooms'),
                'bathrooms': ('num_bathrooms_hint', 'Number of Bathrooms'),
                'address': ('property_address_hint', 'Property Address'),
                'description': ('property_description_hint', 'Property Description/Notes'),
                'floors': ('num_floors_hint', 'Number of Floors'),
                'price': ('property_price_hint', 'Property Price')
            }

            for widget_id, (text_key, fallback) in hint_mappings.items():
                if hasattr(self.ids, widget_id):
                    widget = getattr(self.ids, widget_id)
                    widget.hint_text = get_text(text_key, fallback)

            # Update buttons
            if hasattr(self.ids, 'save_btn'):
                self.ids.save_btn.text = get_text('save', 'Save')
            if hasattr(self.ids, 'cancel_btn'):
                self.ids.cancel_btn.text = get_text('cancel', 'Cancel')
            if hasattr(self.ids, 'add_photo_btn'):
                self.ids.add_photo_btn.text = get_text('add_photos', 'Add Photos')

            # Update photo count
            self.update_photo_count()

            # Apply fonts after text updates
            self.apply_fonts()

        except Exception as e:
            print(f"Error updating texts in PropertyForm: {e}")

    def update_photo_count(self):
        """Update photo count text with proper localization"""
        try:
            if hasattr(self.ids, 'photo_count'):
                count = len(self.selected_photos) if hasattr(self, 'selected_photos') else 0
                if count == 0:
                    self.ids.photo_count.text = get_text('no_photos_selected', 'No photos selected')
                elif count == 1:
                    self.ids.photo_count.text = f"1 {get_text('photo_selected', 'photo selected')}"
                else:
                    self.ids.photo_count.text = f"{count} {get_text('photos_selected', 'photos selected')}"
        except Exception as e:
            print(f"Error updating photo count: {e}")

    def apply_fonts(self):
        """Apply Arabic fonts to all text widgets"""
        try:
            current_lang = self.language_manager.get_current_language() if hasattr(self, 'language_manager') else 'en'

            if current_lang == 'ar':
                for widget in self.walk():
                    if hasattr(widget, 'text') and widget.text:
                        apply_arabic_font(widget, widget.text)
                    if hasattr(widget, 'hint_text') and widget.hint_text:
                        apply_arabic_font(widget, widget.hint_text)

                    # Special handling for Spinners
                    from kivy.uix.spinner import Spinner
                    if isinstance(widget, Spinner):
                        apply_arabic_font(widget, widget.text)
                        # Apply font to all values in the spinner
                        for value in widget.values:
                            if any('\u0600' <= char <= '\u06FF' for char in value):
                                widget.font_name = 'ArabicFont'
                                break
        except Exception as e:
            print(f"Error applying fonts in PropertyForm: {e}")

    def on_language_changed(self):
        """Called when language is changed"""
        try:
            self.update_texts()
        except Exception as e:
            print(f"Error handling language change in PropertyForm: {e}")

    from kivy.properties import ObjectProperty, ListProperty
    save_callback = ObjectProperty(None)
    property_data = ObjectProperty(None)
    photo_count = ObjectProperty(None)
    property_type_values = ListProperty([])
    building_type_values = ListProperty([])
    year_values = ListProperty([])
    offer_type_values = ListProperty([])
    province_values = ListProperty([])
    region_values = ListProperty([])
    owner_values = ListProperty([])
    currency_values = ListProperty([])
    unit_values = ListProperty([])
    """Form for adding or editing a property."""

    def save(self, instance):
        """Save the property data."""
        # Validate required fields
        if not self.property_type_spinner.text or self.property_type_spinner.text == 'Select Property Type' or self.property_type_spinner.text == 'No property types available':
            self.show_error(get_text('property_type_required', 'Property type is required.'))
            return

        if not self.building_type_spinner.text or self.building_type_spinner.text == 'Select Building Type' or self.building_type_spinner.text == 'No building types available':
            self.show_error(get_text('building_type_required', 'Building type is required.'))
            return

        if not self.area_input.text:
            self.show_error(get_text('area_required', 'Property area is required.'))
            return

        if not self.owner_spinner.text or self.owner_spinner.text == 'Select Owner' or self.owner_spinner.text == 'No owners available':
            self.show_error(get_text('owner_required', 'Owner is required.'))
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
            floors = int(self.floors_input.text) if self.floors_input.text else None
            price = float(self.price_input.text) if self.price_input.text else None
            currency_code = self.currency_spinner.text.split(' - ')[0] if self.currency_spinner.text and self.currency_spinner.text != 'Select Currency' else None
            unit_code = self.unit_spinner.text.split(' - ')[0] if self.unit_spinner.text and self.unit_spinner.text != 'Select Unit' else None

            # Prepare property data
            property_data = {
                'Rstatetcode': property_type_code,
                'Buildtcode': building_type_code,
                'Yearmake': year,
                'Property-area': area,
                'Unitm-code': unit_code,
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
                'Descriptions': description,
                'Property-floors': floors,
                'Property-price': price,
                'Property-currency': currency_code
            }

            # Call the save callback with the property data and photos
            photos_to_delete = getattr(self, 'photos_to_delete', [])
            self.save_callback(property_data, self.selected_photos, self.property_code, photos_to_delete)
        except Exception as e:
            self.show_error(f"Error saving property: {str(e)}")


    def populate_fields(self):
        """Populate form fields with property_data for editing, including photos."""
        data = self.property_data
        # Set property_code if available
        if data.get('realstatecode'):
            self.property_code = data['realstatecode']
        # Set spinner/text fields, handle None values
        if data.get('Rstatetcode') and self.property_type_spinner.values:
            match = next((v for v in self.property_type_spinner.values if v.startswith(str(data['Rstatetcode']))), None)
            if match:
                self.property_type_spinner.text = match
        if data.get('Buildtcode') and self.building_type_spinner.values:
            match = next((v for v in self.building_type_spinner.values if v.startswith(str(data['Buildtcode']))), None)
            if match:
                self.building_type_spinner.text = match
        if data.get('Yearmake'):
            # Expecting format 'YYYY-MM-DD'
            self.year_spinner.text = str(data['Yearmake'])[:4]
        self.area_input.text = str(data.get('Property-area', '') or '')
        self.facade_input.text = str(data.get('Property-facade', '') or '')
        self.depth_input.text = str(data.get('Property-depth', '') or '')
        self.bedrooms_input.text = str(data.get('N-of-bedrooms', '') or '')
        self.bathrooms_input.text = str(data.get('N-of-bathrooms', '') or '')
        self.corner_checkbox.active = bool(data.get('Property-corner', False))
        if data.get('Offer-Type-Code') and self.offer_type_spinner.values:
            match = next((v for v in self.offer_type_spinner.values if v.startswith(str(data['Offer-Type-Code']))), None)
            if match:
                self.offer_type_spinner.text = match
        if data.get('Province-code') and self.province_spinner.values:
            match = next((v for v in self.province_spinner.values if v.startswith(str(data['Province-code']))), None)
            if match:
                self.province_spinner.text = match
        if data.get('Region-code') and self.region_spinner.values:
            match = next((v for v in self.region_spinner.values if v.startswith(str(data['Region-code']))), None)
            if match:
                self.region_spinner.text = match
        self.address_input.text = str(data.get('Property-address', '') or '')
        if data.get('Ownercode') and self.owner_spinner.values:
            match = next((v for v in self.owner_spinner.values if v.startswith(str(data['Ownercode']))), None)
            if match:
                self.owner_spinner.text = match
        self.description_input.text = str(data.get('Descriptions', '') or '')
        self.floors_input.text = str(data.get('Property-floors', '') or '')
        self.price_input.text = str(data.get('Property-price', '') or '')
        if data.get('Property-currency') and self.currency_spinner.values:
            match = next((v for v in self.currency_spinner.values if v.startswith(str(data['Property-currency']))), None)
            if match:
                self.currency_spinner.text = match
        if data.get('Unitm-code') and self.unit_spinner.values:
            match = next((v for v in self.unit_spinner.values if v.startswith(str(data['Unitm-code']))), None)
            if match:
                self.unit_spinner.text = match

        # Load and display existing property photos if editing
        if self.property_code:
            # Only load from DB if not already loaded
            if not self.selected_photos and not self.existing_photos:
                try:
                    photos = self.api.get_property_photos(self.property_code)
                    for photo in photos or []:
                        # Construct the full path to the photo
                        storage_path = photo.get('Storagepath', '')
                        filename = photo.get('photofilename', '')

                        # The filename should already include the extension
                        if filename:
                            path = os.path.join(storage_path, filename)
                            if os.path.exists(path):
                                self.selected_photos.append(path)
                                self.existing_photos.append(path)  # Track as existing
                except Exception as e:
                    print(f"Error loading property photos: {e}")
            self.update_photo_gallery()
    def show_add_owner_form(self, instance):
        """Show the form for adding a new owner."""
        from src.screens.owner_management import OwnerForm

        content = OwnerForm(save_callback=self.add_owner)
        self.owner_popup = Popup(
            title='Add New Owner',
            content=content,
            size_hint=(0.8, 0.8)
        )
        # Bind the cancel button to dismiss the popup

    def add_owner(self, owner_name, owner_phone, note, owner_code=None):
        """Add a new owner to the database."""
        owner_code = self.api.add_owner(owner_name, owner_phone, note)
        # You may want to refresh the owner spinner or update the UI here after adding the owner.

    def cancel(self, instance):
        """Cancel the form and close the popup."""
        if hasattr(self.parent, 'dismiss'):
            self.parent.dismiss()

    def show_success(self, message):
        """Show a success popup."""
        content = Label(text=message, color=(0.2, 0.8, 0.3, 1), text_size=(None, None), halign='center')
        apply_arabic_font(content, message)
        popup = Popup(
            title=get_text('success', 'Success'),
            content=content,
            size_hint=(0.7, 0.3)
        )
        popup.open()

    def show_error(self, message):
        """Show an error popup."""
        content = Label(text=message, color=(0.8, 0.2, 0.2, 1), text_size=(None, None), halign='center')
        apply_arabic_font(content, message)
        popup = Popup(
            title=get_text('error', 'Error'),
            content=content,
            size_hint=(0.7, 0.3)
        )
        popup.open()

    def on_province_selected(self, spinner, text):
        """Handle province selection and update region dropdown."""
        # Ignore default/placeholder text
        if not hasattr(self, 'region_spinner'):
            print("Warning: region_spinner not found in PropertyForm")
            return

        try:
            # Extract province_code from the spinner text (format: "code - name")
            province_code = text.split(' - ')[0] if text and ' - ' in text else text

            # Get cities for the selected province
            cities = self.api.get_cities_by_province(province_code)

            if cities:
                # Format city options (code - name)
                city_values = [f"{c.get('code', 'N/A')} - {c.get('name', 'Unknown')}" for c in cities]
                self.region_spinner.values = city_values
                self.region_spinner.text = 'Select Region'
            else:
                # No cities found for this province
                self.region_spinner.values = ['No regions available']
                self.region_spinner.text = 'No regions available'

        except Exception as e:
            print(f"Error updating region dropdown: {e}")
            # Set error state if spinner exists
            if hasattr(self, 'region_spinner'):
                self.region_spinner.values = ['Error loading regions']
                self.region_spinner.text = 'Error loading regions'

class UpdateGUIScreen(Screen):
    """Screen for managing properties."""

    def __init__(self, **kwargs):
        super(UpdateGUIScreen, self).__init__(**kwargs)
        self.api = get_api()
        self.properties_container = None
        self.language_manager = get_language_manager()
        # Register for language change notifications
        self.language_manager.register_observer(self)
        # Bind to on_enter to setup localization
        self.bind(on_enter=self.setup_localization)

    # Layout is now managed by the Kivy file

    def on_enter(self):
        """Load the properties list when entering the screen."""
        # Get the properties container from the kv file
        self.properties_container = self.ids.properties_container
        self.load_properties()

    def setup_localization(self, *args):
        """Setup localization and Arabic fonts"""
        try:
            self.update_texts()
            self.apply_fonts()
        except Exception as e:
            print(f"Error setting up localization in update screen: {e}")

    def show_language_switcher(self):
        """Show language switcher popup"""
        from configs.language_switcher import show_language_switcher
        show_language_switcher()

    def update_texts(self):
        """Update all text widgets with current language"""
        try:
            # Define the mapping of IDs to translation keys
            text_mappings = {
                'header_label': 'property_management',
                'language_btn': 'language',
                'code_header': 'code',
                'type_header': 'type',
                'area_header': 'area',
                'owner_header': 'owner_name',
                'actions_header': 'actions',
                'back_btn': 'back_to_main'
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

        except Exception as e:
            print(f"Error updating texts: {e}")

    def apply_fonts(self):
        """Apply Arabic fonts to all text widgets if Arabic is selected"""
        if self.language_manager.current_language == 'ar':
            try:
                for widget in self.walk():
                    if hasattr(widget, 'text') and widget.text:
                        apply_arabic_font(widget, widget.text)
            except Exception as e:
                print(f"Error applying fonts in update screen: {e}")

    def on_language_changed(self):
        """Called when language is changed"""
        try:
            self.setup_localization()
            # Reload properties to update Edit/Delete button texts
            if hasattr(self, 'properties_container') and self.properties_container is not None:
                self.load_properties()
        except Exception as e:
            print(f"Error handling language change in update screen: {e}")

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
                text=get_text('edit', 'Edit'),
                background_color=(0.3, 0.6, 0.9, 1),
                color=(1, 1, 1, 1)
            )
            # Ensure Arabic font is applied when language is Arabic
            apply_arabic_font(edit_button, edit_button.text)
            edit_button.bind(on_press=lambda x, p=prop: self.show_edit_property_form(p))
            actions.add_widget(edit_button)

            delete_button = Button(
                text=get_text('delete', 'Delete'),
                background_color=(0.8, 0.3, 0.3, 1),
                color=(1, 1, 1, 1)
            )
            # Ensure Arabic font is applied when language is Arabic
            apply_arabic_font(delete_button, delete_button.text)
            delete_button.bind(on_press=lambda x, code=prop.get('realstatecode', ''): self.confirm_delete_property(code))
            actions.add_widget(delete_button)

            property_row.add_widget(actions)

            self.properties_container.add_widget(property_row)

    def show_edit_property_form(self, property_data):
        """Show the form for editing a property."""
        # Get the full property data from the database
        full_property_data = self.api.get_property_by_code(property_data.get('realstatecode'))

        if not full_property_data:
            self.show_error(get_text('property_not_found', 'Property not found in database.'))
            return

        content = PropertyForm(save_callback=self.update_property, property_data=full_property_data)
        popup_title = get_text( 'Edit Property')
        self.popup = Popup(
            title=popup_title,
            content=content,
            size_hint=(0.9, 0.9)
        )
        # Apply Arabic font to popup title if needed
        apply_arabic_font(self.popup, popup_title)
        # Bind the cancel button to close the popup
        if hasattr(content.ids, 'cancel_btn'):
            content.ids.cancel_btn.bind(on_press=lambda x: self.popup.dismiss())
        self.popup.open()

    def update_property(self, property_data, photos, property_code, photos_to_delete=None):
        """Update an existing property in the database."""
        if self.api.update_property(property_code, property_data):
            # Handle photo deletions first
            if photos_to_delete:
                for photo_path in photos_to_delete:
                    # Extract filename from path
                    import os
                    filename = os.path.basename(photo_path)
                    success = self.api.delete_property_photo(property_code, filename)
                    if not success:
                        self.show_error(f"Failed to delete photo {filename}")

            # Filter out existing photos - only upload truly new ones
            new_photos = []
            existing_photos = getattr(self, 'existing_photos', [])

            for photo in photos:
                if photo not in existing_photos:
                    new_photos.append(photo)

            # Upload only new photos
            if new_photos:
                self.upload_photos(property_code, new_photos)

            self.popup.dismiss()
            self.show_success(get_text('property_updated', 'Property updated successfully!').replace('{code}', property_code))
            self.load_properties()
        else:
            self.show_error(get_text('update_failed', 'Failed to update property. Please try again.'))

    def upload_photos(self, property_code, photo_paths):
        """Upload photos for a property (only new photos, not existing ones)."""
        import shutil
        import uuid
        from pathlib import Path

        # Create storage directory for this property
        storage_dir = Path("data/realstateimages") / property_code
        storage_dir.mkdir(parents=True, exist_ok=True)

        for photo_path in photo_paths:
            try:
                # Skip if this is already an existing photo in the storage directory
                if photo_path.startswith(str(storage_dir)):
                    continue  # This is already an existing photo, skip it

                # Generate unique filename to avoid conflicts
                original_file = Path(photo_path)
                file_extension = original_file.suffix.lower()
                unique_filename = f"{uuid.uuid4().hex[:8]}_{original_file.stem}{file_extension}"

                # Copy file to storage directory
                destination = storage_dir / unique_filename
                # Copy file to storage directory
                destination = storage_dir / unique_filename
                shutil.copy2(photo_path, destination)

                # Add to database
                success = self.api.add_property_photo(
                    property_code=property_code,
                    file_path=str(storage_dir),
                    photo_filename=unique_filename,
                    photo_extension=file_extension
                )

                if not success:
                    self.show_error(f"Failed to save photo metadata for {original_file.name}")

            except Exception as e:
                self.show_error(f"Failed to upload photo {Path(photo_path).name}: {str(e)}")

    def confirm_delete_property(self, property_code):
        """Show confirmation dialog for deleting a property."""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Create localized confirmation message
        message_text = get_text('confirm_delete_message', 'Are you sure you want to delete this property?\nThis will also delete all associated photos.')
        message_label = Label(
            text=message_text,
            color=(0.2, 0.2, 0.2, 1),
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        # Apply Arabic font to the message
        apply_arabic_font(message_label, message_text)
        content.add_widget(message_label)

        buttons = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))

        # Localized Yes button
        yes_text = get_text('yes', 'Yes')
        yes_button = Button(
            text=yes_text,
            background_color=(0.8, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        apply_arabic_font(yes_button, yes_text)
        yes_button.bind(on_press=lambda x: self.delete_property(property_code))
        buttons.add_widget(yes_button)

        # Localized No button
        no_text = get_text('no', 'No')
        no_button = Button(
            text=no_text,
            background_color=(0.0, 0.45, 0.85, 1),
            color=(1, 1, 1, 1)
        )
        apply_arabic_font(no_button, no_text)
        no_button.bind(on_press=lambda x: self.delete_popup.dismiss())
        buttons.add_widget(no_button)

        content.add_widget(buttons)

        # Create popup with localized title and white background
        popup_title = get_text('Confirm Delete?')
        self.delete_popup = Popup(
            title=popup_title,
            content=content,
            size_hint=(0.6, 0.4),
            background='',  # Remove default background
            background_color=(1, 1, 1, 1),  # Set white background
            separator_color=(0.2, 0.6, 0.8, 1),  # Optional: custom separator color
            title_color=(0, 0, 0, 1)  # Set title color to black
        )
        # Apply Arabic font to popup title
        apply_arabic_font(self.delete_popup, popup_title)
        self.delete_popup.open()

    def delete_property(self, property_code):
        """Delete a property and all its photos from database and filesystem."""
        if self.api.delete_property(property_code):
            self.delete_popup.dismiss()
            self.show_success(get_text('property_deleted', 'Property and all its photos deleted successfully!').replace('{code}', property_code))
            self.load_properties()
        else:
            self.show_error(get_text('delete_failed', 'Failed to delete property. Please try again.'))

    def show_success(self, message):
        """Show a success popup."""
        content = Label(text=message, color=(0.2, 0.8, 0.3, 1), text_size=(None, None), halign='center')
        apply_arabic_font(content, message)
        popup = Popup(
            title=get_text('success', 'Success'),
            content=content,
            size_hint=(0.7, 0.3)
        )
        popup.open()

    def show_error(self, message):
        """Show an error popup."""
        content = Label(text=message, color=(0.8, 0.2, 0.2, 1), text_size=(None, None), halign='center')
        apply_arabic_font(content, message)
        popup = Popup(
            title=get_text('error', 'Error'),
            content=content,
            size_hint=(0.7, 0.3)
        )
        popup.open()

    def go_to_main_gui(self, instance=None):
        """Navigate back to the main GUI."""
        self.manager.current = 'main_gui'
