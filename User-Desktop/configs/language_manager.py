#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Language Manager for Real Estate Management System
Handles localization and language switching between English and Arabic
"""

import json
import os
from configs.arabic_fonts import apply_arabic_font

class LanguageManager:
    """Manages application localization and language switching"""

    def __init__(self):
        self.current_language = 'en'  # Default to English
        self.translations = {}
        self.observers = []  # Screens that need to be notified of language changes
        self._load_translations()

    def _load_translations(self):
        """Load translation data"""
        self.translations = {
            'en': {
                # Main Screen
                'company_name': 'Al-Kawaz Software and Information Technology',
                'app_title': 'Real Estate Management System',
                'tagline': 'Real Estate in all Aspects',
                'subtitle': 'Professional • Reliable • Innovative',
                'choose_action': 'Choose Your Action',
                'new_property': 'New Property',
                'update_property': 'Update Property',
                'browse_property': 'Browse Property',
                'upload_property': 'Upload Property',
                'about': 'About',
                'exit': 'Exit',
                'language': 'Language',

                # Browse Screen
                'property_search_reports': 'Property Search & Reports',
                'search_criteria': 'Search Criteria',
                'property_type': 'Property Type',
                'building_type': 'Building Type',
                'min_bedrooms': 'Min Bedrooms',
                'max_bedrooms': 'Max Bedrooms',
                'min_price': 'Min Price',
                'max_price': 'Max Price',
                'corner_property': 'Corner Property',
                'search': 'Search',
                'clear_search': 'Clear Search',
                'export_results': 'Export Results',
                'go_back': 'Go Back',
                'search_results': 'Search Results',
                'all_types': 'All Types',
                'no_results_found': 'No properties found matching your criteria.',
                'no_results_to_export': 'No results to export',

                # Insert Screen
                'add_new_property': 'Add New Property',
                'property_code': 'Property Code',
                'year_construction': 'Year of Construction',
                'unit_measurement': 'Unit of Measurement',
                'facade': 'Facade',
                'depth': 'Depth',
                'floors': 'Floors/Levels',
                'area': 'Area',
                'bedrooms': 'Bedrooms',
                'bathrooms': 'Bathrooms',
                'corner': 'Corner?',
                'yes': 'Yes',
                'no': 'No',
                'confirm_delete_message': 'Are you sure you want to delete this property?\nThis will also delete all associated photos.',
                'offer_type': 'Offer Type',
                'governorate': 'Governorate/Province',
                'neighborhood': 'Area/Neighborhood',
                'address': 'Property Address',
                'price': 'Price',
                'owner': 'Property Owner',
                'phone': 'Phone Number',
                'photos': 'Photos',
                'add_photo': 'Add Photo',
                'notes': 'Notes',
                'required_fields': '* Required fields',
                'back': 'Back',
                'clear_form': 'Clear Form',
                'save_property': 'Save Property',

                # About Screen
                'about_us': 'About Us',
                'company_name_full': 'Al-Kawaz Software and Information Technology',
                'version': 'Version: 1.0.0',
                'author': 'Author: Luay Alkawaz',
                'description': 'This application helps users manage real estate properties efficiently and intuitively.\nProfessional • Reliable • Innovative\nThank you for using our system!',
                'back_to_main': 'Back to Main',

                # Upload Screen
                'database_management': 'Database Management',
                'db_description': 'Manage your database: reset, backup, seed with sample data, or upload a new database file',
                'reset_database': 'Reset Database',
                'export_database': 'Export Database',
                'seed_database': 'Seed Database',
                'upload_database': 'Upload Database',
                'reset_db_desc': 'Create a fresh empty database\n(Deletes all existing data)',
                'export_db_desc': 'Create a backup copy of\nyour current database',
                'seed_db_desc': 'Add sample data to database\n(Preserves existing data)',
                'upload_db_desc': 'Replace current database\nwith a new file',

                # Modal Messages
                'reset_db_confirm_title': 'Reset Database',
                'reset_db_confirm_message': 'Are you sure you want to reset the database?\n\nThis will:\n• Delete ALL existing data\n• Create a backup first\n• Create a fresh empty database\n\nContinue?',
                'seed_db_confirm_title': 'Seed Database',
                'seed_db_confirm_message': 'This will add sample data to your database.\nExisting data will be preserved.\n\nContinue?',
                'upload_db_confirm_title': 'Replace Database',
                'upload_db_confirm_message': 'Replace current database with the selected file?\n\nThe current database will be backed up first.\n\nContinue?',
                'export_success_title': 'Export Successful',
                'export_error_title': 'Export Error',
                'backup_failed_title': 'Backup Failed',
                'backup_failed_message': 'Failed to create backup of current database.\n\nDo you want to continue with reset anyway?\n\nWarning: This will permanently delete all data!',
                'file_chooser_error_title': 'File Chooser Error',
                'database_not_found': 'Database file not found',
                'file_not_found': 'Selected file does not exist',
                'large_file_warning': 'Warning: Large file size detected',
                'reset_success': 'Database Reset Successfully',
                'reset_failed': 'Failed to Reset Database',
                'backup_saved': 'Previous database backed up to:',
                'seed_success': 'Seeding Successful',
                'seed_failed': 'Failed to Seed Database',
                'seed_success_message': 'Database has been seeded with sample data successfully!',
                'export_success_message': 'Database exported successfully!',
                'export_failed': 'Failed to export database',
                'large_file_warning_message': 'Selected file is large and might take some time to upload',
                'upload_success': 'Upload Successful',
                'upload_error': 'Upload Error',
                'upload_failed': 'Failed to upload database',
                'upload_success_message': 'Database has been replaced successfully!',
                'file_chooser_error': 'Failed to open file chooser',

                # Update Screen
                'property_management': 'Property Management',
                'code': 'Code',
                'type': 'Type',
                'owner_name': 'Owner',
                'actions': 'Actions',

                # Property Form Fields
                'property_form': 'Property Form',
                'select_property_type': 'Select Property Type',
                'select_building_type': 'Select Building Type',
                'select_year': 'Select Year',
                'property_area_hint': 'Property Area',
                'facade_length_hint': 'Facade Length',
                'property_depth_hint': 'Property Depth',
                'num_bedrooms_hint': 'Number of Bedrooms',
                'num_bathrooms_hint': 'Number of Bathrooms',
                'is_corner_property': 'Is Corner Property',
                'select_offer_type': 'Select Offer Type',
                'select_province': 'Select Province',
                'select_region': 'Select Region',
                'property_address_hint': 'Property Address',
                'select_owner': 'Select Owner',
                'add_new_owner': 'Add New Owner',
                'property_description_hint': 'Property Description/Notes',
                'num_floors_hint': 'Number of Floors',
                'property_price_hint': 'Property Price',
                'select_currency': 'Select Currency',
                'select_unit': 'Select Unit',
                'select_photos': 'Select Photos',
                'no_photos_selected': 'No photos selected',
                'photos_selected': 'photos selected',
                'photo_selected': 'photo selected',
                'add_photos': 'Add Photos',

                # Validation Messages
                'property_type_required': 'Property type is required.',
                'building_type_required': 'Building type is required.',
                'area_required': 'Property area is required.',
                'owner_required': 'Owner is required.',
                'property_updated': 'Property updated successfully!',
                'property_deleted': 'Property and all its photos deleted successfully!',
                'property_not_found': 'Property not found in database.',
                'update_failed': 'Failed to update property. Please try again.',
                'delete_failed': 'Failed to delete property. Please try again.',

                # Modal Titles
                'edit_property': 'Edit Property',
                'add_new_owner_title': 'Add New Owner',
                'confirm_delete': 'Confirm Delete',

                # Common
                'save': 'Save',
                'cancel': 'Cancel',
                'close': 'Close',
                'view': 'View',
                'edit': 'Edit',
                'delete': 'Delete',
                'loading': 'Loading...',
                'error': 'Error',
                'success': 'Success',
                'warning': 'Warning',
                'info': 'Information',
            },
            'ar': {
                # Main Screen
                'company_name': 'الكواز للبرمجيات وتقنية المعلومات',
                'app_title': 'نظام إدارة العقارات',
                'tagline': 'العقارات بجميع جوانبها',
                'subtitle': 'مهني • موثوق • مبتكر',
                'choose_action': 'اختر العملية',
                'new_property': 'عقار جديد',
                'update_property': 'تحديث العقار',
                'browse_property': 'تصفح العقارات',
                'upload_property': 'رفع العقار',
                'about': 'حول',
                'exit': 'خروج',
                'language': 'اللغة',

                # Browse Screen
                'property_search_reports': 'البحث عن العقارات والتقارير',
                'search_criteria': 'معايير البحث',
                'property_type': 'نوع العقار',
                'building_type': 'نوع البناء',
                'min_bedrooms': 'أقل عدد غرف النوم',
                'max_bedrooms': 'أكثر عدد غرف النوم',
                'min_price': 'أقل سعر',
                'max_price': 'أعلى سعر',
                'corner_property': 'عقار زاوية',
                'search': 'بحث',
                'clear_search': 'مسح البحث',
                'export_results': 'تصدير النتائج',
                'go_back': 'العودة',
                'search_results': 'نتائج البحث',
                'all_types': 'جميع الأنواع',
                'no_results_found': 'لم يتم العثور على عقارات تطابق معاييرك.',
                'no_results_to_export': 'لا توجد نتائج للتصدير',
                'no_results_to_export': 'لا توجد نتائج للتصدير',

                # Insert Screen
                'add_new_property': 'إضافة عقار جديد',
                'property_code': 'رمز العقار',
                'year_construction': 'سنة البناء',
                'unit_measurement': 'وحدة القياس',
                'facade': 'الواجهة',
                'depth': 'العمق',
                'floors': 'عدد الطوابق',
                'area': 'المساحة',
                'bedrooms': 'غرف النوم',
                'bathrooms': 'دورات المياه',
                'corner': 'زاوية؟',
                'yes': 'نعم',
                'no': 'لا',
                'confirm_delete_message': 'هل أنت متأكد من حذف هذا العقار؟\nسيتم حذف جميع الصور المرتبطة أيضاً.',
                'offer_type': 'نوع العرض',
                'governorate': 'المحافظة',
                'neighborhood': 'المنطقة/الحي',
                'address': 'عنوان العقار',
                'price': 'السعر',
                'owner': 'مالك العقار',
                'phone': 'رقم الهاتف',
                'photos': 'الصور',
                'add_photo': 'إضافة صورة',
                'notes': 'ملاحظات',
                'required_fields': '* حقول مطلوبة',
                'back': 'رجوع',
                'clear_form': 'مسح النموذج',
                'save_property': 'حفظ العقار',

                # About Screen
                'about_us': 'معلومات عنا',
                'company_name_full': 'الكواز للبرمجيات وتقنية المعلومات',
                'version': 'الإصدار: 1.0.0',
                'author': 'المؤلف: لؤي الكواز',
                'description': 'هذا التطبيق يساعد المستخدمين على إدارة العقارات بكفاءة وسهولة.\nمهني • موثوق • مبتكر\nشكراً لاستخدام نظامنا!',
                'back_to_main': 'العودة للرئيسية',

                # Upload Screen
                'database_management': 'إدارة قاعدة البيانات',
                'db_description': 'إدارة قاعدة البيانات: إعادة تعيين، نسخ احتياطي، إضافة بيانات تجريبية، أو رفع ملف قاعدة بيانات جديد',
                'reset_database': 'إعادة تعيين قاعدة البيانات',
                'export_database': 'تصدير قاعدة البيانات',
                'seed_database': 'إضافة بيانات تجريبية',
                'upload_database': 'رفع قاعدة البيانات',
                'reset_db_desc': 'إنشاء قاعدة بيانات فارغة جديدة\n(حذف جميع البيانات الموجودة)',
                'export_db_desc': 'إنشاء نسخة احتياطية من\nقاعدة البيانات الحالية',
                'seed_db_desc': 'إضافة بيانات تجريبية للقاعدة\n(الاحتفاظ بالبيانات الموجودة)',
                'upload_db_desc': 'استبدال قاعدة البيانات الحالية\nبملف جديد',

                # Modal Messages
                'reset_db_confirm_title': 'إعادة تعيين قاعدة البيانات',
                'reset_db_confirm_message': 'هل أنت متأكد من إعادة تعيين قاعدة البيانات؟\n\nسيتم:\n• حذف جميع البيانات الموجودة\n• إنشاء نسخة احتياطية أولاً\n• إنشاء قاعدة بيانات فارغة جديدة\n\nالمتابعة؟',
                'seed_db_confirm_title': 'إضافة بيانات تجريبية',
                'seed_db_confirm_message': 'سيتم إضافة بيانات تجريبية لقاعدة البيانات.\nسيتم الاحتفاظ بالبيانات الموجودة.\n\nالمتابعة؟',
                'upload_db_confirm_title': 'استبدال قاعدة البيانات',
                'upload_db_confirm_message': 'استبدال قاعدة البيانات الحالية بالملف المحدد؟\n\nسيتم إنشاء نسخة احتياطية من قاعدة البيانات الحالية أولاً.\n\nالمتابعة؟',
                'export_success_title': 'تم التصدير بنجاح',
                'export_error_title': 'خطأ في التصدير',
                'backup_failed_title': 'فشل في النسخ الاحتياطي',
                'backup_failed_message': 'فشل في إنشاء نسخة احتياطية من قاعدة البيانات الحالية.\n\nهل تريد المتابعة مع إعادة التعيين على أي حال؟\n\nتحذير: سيتم حذف جميع البيانات نهائياً!',
                'file_chooser_error_title': 'خطأ في محدد الملفات',
                'database_not_found': 'ملف قاعدة البيانات غير موجود',
                'file_not_found': 'الملف المحدد غير موجود',
                'large_file_warning': 'تحذير: تم اكتشاف حجم ملف كبير',
                'reset_success': 'تم إعادة تعيين قاعدة البيانات بنجاح',
                'reset_failed': 'فشل في إعادة تعيين قاعدة البيانات',
                'backup_saved': 'تم حفظ قاعدة البيانات السابقة في:',
                'seed_success': 'تم إضافة البيانات التجريبية بنجاح',
                'seed_failed': 'فشل في إضافة البيانات التجريبية',
                'seed_success_message': 'تم إضافة البيانات التجريبية لقاعدة البيانات بنجاح!',
                'export_success_message': 'تم تصدير قاعدة البيانات بنجاح!',
                'export_failed': 'فشل في تصدير قاعدة البيانات',
                'large_file_warning_message': 'الملف المحدد كبير وقد يستغرق بعض الوقت للرفع',
                'upload_success': 'تم الرفع بنجاح',
                'upload_error': 'خطأ في الرفع',
                'upload_failed': 'فشل في رفع قاعدة البيانات',
                'upload_success_message': 'تم استبدال قاعدة البيانات بنجاح!',
                'file_chooser_error': 'فشل في فتح محدد الملفات',

                # Update Screen
                'property_management': 'إدارة العقارات',
                'code': 'الرمز',
                'type': 'النوع',
                'owner_name': 'المالك',
                'actions': 'العمليات',

                # Property Form Fields
                'property_form': 'نموذج العقار',
                'select_property_type': 'اختر نوع العقار',
                'select_building_type': 'اختر نوع البناء',
                'select_year': 'اختر السنة',
                'property_area_hint': 'مساحة العقار',
                'facade_length_hint': 'طول الواجهة',
                'property_depth_hint': 'عمق العقار',
                'num_bedrooms_hint': 'عدد غرف النوم',
                'num_bathrooms_hint': 'عدد دورات المياه',
                'is_corner_property': 'عقار زاوية',
                'select_offer_type': 'اختر نوع العرض',
                'select_province': 'اختر المحافظة',
                'select_region': 'اختر المنطقة',
                'property_address_hint': 'عنوان العقار',
                'select_owner': 'اختر المالك',
                'add_new_owner': 'إضافة مالك جديد',
                'property_description_hint': 'وصف العقار/الملاحظات',
                'num_floors_hint': 'عدد الطوابق',
                'property_price_hint': 'سعر العقار',
                'select_currency': 'اختر العملة',
                'select_unit': 'اختر الوحدة',
                'select_photos': 'اختر الصور',
                'no_photos_selected': 'لم يتم اختيار صور',
                'photos_selected': 'صورة محددة',
                'photo_selected': 'صورة واحدة محددة',
                'add_photos': 'إضافة صور',

                # Validation Messages
                'property_type_required': 'نوع العقار مطلوب.',
                'building_type_required': 'نوع البناء مطلوب.',
                'area_required': 'مساحة العقار مطلوبة.',
                'owner_required': 'المالك مطلوب.',
                'property_updated': 'تم تحديث العقار بنجاح!',
                'property_deleted': 'تم حذف العقار وجميع صوره بنجاح!',
                'property_not_found': 'العقار غير موجود في قاعدة البيانات.',
                'update_failed': 'فشل في تحديث العقار. يرجى المحاولة مرة أخرى.',
                'delete_failed': 'فشل في حذف العقار. يرجى المحاولة مرة أخرى.',

                # Modal Titles
                'edit_property': 'تعديل العقار',
                'add_new_owner_title': 'إضافة مالك جديد',
                'confirm_delete': 'تأكيد الحذف',

                # Common
                'save': 'حفظ',
                'cancel': 'إلغاء',
                'close': 'إغلاق',
                'view': 'عرض',
                'edit': 'تعديل',
                'delete': 'حذف',
                'loading': 'جاري التحميل...',
                'error': 'خطأ',
                'success': 'نجح',
                'warning': 'تحذير',
                'info': 'معلومات',
            }
        }

    def get_text(self, key, fallback=None):
        """Get translated text for the current language"""
        if fallback is None:
            fallback = key

        return self.translations.get(self.current_language, {}).get(key, fallback)

    def set_language(self, language_code):
        """Set the current language and notify observers"""
        if language_code in self.translations:
            self.current_language = language_code
            self._notify_language_change()
            print(f"Language switched to: {language_code}")

    def get_current_language(self):
        """Get the current language code"""
        return self.current_language

    def is_rtl(self):
        """Check if current language is right-to-left"""
        return self.current_language == 'ar'

    def register_observer(self, observer):
        """Register a screen to be notified of language changes"""
        if observer not in self.observers:
            self.observers.append(observer)

    def unregister_observer(self, observer):
        """Unregister a screen from language change notifications"""
        if observer in self.observers:
            self.observers.remove(observer)

    def _notify_language_change(self):
        """Notify all registered observers of language change"""
        for observer in self.observers[:]:  # Copy list to avoid modification during iteration
            if hasattr(observer, 'on_language_changed'):
                try:
                    observer.on_language_changed()
                except Exception as e:
                    print(f"Error notifying observer {observer}: {e}")

    def apply_font_and_text(self, widget, text_key, fallback_text=None):
        """Apply text and Arabic font if needed"""
        text = self.get_text(text_key, fallback_text or text_key)
        widget.text = text
        if self.current_language == 'ar':
            apply_arabic_font(widget, text)

# Global language manager instance
_language_manager = None

def get_language_manager():
    """Get the global language manager instance"""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager

def get_text(key, fallback=None):
    """Convenience function to get translated text"""
    return get_language_manager().get_text(key, fallback)

def set_language(language_code):
    """Convenience function to set language"""
    get_language_manager().set_language(language_code)

def apply_localization(widget, text_key, fallback_text=None):
    """Convenience function to apply localization to a widget"""
    get_language_manager().apply_font_and_text(widget, text_key, fallback_text)
