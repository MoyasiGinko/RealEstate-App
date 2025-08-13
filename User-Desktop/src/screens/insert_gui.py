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
from kivy.metrics import dp
from datetime import datetime
import os
from src.models.database_api import get_api

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
	neighborhood = ObjectProperty(None)
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

	def on_enter(self):
		"""Called when the screen is entered"""
		# Load data from database for dropdowns
		self.load_property_types()
		self.load_building_types()
		self.load_offer_types()
		self.load_unit_measurements()
		self.load_owners()

		# Set current year as default
		if hasattr(self, 'year_construction') and self.year_construction:
			current_year = str(datetime.now().year)
			self.year_construction.text = current_year

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
				'Province-code': self.governorate.text,
				'Region-code': self.neighborhood.text,
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
		self.governorate.text = ''
		self.neighborhood.text = ''
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
		"""Show file chooser for selecting property photos."""
		content = BoxLayout(orientation='vertical')

		file_chooser = FileChooserListView(
			path='/',  # Start from root directory
			filters=['*.jpg', '*.jpeg', '*.png']  # Only show image files
		)

		buttons = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))

		select_button = Button(text='Select')
		cancel_button = Button(text='Cancel')

		select_button.bind(on_press=lambda x: self.select_photos(file_chooser.selection, popup))
		cancel_button.bind(on_press=lambda x: popup.dismiss())

		buttons.add_widget(select_button)
		buttons.add_widget(cancel_button)

		content.add_widget(file_chooser)
		content.add_widget(buttons)

		popup = Popup(
			title='Select Photos',
			content=content,
			size_hint=(0.9, 0.9)
		)

		popup.open()

	def select_photos(self, selection, popup):
		"""Handle photo selection."""
		if selection:
			self.selected_photos.extend(selection)
			popup.dismiss()
			self.update_photo_count()
			self.update_photo_gallery()
			self.show_success(f"Selected {len(selection)} photo(s)")

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
		"""Show form for adding a new owner"""
		content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

		form = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(120))

		form.add_widget(Label(text='Owner Name:'))
		owner_name_input = TextInput(multiline=False)
		form.add_widget(owner_name_input)

		form.add_widget(Label(text='Phone Number:'))
		owner_phone_input = TextInput(multiline=False)
		form.add_widget(owner_phone_input)

		form.add_widget(Label(text='Notes:'))
		owner_note_input = TextInput(multiline=True)
		form.add_widget(owner_note_input)

		content.add_widget(form)

		buttons = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
		cancel_btn = Button(text='Cancel')
		save_btn = Button(text='Save Owner', background_color=(0.2, 0.7, 0.3, 1))

		popup = Popup(title='Add New Owner', content=content, size_hint=(0.8, 0.4))

		cancel_btn.bind(on_press=popup.dismiss)
		save_btn.bind(on_press=lambda x: self.add_owner(
			owner_name_input.text,
			owner_phone_input.text,
			owner_note_input.text,
			popup
		))

		buttons.add_widget(cancel_btn)
		buttons.add_widget(save_btn)
		content.add_widget(buttons)

		popup.open()

	def add_owner(self, name, phone, note, popup):
		"""Add a new owner to the database"""
		if not name.strip():
			self.show_error("Owner name is required")
			return

		try:
			owner_code = self.api.add_owner(name, phone, note)
			if owner_code:
				self.show_success(f"Owner {name} added successfully")
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
				self.show_error("Failed to add owner")
		except Exception as e:
			self.show_error(f"Error adding owner: {str(e)}")

	def show_success(self, message):
		"""Show success message popup."""
		popup = Popup(
			title='Success',
			content=Label(text=message),
			size_hint=(0.7, 0.3)
		)
		popup.open()

	def show_error(self, message):
		"""Show error message popup."""
		popup = Popup(
			title='Error',
			content=Label(text=message),
			size_hint=(0.7, 0.3)
		)
		popup.open()