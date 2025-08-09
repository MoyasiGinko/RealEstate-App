from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label

Builder.load_file('assets/kv/insert_gui.kv')

class InsertScreen(Screen):
	property_code = ObjectProperty(None)
	property_type = ObjectProperty(None)
	year_construction = ObjectProperty(None)
	building_type = ObjectProperty(None)
	unit_measurement = ObjectProperty(None)
	facade = ObjectProperty(None)
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
	add_photo = ObjectProperty(None)
	notes = ObjectProperty(None)
	save_btn = ObjectProperty(None)
	new_btn = ObjectProperty(None)

	def on_save(self):
		# Example: collect data and show a popup
		data = {
			'Property Code': self.property_code.text,
			'Property Type': self.property_type.text,
			'Year of Construction': self.year_construction.text,
			'Building Type': self.building_type.text,
			'Unit of Measurement': self.unit_measurement.text,
			'Facade': self.facade.text,
			'Floors': self.floors.text,
			'Area': self.area.text,
			'Bedrooms': self.bedrooms.text,
			'Bathrooms': self.bathrooms.text,
			'Corner': 'Yes' if self.corner_yes.active else 'No',
			'Offer Type': self.offer_type.text,
			'Governorate': self.governorate.text,
			'Neighborhood': self.neighborhood.text,
			'Price': self.price.text,
			'Currency': 'Dinar' if self.price_dinar.state == 'down' else 'Dollar',
			'Property Owner': self.property_owner.text,
			'Notes': self.notes.text
		}
		Popup(title='Saved', content=Label(text='Property saved!'), size_hint=(0.5, 0.3)).open()
		# Here you would add logic to save to database

	def on_new(self):
		# Example: clear all fields
		self.property_code.text = ''
		self.property_type.text = 'Select Type'
		self.year_construction.text = ''
		self.building_type.text = 'Select Building Type'
		self.unit_measurement.text = 'Select Unit'
		self.facade.text = ''
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
		self.notes.text = ''
		# Here you would also clear any added photos
