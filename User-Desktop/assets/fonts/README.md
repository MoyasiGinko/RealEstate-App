# Font Directory

This directory contains font files for the Real Estate Management System.

## Required Fonts for Arabic Support

To enable full Arabic text support, please download and place the following fonts in this directory:

### Primary Arabic Fonts (Amiri Family)

- **Amiri-Regular.ttf** - Main Arabic font
- **Amiri-Bold.ttf** - Bold variant
- **Amiri-Italic.ttf** - Italic variant
- **Amiri-BoldItalic.ttf** - Bold italic variant

Download from: https://fonts.google.com/specimen/Amiri

### Fallback Arabic Fonts (Noto Sans Arabic)

- **NotoSansArabic-Regular.ttf** - Fallback regular
- **NotoSansArabic-Bold.ttf** - Fallback bold

Download from: https://fonts.google.com/specimen/Noto+Sans+Arabic

### English Fonts (Roboto Family) - Optional

- **Roboto-Regular.ttf** - English regular
- **Roboto-Bold.ttf** - English bold
- **Roboto-Italic.ttf** - English italic
- **Roboto-BoldItalic.ttf** - English bold italic

Download from: https://fonts.google.com/specimen/Roboto

## Installation Instructions

1. Download the font files from the links above
2. Copy all .ttf files to this directory
3. The font configuration system will automatically detect and register them
4. Restart the application to apply the changes

## Font Usage

The application will automatically:

- Use Arabic fonts for Arabic text
- Use English fonts for English text
- Use mixed fonts for content containing both languages

## File Structure

```
assets/fonts/
├── README.md                 (this file)
├── Amiri-Regular.ttf        (Arabic - Regular)
├── Amiri-Bold.ttf           (Arabic - Bold)
├── Amiri-Italic.ttf         (Arabic - Italic)
├── Amiri-BoldItalic.ttf     (Arabic - Bold Italic)
├── NotoSansArabic-Regular.ttf (Arabic Fallback - Regular)
├── NotoSansArabic-Bold.ttf    (Arabic Fallback - Bold)
├── Roboto-Regular.ttf       (English - Regular)
├── Roboto-Bold.ttf          (English - Bold)
├── Roboto-Italic.ttf        (English - Italic)
└── Roboto-BoldItalic.ttf    (English - Bold Italic)
```

## Troubleshooting

If fonts are not loading:

1. Check that font files exist in this directory
2. Verify file names match exactly (case-sensitive)
3. Ensure font files are not corrupted
4. Check the console for font registration messages
5. Restart the application after adding new fonts
