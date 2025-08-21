from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
import os
import shutil
import sys
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.models.database_api import get_api
from configs.language_manager import get_language_manager, get_text
from configs.arabic_fonts import apply_arabic_font

# Load the KV file for the upload_gui interface - use absolute path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir))
_kv_path = os.path.join(_project_root, 'assets', 'kv', 'upload_gui.kv')
Builder.load_file(_kv_path)


class ConfirmationPopup(Popup):
    """Popup for confirmation dialogs."""

    def __init__(self, title_text, message, on_yes_callback, **kwargs):
        super(ConfirmationPopup, self).__init__(**kwargs)
        self.title = title_text
        self.size_hint = (None, None)
        self.size = (dp(400), dp(200))
        self.on_yes_callback = on_yes_callback

        # Create layout
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Message
        message_label = Label(
            text=message,
            text_size=(dp(350), None),
            halign='center',
            valign='middle'
        )
        layout.add_widget(message_label)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))

        no_btn = Button(text='No', size_hint_x=0.5, background_color=(0.8, 0.2, 0.2, 1))
        no_btn.bind(on_press=self.dismiss)
        button_layout.add_widget(no_btn)

        yes_btn = Button(text='Yes', size_hint_x=0.5, background_color=(0.2, 0.6, 0.2, 1))
        yes_btn.bind(on_press=self.on_yes)
        button_layout.add_widget(yes_btn)

        layout.add_widget(button_layout)
        self.content = layout

    def on_yes(self, instance):
        """Handle yes button press."""
        self.dismiss()
        self.on_yes_callback()


