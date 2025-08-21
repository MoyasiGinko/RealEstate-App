# Arabic Font Support - Production Setup

## Overview

Clean, production-ready Arabic font support for the Real Estate Management System.

## Files Structure

```
configs/
  arabic_fonts.py          # Main Arabic font configuration
assets/
  fonts/
    Amiri-Regular.ttf      # Arabic font (regular)
    Amiri-Bold.ttf         # Arabic font (bold)
```

## Usage

### 1. Initialize Fonts (Done in main.py)

```python
from configs.arabic_fonts import init_arabic_fonts

# In your app's build() method
init_arabic_fonts()
```

### 2. Apply Arabic Fonts to Widgets

#### Automatic Detection

```python
from configs.arabic_fonts import apply_arabic_font

# This will automatically detect Arabic text and apply font
apply_arabic_font(widget, "Hello مرحبا")
```

#### Create Widgets with Arabic Support

```python
from configs.arabic_fonts import create_arabic_label, create_arabic_button, create_arabic_textinput

# These automatically handle Arabic text
label = create_arabic_label("Welcome - مرحبا بك")
button = create_arabic_button("Save - حفظ")
text_input = create_arabic_textinput("Type here - اكتب هنا")
```

### 3. Update Existing Screens

To add Arabic support to any screen, add this to the screen's `__init__` method:

```python
from configs.arabic_fonts import apply_arabic_font

class YourScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_enter=self.setup_arabic_fonts)

    def setup_arabic_fonts(self, *args):
        """Apply Arabic fonts to all text widgets"""
        for widget in self.walk(restrict=True):
            if hasattr(widget, 'text') and widget.text:
                apply_arabic_font(widget, widget.text)
```

## Arabic Text Examples

- English: "Welcome to our application"
- Arabic: "مرحباً بكم في تطبيقنا"
- Mixed: "Welcome مرحباً - Real Estate عقارات"

## Testing

The About screen now shows both English and Arabic text to demonstrate the functionality.
