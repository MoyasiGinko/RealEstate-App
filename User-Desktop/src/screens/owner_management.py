from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.uix.spinner import Spinner
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from src.models.database_api import get_api
import re

class OwnerForm(BoxLayout):
    """Form for adding or editing an owner."""

    def __init__(self, save_callback, owner_data=None, **kwargs):
        super(OwnerForm, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)

        # Set white background for the form
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.save_callback = save_callback
        self.owner_data = owner_data
        self.owner_code = owner_data.get('Ownercode') if owner_data else None

        # Title
        title = 'Edit Owner' if owner_data else 'Add New Owner'
        self.add_widget(Label(
            text=title,
            font_size=dp(24),
            size_hint_y=None,
            height=dp(40),
            color=(0.2, 0.2, 0.2, 1)  # Dark gray text
        ))

        # Form container with scroll view for larger forms
        form_container = BoxLayout(orientation='vertical', spacing=dp(10))

        # Owner name input
        name_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(60))
        name_layout.add_widget(Label(
            text='Owner Name*',
            size_hint_y=None,
            height=dp(20),
            halign='left',
            text_size=(dp(300), dp(20)),
            color=(0.3, 0.3, 0.3, 1)  # Dark gray text
        ))
        self.owner_name_input = TextInput(
            hint_text='Enter owner name',
            text=owner_data.get('ownername', '') if owner_data else '',
            multiline=False,
            size_hint_y=None,
            height=dp(40),
            background_color=(0.98, 0.98, 0.98, 1),  # Light gray background
            foreground_color=(0.2, 0.2, 0.2, 1)  # Dark text
        )
        name_layout.add_widget(self.owner_name_input)
        form_container.add_widget(name_layout)

        # Owner phone input
        phone_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(60))
        phone_layout.add_widget(Label(
            text='Owner Phone*',
            size_hint_y=None,
            height=dp(20),
            halign='left',
            text_size=(dp(300), dp(20)),
            color=(0.3, 0.3, 0.3, 1)  # Dark gray text
        ))
        self.owner_phone_input = TextInput(
            hint_text='Enter phone number (07xxxxxxxxx)',
            text=owner_data.get('ownerphone', '') if owner_data else '',
            multiline=False,
            size_hint_y=None,
            height=dp(40),
            input_filter=self.phone_filter,
            background_color=(0.98, 0.98, 0.98, 1),  # Light gray background
            foreground_color=(0.2, 0.2, 0.2, 1)  # Dark text
        )
        phone_layout.add_widget(self.owner_phone_input)
        form_container.add_widget(phone_layout)

        # Note input
        note_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120))
        note_layout.add_widget(Label(
            text='Note',
            size_hint_y=None,
            height=dp(20),
            halign='left',
            text_size=(dp(300), dp(20)),
            color=(0.3, 0.3, 0.3, 1)  # Dark gray text
        ))
        self.note_input = TextInput(
            hint_text='Enter additional notes (optional)',
            text=owner_data.get('Note', '') if owner_data else '',
            multiline=True,
            size_hint_y=None,
            height=dp(100),
            background_color=(0.98, 0.98, 0.98, 1),  # Light gray background
            foreground_color=(0.2, 0.2, 0.2, 1)  # Dark text
        )
        note_layout.add_widget(self.note_input)
        form_container.add_widget(note_layout)

        # Add the form container to the layout
        self.add_widget(form_container)

        # Buttons layout
        buttons_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))

        # Save button
        save_button = Button(
            text='Save',
            background_color=(0.2, 0.6, 0.2, 1),  # Green button
            color=(1, 1, 1, 1)  # White text
        )
        save_button.bind(on_press=self.save)
        buttons_layout.add_widget(save_button)

        # Cancel button
        self.cancel_button = Button(
            text='Cancel',
            background_color=(0.6, 0.2, 0.2, 1),  # Red button
            color=(1, 1, 1, 1)  # White text
        )
        # We'll bind this in the parent class
        buttons_layout.add_widget(self.cancel_button)

        self.add_widget(buttons_layout)

    def update_rect(self, instance, value):
        """Update the rectangle position and size."""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def phone_filter(self, text, from_undo=False):
        """Filter for phone number input - only allow digits and limit length."""
        if len(text) <= 11 and text.isdigit():
            return text
        return ''

    def save(self, instance):
        """Save the owner data."""
        owner_name = self.owner_name_input.text.strip()
        owner_phone = self.owner_phone_input.text.strip()
        note = self.note_input.text.strip()

        if not owner_name:
            self.show_error("Owner name is required.")
            return

        if not owner_phone:
            self.show_error("Owner phone is required.")
            return

        # Validate phone number format (should be 11 digits and start with 07)
        phone_pattern = re.compile(r'^07\d{9}$')
        if not phone_pattern.match(owner_phone):
            self.show_error("Phone number must be 11 digits and start with 07.")
            return

        # Call the save callback with the owner data
        self.save_callback(owner_name, owner_phone, note, self.owner_code)

    def show_error(self, message):
        """Show an error popup."""
        popup = Popup(
            title='Error',
            content=Label(text=message, color=(0.2, 0.2, 0.2, 1)),
            size_hint=(0.7, 0.3)
        )
        popup.open()