class UploadScreen(Screen):
    """Screen for database management operations."""

    def __init__(self, **kwargs):
        super(UploadScreen, self).__init__(**kwargs)
        self.api = get_api()
        # Fix the path to use the correct User-Desktop directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.db_path = os.path.join(project_root, 'data', 'local.db')
        self.database_utils_path = os.path.join(project_root, 'configs/database_utils')
        print(f"Database path: {self.db_path}")  # Debug output
        self.language_manager = get_language_manager()
        # Register for language change notifications
        self.language_manager.register_observer(self)
        # Bind to on_enter to setup localization
        self.bind(on_enter=self.setup_localization)

    def setup_localization(self, *args):
        """Setup localization and Arabic fonts"""
        try:
            self.update_texts()
            self.apply_fonts()
        except Exception as e:
            print(f"Error setting up localization in upload screen: {e}")

    def show_language_switcher(self):
        """Show language switcher popup"""
        from configs.language_switcher import LanguageSwitcherPopup
        popup = LanguageSwitcherPopup()
        popup.open()

    def update_texts(self):
        """Update all text widgets with current language"""
        try:
            # Define the mapping of IDs to translation keys
            text_mappings = {
                'screen_title': 'database_management',
                'description_label': 'db_description',
                'reset_db_btn': 'reset_database',
                'export_db_btn': 'export_database',
                'seed_db_btn': 'seed_database',
                'upload_db_btn': 'upload_database',
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

            # Update description labels with more specific content
            description_mappings = {
                'reset_db_description': ('reset_db_desc', 'Create a fresh empty database\n(Deletes all existing data)'),
                'export_db_description': ('export_db_desc', 'Create a backup copy of\nyour current database'),
                'seed_db_description': ('seed_db_desc', 'Add sample data to database\n(Preserves existing data)'),
                'upload_db_description': ('upload_db_desc', 'Replace current database\nwith a new file')
            }

            for widget_id, (text_key, fallback_text) in description_mappings.items():
                try:
                    widget = self.ids.get(widget_id)
                    if widget:
                        new_text = get_text(text_key, fallback_text)
                        widget.text = new_text
                        # Apply Arabic font if needed
                        if self.language_manager.current_language == 'ar':
                            apply_arabic_font(widget, new_text)
                except Exception as e:
                    print(f"Error updating description widget {widget_id}: {e}")

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
                print(f"Error applying fonts in upload screen: {e}")

    def on_language_changed(self):
        """Called when language is changed"""
        try:
            self.update_texts()
            self.apply_fonts()
        except Exception as e:
            print(f"Error handling language change in upload screen: {e}")

    def import_database_utility(self, module_name):
        """Safely import database utility modules."""
        try:
            # Add database_utils to path if not already there
            if self.database_utils_path not in sys.path:
                sys.path.insert(0, self.database_utils_path)

            # Dynamic import
            module = __import__(module_name)
            return module
        except ImportError as e:
            self.show_message("Import Error", f"Could not import {module_name}:\n{str(e)}")
            return None

    def create_fresh_database(self, instance=None):
        """Create a fresh database (reset) - exactly like the original create_database command."""
        def confirm_reset():
            try:
                print(f"Attempting to reset database at: {self.db_path}")  # Debug

                # Create backup before resetting
                backup_dir = os.path.join(os.path.dirname(self.db_path), 'backups')
                os.makedirs(backup_dir, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"local_db_backup_before_reset_{timestamp}.db"
                backup_path = os.path.join(backup_dir, backup_filename)

                # Backup current database if it exists
                backup_created = False
                if os.path.exists(self.db_path):
                    try:
                        shutil.copy2(self.db_path, backup_path)
                        backup_created = True
                        print(f"Database backed up to: {backup_path}")  # Debug
                    except Exception as backup_error:
                        print(f"Warning: Failed to create backup: {str(backup_error)}")  # Debug
                        # Ask user if they want to continue without backup
                        continue_without_backup = self.ask_continue_without_backup()
                        if not continue_without_backup:
                            return

                # Import the create_database utility
                create_db_module = self.import_database_utility('create_database')
                if create_db_module is None:
                    return

                # Close current API connection completely
                self.api.close()

                # Call the original create_fresh_database function exactly as it was working before
                result = create_db_module.create_fresh_database(self.db_path)
                print(f"Create database result: {result}")  # Debug

                if result:
                    # Reconnect API
                    self.api.connect()
                    success_message = f"Database has been reset successfully!\n\nLocation: {result}"
                    if backup_created:
                        success_message += f"\n\nPrevious database backed up to:\n{backup_path}"
                    self.show_message("Success", success_message)
                else:
                    # Reconnect API even if failed
                    self.api.connect()
                    self.show_message("Error", "Failed to reset database. Please close the application completely and try again.\n\nThe database file might be locked by another process.")

            except Exception as e:
                print(f"Error in create_fresh_database: {str(e)}")  # Debug
                # Ensure we reconnect even if there was an error
                try:
                    self.api.connect()
                except:
                    pass
                self.show_message("Error", f"Failed to reset database: {str(e)}")

        # Show confirmation dialog with backup information
        popup = ConfirmationPopup(
            "Reset Database",
            "Are you sure you want to reset the database?\n\nThis will:\n• Delete ALL existing data\n• Create a backup first\n• Create a fresh empty database\n\nContinue?",
            confirm_reset
        )
        popup.open()

    def ask_continue_without_backup(self):
        """Ask user if they want to continue reset without creating backup."""
        import tkinter.messagebox as msgbox

        root = tk.Tk()
        root.withdraw()  # Hide the main window
        root.wm_attributes('-topmost', 1)  # Bring to front

        result = msgbox.askyesno(
            "Backup Failed",
            "Failed to create backup of current database.\n\nDo you want to continue with reset anyway?\n\nWarning: This will permanently delete all data!",
            icon='warning'
        )

        root.destroy()
        return result

    def export_database(self, instance=None):
        """Export the current database."""
        try:
            print(f"Exporting database from: {self.db_path}")  # Debug

            # Check if database file exists
            if not os.path.exists(self.db_path):
                self.show_message("Error", f"Database file not found at:\n{self.db_path}")
                return

            # Create backups directory if it doesn't exist
            backup_dir = os.path.join(os.path.dirname(self.db_path), 'backups')
            os.makedirs(backup_dir, exist_ok=True)

            # Generate timestamp for backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"local_db_backup_{timestamp}.db"
            backup_path = os.path.join(backup_dir, backup_filename)

            # Copy the database file
            shutil.copy2(self.db_path, backup_path)
            print(f"Database exported to: {backup_path}")  # Debug

            self.show_message(
                "Export Successful",
                f"Database exported successfully!\n\nFrom: {self.db_path}\n\nTo: {backup_path}\n\nBackup size: {os.path.getsize(backup_path)} bytes"
            )

        except Exception as e:
            print(f"Export error: {str(e)}")  # Debug
            self.show_message("Export Error", f"Failed to export database:\n{str(e)}")

    def seed_database(self, instance=None):
        """Seed the database with sample data."""
        def confirm_seed():
            try:
                print(f"Seeding database at: {self.db_path}")  # Debug

                # Import the seed_data utility
                seed_data_module = self.import_database_utility('seed_data')
                if seed_data_module is None:
                    return

                # Smart merge seed data (preserves existing data)
                seed_data_module.smart_merge_seed_data(self.db_path)

                self.show_message(
                    "Seeding Successful",
                    f"Database has been seeded with sample data!\n\nLocation: {self.db_path}\n\nExisting data has been preserved."
                )

            except Exception as e:
                print(f"Seeding error: {str(e)}")  # Debug
                self.show_message("Seeding Error", f"Failed to seed database:\n{str(e)}")

        # Show confirmation dialog
        popup = ConfirmationPopup(
            "Seed Database",
            "This will add sample data to your database.\nExisting data will be preserved.\n\nContinue?",
            confirm_seed
        )
        popup.open()

    def upload_database(self, instance=None):
        """Upload a new database file to replace the current one using Windows File Explorer."""
        try:
            # Hide the Kivy window temporarily to show native dialog
            root = tk.Tk()
            root.withdraw()  # Hide the main tkinter window
            root.wm_attributes('-topmost', 1)  # Bring dialog to front

            # Open Windows File Explorer dialog
            file_path = filedialog.askopenfilename(
                title="Select Database File to Upload",
                filetypes=[
                    ("Database files", "*.db"),
                    ("SQLite files", "*.sqlite"),
                    ("All files", "*.*")
                ],
                initialdir=os.path.expanduser("~\\Desktop")  # Start from Desktop
            )

            root.destroy()  # Clean up tkinter

            if not file_path:
                return  # User cancelled

            # Validate the selected file
            if not os.path.exists(file_path):
                self.show_message("File Error", "Selected file does not exist.")
                return

            # Check file size (optional - warn if very large)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            if file_size > 100:  # Warn if larger than 100MB
                self.show_message(
                    "Large File Warning",
                    f"Selected file is {file_size:.1f}MB.\nThis might take some time to upload."
                )

            def confirm_upload():
                try:
                    print(f"Uploading database from: {file_path}")  # Debug

                    # Close current API connection
                    self.api.close()

                    # Create backup of current database
                    backup_dir = os.path.join(os.path.dirname(self.db_path), 'backups')
                    os.makedirs(backup_dir, exist_ok=True)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_filename = f"local_db_backup_before_upload_{timestamp}.db"
                    backup_path = os.path.join(backup_dir, backup_filename)

                    # Backup current database
                    if os.path.exists(self.db_path):
                        shutil.copy2(self.db_path, backup_path)
                        print(f"Current database backed up to: {backup_path}")  # Debug

                    # Replace with new database
                    shutil.copy2(file_path, self.db_path)
                    print(f"Database replaced with: {file_path}")  # Debug

                    # Reconnect API
                    self.api.connect()

                    self.show_message(
                        "Upload Successful",
                        f"Database has been replaced successfully!\n\nFile: {os.path.basename(file_path)}\nSize: {file_size:.1f}MB\n\nPrevious database backed up to:\n{backup_path}"
                    )

                except Exception as e:
                    print(f"Upload error: {str(e)}")  # Debug
                    self.show_message("Upload Error", f"Failed to upload database:\n{str(e)}")

            # Show confirmation for upload
            popup = ConfirmationPopup(
                "Replace Database",
                f"Replace current database with:\n\nFile: {os.path.basename(file_path)}\nSize: {file_size:.1f}MB\nLocation: {file_path}\n\nThe current database will be backed up first.\n\nContinue?",
                confirm_upload
            )
            popup.open()

        except Exception as e:
            print(f"File chooser error: {str(e)}")  # Debug
            self.show_message("File Chooser Error", f"Failed to open file chooser:\n{str(e)}")

    def show_message(self, title, message):
        """Show a message popup."""
        popup = Popup(
            title=title,
            content=Label(
                text=message,
                text_size=(dp(400), None),
                halign='center',
                valign='middle'
            ),
            size_hint=(None, None),
            size=(dp(450), dp(300))
        )
        popup.open()

    def go_to_main_gui(self, instance=None):
        """Navigate back to main GUI."""
        if hasattr(self.manager, 'current'):
            self.manager.current = 'main_gui'