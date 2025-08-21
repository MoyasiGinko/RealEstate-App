from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp
from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog
from src.models.database_api import get_api
from configs.language_manager import get_language_manager, get_text
from configs.arabic_fonts import apply_arabic_font
from configs.language_switcher import show_language_switcher

Builder.load_file('assets/kv/insert_gui.kv')

class InsertScreen(Screen):
	property_code = ObjectProperty(None)
	property_type = ObjectProperty(None)
	year_construction = ObjectProperty(None)
	building_type = ObjectProperty(None)
	unit_measurement = ObjectProperty(None)
	facade = ObjectProperty(None)
	depth = ObjectProperty(None)
	floors = ObjectProperty(None)
	area = ObjectProperty(None)
	bedrooms = ObjectProperty(None)
	bathrooms = ObjectProperty(None)
	corner_yes = ObjectProperty(None)
	corner_no = ObjectProperty(None)
	offer_type = ObjectProperty(None)
	governorate = ObjectProperty(None)
	region = ObjectProperty(None)
	price = ObjectProperty(None)
	price_dinar = ObjectProperty(None)
	price_dollar = ObjectProperty(None)
	property_owner = ObjectProperty(None)
	owner_search = ObjectProperty(None)
	add_photo = ObjectProperty(None)
	photo_count = ObjectProperty(None)
	photo_gallery = ObjectProperty(None)
	notes = ObjectProperty(None)
	save_btn = ObjectProperty(None)
	new_btn = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(InsertScreen, self).__init__(**kwargs)
		self.api = get_api()
		self.selected_photos = []
		self.owners_data = []
		self.provinces_data = []
		self.regions_data = []
		self.language_manager = get_language_manager()
		# Register for language change notifications
		self.language_manager.register_observer(self)
		# Bind to on_enter to setup localization
		self.bind(on_enter=self.setup_localization)

	def on_enter(self):
		"""Called when the screen is entered"""
		# Load data from database for dropdowns
		self.load_property_types()
		self.load_building_types()
		self.load_offer_types()
		self.load_unit_measurements()
		self.load_provinces()
		self.load_owners()

		# Set current year as default
		if hasattr(self, 'year_construction') and self.year_construction:
			current_year = str(datetime.now().year)
			self.year_construction.text = current_year

	def setup_localization(self, *args):
		"""Setup localization and Arabic fonts"""
		try:
			self.update_texts()
			self.apply_fonts()
		except Exception as e:
			print(f"Error setting up localization in insert screen: {e}")

	def update_texts(self):
		"""Update all text widgets with current language"""
		try:
			# Define the mapping of IDs to translation keys
			text_mappings = {
				'header_label': 'add_new_property',
				'property_code_label': 'property_code',
				'property_type_label': 'property_type',
				'year_construction_label': 'year_construction',
				'building_type_label': 'building_type',
				'unit_measurement_label': 'unit_measurement',
				'facade_label': 'facade',
				'depth_label': 'depth',
				'floors_label': 'floors',
				'area_label': 'area',
				'bedrooms_label': 'bedrooms',
				'bathrooms_label': 'bathrooms',
				'corner_label': 'corner',
				'yes_label': 'yes',
				'no_label': 'no',
				'offer_type_label': 'offer_type',
				'governorate_label': 'province',
				'region_label': 'region',
				'address_label': 'address',
				'price_label': 'price',
				'owner_label': 'owner',
				'photos_label': 'photos',
				'notes_label': 'notes',
				'required_fields_label': 'required_fields',
				'back_btn': 'back',
				'new_btn': 'clear_form',
				'save_btn': 'save_property'
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
				print(f"Error applying fonts in insert screen: {e}")

	def on_language_changed(self):
		"""Called when language is changed"""
		try:
			self.setup_localization()
		except Exception as e:
			print(f"Error handling language change in insert screen: {e}")

	def show_language_switcher(self):
		"""Show the language switcher popup"""
		show_language_switcher()

	def load_property_types(self):
		"""Load property types from database into spinner"""
		if hasattr(self, 'property_type') and self.property_type:
			property_types = self.api.get_property_types() or []
			values = [pt['name'] for pt in property_types if 'name' in pt] if property_types else []
			if not values:
				values = ['No property types available']
			self.property_type.values = values

	def load_building_types(self):
		"""Load building types from database into spinner"""
		if hasattr(self, 'building_type') and self.building_type:
			building_types = self.api.get_building_types() or []
			values = [bt['name'] for bt in building_types if 'name' in bt] if building_types else []
			if not values:
				values = ['No building types available']
			self.building_type.values = values

	def load_unit_measurements(self):
		"""Load unit measurements from database into spinner"""
		if hasattr(self, 'unit_measurement') and self.unit_measurement:
			unit_types = self.api.get_unit_measures() or []
			values = [ut['name'] for ut in unit_types if 'name' in ut] if unit_types else []
			if not values:
				values = ['m²', 'ft²']
			self.unit_measurement.values = values

	def load_offer_types(self):
		"""Load offer types from database into spinner"""
		if hasattr(self, 'offer_type') and self.offer_type:
			offer_types = self.api.get_offer_types() or []
			values = [ot['name'] for ot in offer_types if 'name' in ot] if offer_types else []
			if not values:
				values = ['Sale', 'Rent', 'Lease']
			self.offer_type.values = values

	def load_provinces(self):
		"""Load provinces from database into spinner"""
		if hasattr(self, 'governorate') and self.governorate:
			provinces = self.api.get_provinces() or []
			values = [f"{p['name']} ({p['code']})" for p in provinces if 'name' in p and 'code' in p] if provinces else []
			if not values:
				values = ['No provinces available']
			self.governorate.values = values
			# Store provinces data for later use
			self.provinces_data = provinces

	def on_province_selected(self, selected_text):
		"""Load regions when a province is selected"""
		if not selected_text or selected_text in ['Select Province', 'No provinces available']:
			# Clear regions
			if hasattr(self, 'region') and self.region:
				self.region.values = []
				self.region.text = 'Select Region'
			return

		# Extract province code from selected text
		province_code = None
		if hasattr(self, 'provinces_data'):
			for province in self.provinces_data:
				if f"{province['name']} ({province['code']})" == selected_text:
					province_code = province['code']
					break

		if province_code:
			# Load regions for this province
			regions = self.api.get_regions_by_province(province_code) or []
			if hasattr(self, 'region') and self.region:
				values = [f"{r['name']} ({r['code']})" for r in regions if 'name' in r and 'code' in r] if regions else []
				if not values:
					values = ['No regions available']
				self.region.values = values
				self.region.text = 'Select Region' if values != ['No regions available'] else 'No regions available'
				# Store regions data for later use
				self.regions_data = regions

	def load_owners(self):
		"""Load owners from database and populate the spinner"""
		self.owners_data = self.api.get_all_owners() or []
		self.filtered_owners = self.owners_data.copy()
		self.update_owner_spinner()

	def update_owner_spinner(self):
		if hasattr(self, 'property_owner') and self.property_owner:
			# Show both name and code for clarity
			values = [f"{o['ownername']} ({o['Ownercode']})" for o in self.filtered_owners if 'ownername' in o and 'Ownercode' in o]
			if values:
				self.property_owner.values = values
				self.property_owner.text = values[0]
			else:
				self.property_owner.values = ['No owners found']
				self.property_owner.text = 'No owners found'

	def filter_owners(self, search_text):
		"""Filter owners by name or code and update spinner immediately"""
		search = search_text.lower().strip()
		if not search:
			self.filtered_owners = self.owners_data.copy()
		else:
			self.filtered_owners = [o for o in self.owners_data if search in o.get('ownername','').lower() or search in o.get('Ownercode','').lower()]
		self.update_owner_spinner()
		# Optionally, close and reopen the spinner to refresh dropdown (if open)
		if self.property_owner.is_open:
			self.property_owner.is_open = False
			self.property_owner.is_open = True

	def on_save(self, instance=None):
		# Validate required fields
		if not self.property_type.text or self.property_type.text == 'Select Type':
			self.show_error("Please select a Property Type")
			return

		if not self.building_type.text or self.building_type.text == 'Select Building Type':
			self.show_error("Please select a Building Type")
			return

		if not self.governorate.text or self.governorate.text == 'Select Province':
			self.show_error("Please select a Province")
			return

		if not self.region.text or self.region.text == 'Select Region':
			self.show_error("Please select a Region")
			return

		if not self.property_owner.text or self.property_owner.text == 'Select Owner' or not self.filtered_owners:
			self.show_error("Please select a Property Owner or add a new one.")
			return

		# Extract owner code from spinner value
		selected_owner = self.property_owner.text
		owner_code = None
		for o in self.filtered_owners:
			label = f"{o['ownername']} ({o['Ownercode']})"
			if label == selected_owner:
				owner_code = o['Ownercode']
				break
		if not owner_code:
			self.show_error("Selected owner not found. Please try again.")
			return

		# Extract province and region codes
		province_code = self.get_code_from_selection(self.governorate.text, self.provinces_data)
		region_code = self.get_code_from_selection(self.region.text, self.regions_data)

		if not province_code:
			self.show_error("Invalid province selection. Please try again.")
			return

		if not region_code:
			self.show_error("Invalid region selection. Please try again.")
			return

		# Collect data from form
		try:
			# Get database codes instead of display names for dropdown values
			property_type_code = self.get_code_for_name('property_types', self.property_type.text)
			building_type_code = self.get_code_for_name('building_types', self.building_type.text)
			offer_type_code = self.get_code_for_name('offer_types', self.offer_type.text)
			unit_code = self.get_code_for_name('unit_measures', self.unit_measurement.text)

			data = {
				'realstatecode': self.property_code.text if self.property_code.text else self.api.generate_property_code(),
				'Rstatetcode': property_type_code,
				'Yearmake': self.year_construction.text,
				'Buildtcode': building_type_code,
				'Unitm-code': unit_code,
				'Property-facade': self.facade.text,
				'Property-depth': self.depth.text,
				'Property-floors': self.floors.text,
				'Property-area': self.area.text,
				'N-of-bedrooms': self.bedrooms.text,
				'N-of-bathrooms': self.bathrooms.text,
				'Property-corner': 'Y' if self.corner_yes.active else 'N',
				'Offer-Type-Code': offer_type_code,
				'Province-code': province_code,
				'Region-code': region_code,
				'Property-address': self.address.text,
				'Property-price': self.price.text,
				'Property-currency': 'Dinar' if self.price_dinar.state == 'down' else 'Dollar',
				'Ownercode': owner_code,
				'Descriptions': self.notes.text
			}

			# Add property to database
			property_code = self.api.add_property(data)

			if property_code:
				# Upload photos if any
				if self.selected_photos:
					self.upload_photos(property_code, self.selected_photos)

				self.show_success(f"Property '{property_code}' added successfully!")
				self.on_new()  # Clear the form
			else:
				self.show_error("Failed to add property. Please try again.")

		except Exception as e:
			self.show_error(f"Error: {str(e)}")

	def get_code_for_name(self, type_name, display_name):
		"""Get the database code for a display name from a lookup list"""
		if type_name == 'property_types':
			items = self.api.get_property_types() or []
		elif type_name == 'building_types':
			items = self.api.get_building_types() or []
		elif type_name == 'offer_types':
			items = self.api.get_offer_types() or []
		elif type_name == 'unit_measures':
			items = self.api.get_unit_measures() or []
		else:
			return display_name

		for item in items:
			if 'name' in item and item['name'] == display_name:
				return item.get('code', display_name)

		return display_name  # Return the display name if code not found

	def get_code_from_selection(self, selected_text, data_list):
		"""Extract code from selected text in format 'Name (Code)'"""
		if not selected_text or not data_list:
			return None

		for item in data_list:
			if f"{item['name']} ({item['code']})" == selected_text:
				return item['code']
		return None

	def on_new(self, instance=None):
		# Clear all fields
		self.property_code.text = ''
		self.property_type.text = 'Select Type'
		self.year_construction.text = ''
		self.building_type.text = 'Select Building Type'
		self.unit_measurement.text = 'Select Unit'
		self.facade.text = ''
		self.depth.text = ''
		self.floors.text = ''
		self.area.text = ''
		self.bedrooms.text = ''
		self.bathrooms.text = ''
		self.corner_yes.active = False
		self.corner_no.active = False
		self.offer_type.text = 'Select Offer Type'
		self.governorate.text = 'Select Province'
		self.region.text = 'Select Region'
		self.price.text = ''
		self.price_dinar.state = 'normal'
		self.price_dollar.state = 'normal'
		self.property_owner.text = ''
		self.address.text = ''
		self.notes.text = ''
		self.selected_photos = []  # Clear selected photos
		self.update_photo_count()  # Update photo count display
		self.update_photo_gallery()  # Clear photo gallery

	def show_file_chooser(self, instance):
		"""Show Windows File Explorer for selecting property photos."""
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
				# Add selected files to the selection
				for file_path in file_paths:
					if file_path not in self.selected_photos:
						self.selected_photos.append(file_path)

				self.update_photo_count()
				self.update_photo_gallery()
				self.show_success(f"Selected {len(file_paths)} photo(s)")

		except Exception as e:
			print(f"File chooser error: {str(e)}")  # Debug
			self.show_error(f"Failed to open file chooser:\n{str(e)}")

	def update_photo_count(self):
		"""Update the photo count display."""
		if hasattr(self, 'photo_count') and self.photo_count:
			count = len(self.selected_photos)
			if count == 0:
				self.photo_count.text = 'No photos selected'
			elif count == 1:
				self.photo_count.text = '1 photo selected'
			else:
				self.photo_count.text = f'{count} photos selected'

	def update_photo_gallery(self):
		"""Update the photo gallery preview with selected photos."""
		if hasattr(self, 'photo_gallery') and self.photo_gallery:
			# Clear existing preview items
			self.photo_gallery.clear_widgets()

			for photo_path in self.selected_photos:
				# Create a container for each photo preview
				photo_container = BoxLayout(
					orientation='vertical',
					size_hint=(None, 1),
					width=100,
					spacing=2
				)

				try:
					# Try to display the image
					from kivy.uix.image import Image
					img = Image(
						source=photo_path,
						size_hint=(1, 0.8),
						fit_mode='contain'
					)
				except Exception:
					# Fallback if image can't be loaded
					img = Label(
						text='[Image]',
						size_hint=(1, 0.8),
						color=(0.5, 0.5, 0.5, 1)
					)

				# Add remove button
				remove_btn = Button(
					text='×',
					size_hint=(1, 0.2),
					background_color=(0.8, 0.2, 0.2, 1),
					color=(1, 1, 1, 1)
				)

				# Bind remove button with photo path
				remove_btn.bind(on_press=lambda btn, path=photo_path: self.remove_photo(path))

				# Add widgets to container
				photo_container.add_widget(img)
				photo_container.add_widget(remove_btn)

				# Add container to gallery
				self.photo_gallery.add_widget(photo_container)

	def remove_photo(self, photo_path):
		"""Remove a photo from the selection."""
		if photo_path in self.selected_photos:
			self.selected_photos.remove(photo_path)
			self.update_photo_count()
			self.update_photo_gallery()

	def upload_photos(self, property_code, photo_paths):
		"""Upload photos for a property."""
		import shutil
		import uuid
		from pathlib import Path

		# Create storage directory for this property
		storage_dir = Path("data/realstateimages") / property_code
		storage_dir.mkdir(parents=True, exist_ok=True)

		for photo_path in photo_paths:
			try:
				# Generate unique filename to avoid conflicts
				original_file = Path(photo_path)
				file_extension = original_file.suffix.lower()
				unique_filename = f"{uuid.uuid4().hex[:8]}_{original_file.stem}{file_extension}"

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

	def show_owner_form(self, instance):
		"""Show responsive form for adding a new owner with proper localization"""
		from kivy.graphics import Color, RoundedRectangle
		from kivy.uix.widget import Widget

		# Main container with proper padding
		content = BoxLayout(
			orientation='vertical',
			padding=dp(25),
			spacing=dp(20)
		)

		# Add subtle background to content
		with content.canvas.before:
			Color(0.98, 0.98, 0.98, 1)
			content.bg_rect = RoundedRectangle(
				pos=content.pos,
				size=content.size,
				radius=[dp(5)]
			)
		content.bind(pos=lambda instance, value: setattr(content.bg_rect, 'pos', value))
		content.bind(size=lambda instance, value: setattr(content.bg_rect, 'size', value))

		# Form title
		title_label = Label(
			text=get_text('Add New Owner'),
			font_size=dp(18),
			size_hint_y=None,
			height=dp(35),
			color=(0.2, 0.2, 0.2, 1),
			bold=True,
			halign='center',
			valign='middle'
		)
		title_label.bind(size=title_label.setter('text_size'))
		if self.language_manager.current_language == 'ar':
			apply_arabic_font(title_label, title_label.text)
		content.add_widget(title_label)

		# Scrollable form area
		scroll_view = ScrollView(
			do_scroll_x=False,
			do_scroll_y=True,
			size_hint_y=0.7
		)

		form_container = BoxLayout(
			orientation='vertical',
			spacing=dp(15),
			size_hint_y=None
		)
		form_container.bind(minimum_height=form_container.setter('height'))

		# Owner Name field
		name_section = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None, height=dp(70))

		owner_name_label = Label(
			text=get_text('owner_name_label', 'Owner Name:'),
			font_size=dp(14),
			size_hint_y=None,
			height=dp(25),
			color=(0.3, 0.3, 0.3, 1),
			halign='left',
			valign='middle',
			bold=True
		)
		owner_name_label.bind(size=owner_name_label.setter('text_size'))
		if self.language_manager.current_language == 'ar':
			apply_arabic_font(owner_name_label, owner_name_label.text)
			owner_name_label.halign = 'right'

		owner_name_placeholder = get_text('enter_owner_name', 'Enter owner name')
		owner_name_input = TextInput(
			multiline=False,
			foreground_color=(0.2, 0.2, 0.2, 1),
			background_color=(1, 1, 1, 1),
			hint_text=owner_name_placeholder,
			hint_text_color=(0.6, 0.6, 0.6, 1),
			size_hint_y=None,
			height=dp(40),
			padding=[dp(10), dp(8)]
		)
		if self.language_manager.current_language == 'ar':
			apply_arabic_font(owner_name_input, owner_name_placeholder)

		name_section.add_widget(owner_name_label)
		name_section.add_widget(owner_name_input)
		form_container.add_widget(name_section)

		# Phone Number field
		phone_section = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None, height=dp(70))

		phone_label = Label(
			text=get_text('phone_label', 'Phone Number:'),
			font_size=dp(14),
			size_hint_y=None,
			height=dp(25),
			color=(0.3, 0.3, 0.3, 1),
			halign='left',
			valign='middle',
			bold=True
		)
		phone_label.bind(size=phone_label.setter('text_size'))
		if self.language_manager.current_language == 'ar':
			apply_arabic_font(phone_label, phone_label.text)
			phone_label.halign = 'right'

		owner_phone_placeholder = get_text('enter_phone', 'Enter phone number')
		owner_phone_input = TextInput(
			multiline=False,
			foreground_color=(0.2, 0.2, 0.2, 1),
			background_color=(1, 1, 1, 1),
			hint_text=owner_phone_placeholder,
			hint_text_color=(0.6, 0.6, 0.6, 1),
			size_hint_y=None,
			height=dp(40),
			padding=[dp(10), dp(8)],
			input_filter='int'
		)
		if self.language_manager.current_language == 'ar':
			apply_arabic_font(owner_phone_input, owner_phone_placeholder)

		phone_section.add_widget(phone_label)
		phone_section.add_widget(owner_phone_input)
		form_container.add_widget(phone_section)

		# Notes field
		notes_section = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None, height=dp(110))

		notes_label = Label(
			text=get_text('notes_label', 'Notes:'),
			font_size=dp(14),
			size_hint_y=None,
			height=dp(25),
			color=(0.3, 0.3, 0.3, 1),
			halign='left',
			valign='middle',
			bold=True
		)
		notes_label.bind(size=notes_label.setter('text_size'))
		if self.language_manager.current_language == 'ar':
			apply_arabic_font(notes_label, notes_label.text)
			notes_label.halign = 'right'

		owner_note_placeholder = get_text('enter_notes', 'Optional notes about the owner')
		owner_note_input = TextInput(
			multiline=True,
			foreground_color=(0.2, 0.2, 0.2, 1),
			background_color=(1, 1, 1, 1),
			hint_text=owner_note_placeholder,
			hint_text_color=(0.6, 0.6, 0.6, 1),
			size_hint_y=None,
			height=dp(80),
			padding=[dp(10), dp(8)]
		)
		if self.language_manager.current_language == 'ar':
			apply_arabic_font(owner_note_input, owner_note_placeholder)

		notes_section.add_widget(notes_label)
		notes_section.add_widget(owner_note_input)
		form_container.add_widget(notes_section)

		scroll_view.add_widget(form_container)
		content.add_widget(scroll_view)

		# Separator line
		separator = Widget(size_hint_y=None, height=dp(1))
		with separator.canvas:
			Color(0.8, 0.8, 0.8, 1)
			separator.line_rect = RoundedRectangle(
				pos=(separator.x, separator.center_y),
				size=(separator.width, dp(1)),
				radius=[dp(0.5)]
			)
		separator.bind(pos=lambda instance, value: setattr(separator.line_rect, 'pos', (instance.x, instance.center_y)))
		separator.bind(size=lambda instance, value: setattr(separator.line_rect, 'size', (instance.width, dp(1))))
		content.add_widget(separator)

		# Button container
		buttons_container = BoxLayout(
			size_hint_y=None,
			height=dp(55),
			spacing=dp(15),
			padding=[dp(5), dp(10)]
		)

		# Cancel button
		cancel_text = get_text('cancel', 'Cancel')
		cancel_btn = Button(
			text=cancel_text,
			font_size=dp(14),
			size_hint_x=0.4,
			background_color=(0.7, 0.7, 0.7, 1),
			color=(1, 1, 1, 1),
			size_hint_y=1
		)
		if self.language_manager.current_language == 'ar':
			apply_arabic_font(cancel_btn, cancel_text)

		# Save button
		save_text = get_text('save', 'Save Owner')
		save_btn = Button(
			text=save_text,
			font_size=dp(14),
			size_hint_x=0.6,
			background_color=(0.2, 0.7, 0.3, 1),
			color=(1, 1, 1, 1),
			size_hint_y=1
		)
		if self.language_manager.current_language == 'ar':
			apply_arabic_font(save_btn, save_text)

		buttons_container.add_widget(cancel_btn)
		buttons_container.add_widget(save_btn)
		content.add_widget(buttons_container)

		# Create responsive popup
		popup_title = get_text('add_new_owner_title', 'Add New Owner')
		popup = Popup(
			title=popup_title,
			content=content,
			size_hint=(0.9, 0.7),  # More responsive sizing
			background='',
			background_color=(1, 1, 1, 1),
			separator_color=(0.2, 0.6, 0.8, 1),
			title_color=(0.2, 0.2, 0.2, 1),
			title_size=dp(16)
		)

		# Apply Arabic font to popup title
		if self.language_manager.current_language == 'ar':
			apply_arabic_font(popup, popup_title)

		# Bind button events
		cancel_btn.bind(on_press=popup.dismiss)
		save_btn.bind(on_press=lambda x: self.add_owner(
			owner_name_input.text,
			owner_phone_input.text,
			owner_note_input.text,
			popup
		))

		# Focus on name input when popup opens
		def focus_name_input(dt):
			owner_name_input.focus = True

		popup.bind(on_open=lambda x: Clock.schedule_once(focus_name_input, 0.1))
		popup.open()

	def add_owner(self, name, phone, note, popup):
		"""Add a new owner to the database"""
		if not name.strip():
			self.show_error(get_text('owner_name_required', 'Owner name is required'))
			return

		try:
			owner_code = self.api.add_owner(name, phone, note)
			if owner_code:
				success_msg = get_text('owner_added_success', 'Owner {0} added successfully').format(name)
				self.show_success(success_msg)
				# Reload owners data and select the new owner
				self.load_owners()
				# Set spinner to new owner
				for o in self.owners_data:
					if o.get('Ownercode') == owner_code:
						label = f"{o['ownername']} ({o['Ownercode']})"
						self.property_owner.text = label
						break
				popup.dismiss()
			else:
				self.show_error(get_text('failed_to_add_owner', 'Failed to add owner'))
		except Exception as e:
			error_msg = get_text('error_adding_owner', 'Error adding owner: {0}').format(str(e))
			self.show_error(error_msg)

	def show_success(self, message):
		"""Show success message popup."""
		content = Label(
			text=message,
			color=(0.2, 0.8, 0.3, 1),
			text_size=(None, None),
			halign='center',
			valign='middle'
		)
		apply_arabic_font(content, message)

		popup = Popup(
			title=get_text('success', 'Success'),
			content=content,
			size_hint=(0.7, 0.3),
			background='',  # Remove default background
			background_color=(1, 1, 1, 1),  # Set white background
			separator_color=(0.2, 0.6, 0.8, 1)
		)
		# Apply Arabic font to popup title
		apply_arabic_font(popup, popup.title)
		popup.open()

	def show_error(self, message):
		"""Show error message popup."""
		content = Label(
			text=message,
			color=(0.8, 0.2, 0.2, 1),
			text_size=(None, None),
			halign='center',
			valign='middle'
		)
		apply_arabic_font(content, message)

		popup = Popup(
			title=get_text('error', 'Error'),
			content=content,
			size_hint=(0.7, 0.3),
			background='',  # Remove default background
			background_color=(1, 1, 1, 1),  # Set white background
			separator_color=(0.2, 0.6, 0.8, 1)
		)
		# Apply Arabic font to popup title
		apply_arabic_font(popup, popup.title)
		popup.open()