class OwnerManagementScreen(Screen):
    """Screen for managing owners."""

    def __init__(self, **kwargs):
        super(OwnerManagementScreen, self).__init__(**kwargs)
        self.api = get_api()

        # Set white background for the entire screen
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_screen_rect, size=self.update_screen_rect)

        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header with title and add button
        header = BoxLayout(size_hint_y=None, height=dp(50))
        header.add_widget(Label(
            text='Owner Management',
            font_size=dp(24),
            halign='left',
            valign='middle',
            text_size=(dp(300), dp(50)),
            color=(0.2, 0.2, 0.2, 1)  # Dark gray text
        ))

        add_button = Button(
            text='Add Owner',
            size_hint_x=None,
            width=dp(120),
            background_color=(0.2, 0.6, 0.2, 1),  # Green button
            color=(1, 1, 1, 1)  # White text
        )
        add_button.bind(on_press=self.show_add_owner_form)
        header.add_widget(add_button)

        self.layout.add_widget(header)

        # Search bar
        search_container = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))

        self.search_input = TextInput(
            hint_text='Search owners by name or phone',
            multiline=False,
            size_hint_x=0.7,
            background_color=(0.98, 0.98, 0.98, 1),  # Light gray background
            foreground_color=(0.2, 0.2, 0.2, 1)  # Dark text
        )
        self.search_input.bind(text=self.on_search_text_changed)
        search_container.add_widget(self.search_input)

        search_button = Button(
            text='Search',
            size_hint_x=0.15,
            background_color=(0.2, 0.4, 0.8, 1),  # Blue button
            color=(1, 1, 1, 1)  # White text
        )
        search_button.bind(on_press=self.search_owners)
        search_container.add_widget(search_button)

        clear_button = Button(
            text='Clear',
            size_hint_x=0.15,
            background_color=(0.5, 0.5, 0.5, 1),  # Gray button
            color=(1, 1, 1, 1)  # White text
        )
        clear_button.bind(on_press=self.clear_search)
        search_container.add_widget(clear_button)

        self.layout.add_widget(search_container)

        # Stats summary
        self.stats_label = Label(
            text='Total Owners: 0',
            size_hint_y=None,
            height=dp(30),
            halign='right',
            valign='middle',
            text_size=(self.width, dp(30)),
            color=(0.3, 0.3, 0.3, 1)  # Dark gray text
        )
        self.layout.add_widget(self.stats_label)

        # Owners list header
        list_header = GridLayout(cols=4, size_hint_y=None, height=dp(40))
        # Add background to header
        with list_header.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light gray background for header
            list_header.rect = Rectangle(pos=list_header.pos, size=list_header.size)
        list_header.bind(pos=self.update_rect, size=self.update_rect)

        list_header.add_widget(Label(text='Code', bold=True, color=(0.2, 0.2, 0.2, 1)))
        list_header.add_widget(Label(text='Name', bold=True, color=(0.2, 0.2, 0.2, 1)))
        list_header.add_widget(Label(text='Phone', bold=True, color=(0.2, 0.2, 0.2, 1)))
        list_header.add_widget(Label(text='Actions', bold=True, color=(0.2, 0.2, 0.2, 1)))
        self.layout.add_widget(list_header)

        # Owners list in a scrollview
        self.owners_container = GridLayout(cols=1, spacing=dp(2), size_hint_y=None)
        self.owners_container.bind(minimum_height=self.owners_container.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        scroll_view.add_widget(self.owners_container)
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

        # All owners cache
        self.all_owners = []

        self.add_widget(self.layout)

    def update_screen_rect(self, instance, value):
        """Update the screen background rectangle position and size."""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def on_search_text_changed(self, instance, value):
        """Filter owners as user types."""
        if len(value) >= 3:  # Only search if at least 3 characters
            self.search_owners(None)

    def search_owners(self, instance):
        """Search owners by name or phone."""
        search_text = self.search_input.text.strip().lower()

        if not search_text:
            self.load_owners()
            return

        # Filter owners from the cached list
        filtered_owners = [
            owner for owner in self.all_owners
            if search_text in owner['ownername'].lower() or search_text in owner['ownerphone']
        ]

        self.display_owners(filtered_owners)
        self.stats_label.text = f'Found: {len(filtered_owners)} owners'

    def clear_search(self, instance):
        """Clear search and show all owners."""
        self.search_input.text = ''
        self.load_owners()

    def on_enter(self):
        """Load the owners list when entering the screen."""
        self.load_owners()

    def load_owners(self):
        """Load owners from the database and display them."""
        self.all_owners = self.api.get_all_owners()
        self.display_owners(self.all_owners)
        self.stats_label.text = f'Total Owners: {len(self.all_owners)}'

    def display_owners(self, owners):
        """Display the list of owners."""
        self.owners_container.clear_widgets()

        if not owners:
            self.owners_container.add_widget(
                Label(
                    text='No owners found. Click "Add Owner" to create one.',
                    size_hint_y=None,
                    height=dp(40),
                    color=(0.4, 0.4, 0.4, 1)  # Gray text
                )
            )
            return

        for owner in owners:
            owner_row = GridLayout(cols=4, size_hint_y=None, height=dp(40))

            # Add a background color effect for rows
            with owner_row.canvas.before:
                Color(0.98, 0.98, 0.98, 1)  # Very light gray background
                owner_row.rect = Rectangle(pos=owner_row.pos, size=owner_row.size)

            owner_row.bind(pos=self.update_rect, size=self.update_rect)

            owner_row.add_widget(Label(
                text=owner['Ownercode'],
                color=(0.2, 0.2, 0.6, 1)  # Dark blue text
            ))
            owner_row.add_widget(Label(text=owner['ownername'], color=(0.2, 0.2, 0.2, 1)))
            owner_row.add_widget(Label(text=owner['ownerphone'], color=(0.2, 0.2, 0.2, 1)))

            actions = BoxLayout(spacing=dp(5))

            edit_button = Button(
                text='Edit',
                background_color=(0.2, 0.4, 0.8, 1),  # Blue button
                color=(1, 1, 1, 1)  # White text
            )
            edit_button.bind(on_press=lambda x, o=owner: self.show_edit_owner_form(o))
            actions.add_widget(edit_button)

            delete_button = Button(
                text='Delete',
                background_color=(0.6, 0.2, 0.2, 1),  # Red button
                color=(1, 1, 1, 1)  # White text
            )
            delete_button.bind(on_press=lambda x, code=owner['Ownercode']: self.confirm_delete_owner(code))
            actions.add_widget(delete_button)

            owner_row.add_widget(actions)

            self.owners_container.add_widget(owner_row)

    def update_rect(self, instance, value):
        """Update the rectangle position and size."""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def show_add_owner_form(self, instance):
        """Show the form for adding a new owner."""
        content = OwnerForm(save_callback=self.add_owner)
        self.popup = Popup(
            title='Add New Owner',
            content=content,
            size_hint=(0.8, 0.8)
        )
        # Bind the cancel method directly to the popup
        content.cancel_button.bind(on_press=lambda x: self.popup.dismiss())
        self.popup.open()

    def show_edit_owner_form(self, owner_data):
        """Show the form for editing an owner."""
        content = OwnerForm(save_callback=self.update_owner, owner_data=owner_data)
        self.popup = Popup(
            title='Edit Owner',
            content=content,
            size_hint=(0.8, 0.8)
        )
        # Bind the cancel method directly to the popup
        content.cancel_button.bind(on_press=lambda x: self.popup.dismiss())
        self.popup.open()

    def add_owner(self, owner_name, owner_phone, note, owner_code=None):
        """Add a new owner to the database."""
        owner_code = self.api.add_owner(owner_name, owner_phone, note)

        if owner_code:
            self.popup.dismiss()
            self.show_success(f"Owner '{owner_name}' added successfully!")
            self.load_owners()
        else:
            self.show_error("Failed to add owner. Please try again.")

    def update_owner(self, owner_name, owner_phone, note, owner_code):
        """Update an existing owner in the database."""
        if self.api.update_owner(owner_code, owner_name, owner_phone, note):
            self.popup.dismiss()
            self.show_success(f"Owner '{owner_name}' updated successfully!")
            self.load_owners()
        else:
            self.show_error("Failed to update owner. Please try again.")

    def confirm_delete_owner(self, owner_code):
        """Show confirmation dialog for deleting an owner."""
        # Get owner details for the confirmation message
        owner = self.api.get_owner_by_code(owner_code)
        if not owner:
            self.show_error("Owner not found.")
            return

        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(
            text=f"Are you sure you want to delete owner '{owner['ownername']}' ({owner_code})?\n\n"
                 "Note: Owners linked to properties cannot be deleted.",
            color=(0.2, 0.2, 0.2, 1)  # Dark gray text
        ))

        buttons = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))

        yes_button = Button(
            text='Yes, Delete',
            background_color=(0.6, 0.2, 0.2, 1),  # Red button
            color=(1, 1, 1, 1)  # White text
        )
        yes_button.bind(on_press=lambda x: self.delete_owner(owner_code))
        buttons.add_widget(yes_button)

        no_button = Button(
            text='Cancel',
            background_color=(0.5, 0.5, 0.5, 1),  # Gray button
            color=(1, 1, 1, 1)  # White text
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

    def delete_owner(self, owner_code):
        """Delete an owner from the database."""
        if self.api.delete_owner(owner_code):
            self.confirm_popup.dismiss()
            self.show_success("Owner deleted successfully!")
            self.load_owners()
        else:
            self.confirm_popup.dismiss()
            self.show_error("Failed to delete owner. The owner may be linked to one or more properties.")

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
            content=Label(text=message, color=(0.2, 0.2, 0.2, 1)),
            size_hint=(0.7, 0.3)
        )
        popup.open()

    def go_to_dashboard(self, instance=None):
        """Navigate back to the dashboard."""
        self.manager.current = 'dashboard'