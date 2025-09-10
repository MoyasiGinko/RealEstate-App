import os
import sys

# Ensure repository root is on sys.path so `src` imports work
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Also ensure 'src' package imports work (some modules import via 'screens' etc.)
SRC_PATH = os.path.join(REPO_ROOT, 'src')
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from src.main import MainApp
from kivy.clock import Clock
import re

class SmokeApp(MainApp):
    def on_start(self):
        # run tests shortly after start
        Clock.schedule_once(self.run_tests, 0.5)

    def run_tests(self, dt):
        issues = []
        # Ensure language is Arabic for RTL test
        try:
            self.language_manager.set_language('ar')
        except Exception as e:
            issues.append(f"Failed to set language to ar: {e}")

        # Screens
        try:
            insert = self.sm.get_screen('insert_gui')
            # Call load methods
            try:
                insert.load_property_types()
                insert.load_provinces()
                insert.load_owners()
            except Exception as e:
                issues.append(f"Insert screen load error: {e}")

            # Check spinners
            def has_arabic(values):
                for v in values or []:
                    if re.search(r'[\u0600-\u06FF]', str(v)):
                        return True
                return False

            try:
                if hasattr(insert, 'property_type') and insert.property_type:
                    if not has_arabic(getattr(insert.property_type, 'values', [])):
                        issues.append('Insert.property_type has no Arabic in values')
                if hasattr(insert, 'governorate') and insert.governorate:
                    if not has_arabic(getattr(insert.governorate, 'values', [])):
                        issues.append('Insert.governorate has no Arabic in values')
            except Exception as e:
                issues.append(f"Insert spinner check error: {e}")

            browse = self.sm.get_screen('browse_gui')
            try:
                browse.load_property_types()
                browse.load_building_types()
            except Exception as e:
                issues.append(f"Browse load error: {e}")
            try:
                pvals = getattr(browse.ids.property_type_spinner, 'values', []) if hasattr(browse, 'ids') and getattr(browse.ids, 'property_type_spinner', None) else []
                if not has_arabic(pvals):
                    issues.append('Browse.property_type_spinner has no Arabic in values')
            except Exception as e:
                issues.append(f"Browse spinner check error: {e}")

            update = self.sm.get_screen('update_gui')
            try:
                provs = update.api.get_provinces() or []
                if provs:
                    first = f"{provs[0]['code']} - {provs[0]['name']}"
                    # Call province-selected handler: it may live on the screen or on a child (PropertyForm)
                    handled = False
                    try:
                        if hasattr(update, 'on_province_selected'):
                            update.on_province_selected(None, first)
                            handled = True
                    except Exception:
                        handled = False

                    if not handled:
                        # search children for a handler
                        for child in update.walk():
                            if hasattr(child, 'on_province_selected'):
                                try:
                                    child.on_province_selected(None, first)
                                    handled = True
                                    break
                                except Exception:
                                    continue

                    if not handled:
                        issues.append('Update region test error: no on_province_selected handler found')
                    else:
                        rvals = getattr(update, 'region_spinner', None) or None
                        if not rvals:
                            # maybe the handler populated a child spinner; search for a spinner named 'region'
                            for child in update.walk():
                                if getattr(child, 'id', None) == 'region' or getattr(child, 'name', None) == 'region':
                                    rvals = child
                                    break

                        if rvals:
                            vals = getattr(rvals, 'values', [])
                            if not has_arabic(vals):
                                issues.append('Update.region_spinner has no Arabic in values')
            except Exception as e:
                issues.append(f"Update region test error: {e}")

        except Exception as e:
            issues.append(f"General test failure: {e}")

        # Print results
        if issues:
            print('\nSMOKE TEST FOUND ISSUES:')
            for it in issues:
                print('-', it)
        else:
            print('\nSMOKE TEST PASSED: No obvious untranslated/unshaped spinner values found')

        # Stop the app
        Clock.schedule_once(lambda dt: self.stop(), 0.5)

if __name__ == '__main__':
    SmokeApp().run()
