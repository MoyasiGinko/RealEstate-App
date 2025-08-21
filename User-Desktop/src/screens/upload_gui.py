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
    """Popup for confirmation dialogs with improved design and localization."""

    def __init__(self, title_key, message_key, on_yes_callback, title_fallback="Confirm", message_fallback="Are you sure?", **kwargs):
        super(ConfirmationPopup, self).__init__(**kwargs)

        # Get localized text
        title_text = get_text(title_key, title_fallback)
        self.size_hint = (0.8, 0.6)  # More responsive sizing
        self.auto_dismiss = False
        self.background = ''  # Remove default background
        self.background_color = (1, 1, 1, 1)  # White background
        self.separator_color = (0.2, 0.6, 0.8, 1)  # Blue separator

        self.on_yes_callback = on_yes_callback

        # Create main layout with better spacing
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(20)
        )

        # Title as a Label inside content with black text
        title_label = Label(
            text=title_text,
            size_hint_y=None,
            height=dp(40),
            font_size=20,
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1),  # Black title text
            markup=True
        )
        apply_arabic_font(title_label, title_text)
        # Ensure proper alignment/wrapping
        from kivy.clock import Clock
        def set_title_text_size(dt):
            title_label.text_size = (self.width - dp(60), None)
        Clock.schedule_once(set_title_text_size, 0.05)

        main_layout.add_widget(title_label)

        # Message with better styling
        message_text = get_text(message_key, message_fallback)
        message_label = Label(
            text=message_text,
            text_size=(None, None),
            halign='center',
            valign='middle',
            color=(0.1, 0.1, 0.1, 1),  # Dark text for better readability
            font_size=16,
            markup=True
        )
        # Apply Arabic font if needed
        apply_arabic_font(message_label, message_text)

        # Set text_size after the widget is added to get proper wrapping
        def set_text_size(dt):
            message_label.text_size = (self.width - dp(60), None)
        Clock.schedule_once(set_text_size, 0.1)

        main_layout.add_widget(message_label)

        # Add some spacing
        main_layout.add_widget(Label(size_hint_y=None, height=dp(20)))

        # Buttons with improved design
        button_layout = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(20),
            padding=[dp(40), 0, dp(40), 0]  # Add horizontal padding
        )

        # No button with localized text
        no_text = get_text('no', 'No')
        no_btn = Button(
            text=no_text,
            font_size=18,
            background_color=(0.8, 0.3, 0.3, 1),  # Red color
            color=(1, 1, 1, 1),
            size_hint_x=0.5
        )
        apply_arabic_font(no_btn, no_text)
        no_btn.bind(on_press=self.dismiss)
        button_layout.add_widget(no_btn)

        # Yes button with localized text
        yes_text = get_text('yes', 'Yes')
        yes_btn = Button(
            text=yes_text,
            font_size=18,
            background_color=(0.3, 0.7, 0.3, 1),  # Green color
            color=(1, 1, 1, 1),
            size_hint_x=0.5
        )
        apply_arabic_font(yes_btn, yes_text)
        yes_btn.bind(on_press=self.on_yes)
        button_layout.add_widget(yes_btn)

        main_layout.add_widget(button_layout)
        self.content = main_layout

        # Keep the native title bar empty (we render title inside content)
        self.title = ''
        # Apply Arabic font to the popup widget (title handled above)
        apply_arabic_font(self, title_text)

    def on_yes(self, instance):
        """Handle yes button press."""
        self.dismiss()
        if self.on_yes_callback:
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
                    success_message = get_text('reset_success', f"Database has been reset successfully!\n\nLocation: {result}")
                    if backup_created:
                        success_message += f"\n\n{get_text('backup_saved', 'Previous database backed up to:')} \n{backup_path}"
                    self.show_message('success', success_message)
                else:
                    # Reconnect API even if failed
                    self.api.connect()
                    self.show_message('error', get_text('reset_failed', 'Failed to reset database. Please close the application completely and try again.\n\nThe database file might be locked by another process.'))

            except Exception as e:
                print(f"Error in create_fresh_database: {str(e)}")  # Debug
                # Ensure we reconnect even if there was an error
                try:
                    self.api.connect()
                except:
                    pass
                self.show_message('error', get_text('reset_failed', f"Failed to reset database: {str(e)}"))

        # Show confirmation dialog with localized content
        popup = ConfirmationPopup(
            title_key='reset_db_confirm_title',
            message_key='reset_db_confirm_message',
            title_fallback='Reset Database',
            message_fallback='Are you sure you want to reset the database?\n\nThis will:\n• Delete ALL existing data\n• Create a backup first\n• Create a fresh empty database\n\nContinue?',
            on_yes_callback=confirm_reset
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
                self.show_message('database_not_found', get_text('database_not_found', f"Database file not found at:\n{self.db_path}"))
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
                'export_success_title',
                get_text('export_success_message', f"Database exported successfully!\n\nFrom: {self.db_path}\n\nTo: {backup_path}\n\nBackup size: {os.path.getsize(backup_path)} bytes")
            )

        except Exception as e:
            print(f"Export error: {str(e)}")  # Debug
            self.show_message('export_error_title', get_text('export_failed', f"Failed to export database: {str(e)}"))

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
                    'seed_success',
                    get_text('seed_success_message', f"Database has been seeded with sample data!\n\nLocation: {self.db_path}\n\nExisting data has been preserved.")
                )

            except Exception as e:
                print(f"Seeding error: {str(e)}")  # Debug
                self.show_message('seed_error', get_text('seed_failed', f"Failed to seed database: {str(e)}"))

        # Show confirmation dialog with localized content
        popup = ConfirmationPopup(
            title_key='seed_db_confirm_title',
            message_key='seed_db_confirm_message',
            title_fallback='Seed Database',
            message_fallback='This will add sample data to your database.\nExisting data will be preserved.\n\nContinue?',
            on_yes_callback=confirm_seed
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
                self.show_message('file_not_found', get_text('file_not_found', 'Selected file does not exist.'))
                return

            # Check file size (optional - warn if very large)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            if file_size > 100:  # Warn if larger than 100MB
                self.show_message(
                    'large_file_warning',
                    get_text('large_file_warning_message', f"Selected file is {file_size:.1f}MB.\nThis might take some time to upload.")
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
                        'upload_success',
                        get_text('upload_success_message', f"Database has been replaced successfully!\n\nFile: {os.path.basename(file_path)}\nSize: {file_size:.1f}MB\n\nPrevious database backed up to:\n{backup_path}")
                    )

                except Exception as e:
                    print(f"Upload error: {str(e)}")  # Debug
                    self.show_message('upload_error', get_text('upload_failed', f"Failed to upload database: {str(e)}"))

            # Show confirmation for upload with localized content
            popup = ConfirmationPopup(
                title_key='upload_db_confirm_title',
                message_key='upload_db_confirm_message',
                title_fallback='Replace Database',
                message_fallback=f"Replace current database with:\n\nFile: {os.path.basename(file_path)}\nSize: {file_size:.1f}MB\nLocation: {file_path}\n\nThe current database will be backed up first.\n\nContinue?",
                on_yes_callback=confirm_upload
            )
            popup.open()

        except Exception as e:
            print(f"File chooser error: {str(e)}")  # Debug
            self.show_message('file_chooser_error_title', get_text('file_chooser_error', f"Failed to open file chooser: {str(e)}"))

    def show_message(self, title_key, message, title_fallback=None):
        """Show a message popup with improved design and localization."""
        # Get localized title
        if title_fallback is None:
            title_fallback = title_key
        title_text = get_text(title_key, title_fallback)

        # Create content layout
        content_layout = BoxLayout(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(20)
        )

        # Message label with better styling
        message_label = Label(
            text=message,
            text_size=(None, None),
            halign='center',
            valign='middle',
            color=(0.1, 0.1, 0.1, 1),  # Dark text
            font_size=16,
            markup=True
        )
        apply_arabic_font(message_label, message)
        content_layout.add_widget(message_label)

        # Close button
        close_text = get_text('close', 'Close')
        close_btn = Button(
            text=close_text,
            font_size=16,
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(50),
            size_hint_x=0.4,
            pos_hint={'center_x': 0.5}
        )
        apply_arabic_font(close_btn, close_text)

        popup = Popup(
            title=title_text,
            content=content_layout,
            size_hint=(0.7, 0.5),
            auto_dismiss=True,
            background='',  # Remove default background
            background_color=(1, 1, 1, 1),  # White background
            separator_color=(0.2, 0.6, 0.8, 1)  # Blue separator
        )

        # Apply Arabic font to title
        apply_arabic_font(popup, title_text)

        close_btn.bind(on_press=popup.dismiss)
        content_layout.add_widget(close_btn)

        # Set text_size after popup is created for proper text wrapping
        def set_text_size(dt):
            message_label.text_size = (popup.width - dp(60), None)
        from kivy.clock import Clock
        Clock.schedule_once(set_text_size, 0.1)

        popup.open()

    def go_to_main_gui(self, instance=None):
        """Navigate back to main GUI."""
        if hasattr(self.manager, 'current'):
            self.manager.current = 'main_gui'