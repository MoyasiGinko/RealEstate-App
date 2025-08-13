#!/usr/bin/env python3
"""
Test script to verify property-photo relationship is working correctly
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models.database_api import get_api
import tempfile
from PIL import Image

def create_test_image(filename, size=(100, 100), color='red'):
    """Create a simple test image"""
    img = Image.new('RGB', size, color=color)
    img.save(filename)
    return filename

def test_property_photo_relationship():
    """Test that property and photo codes match correctly"""
    api = get_api()

    # Connect to database
    if not api.connect():
        print("Failed to connect to database")
        return False

    # Set company code (should already be set, but just to be sure)
    api.set_company_code('E901')

    print("Testing property-photo relationship...")

    # Create test property data
    property_data = {
        'Rstatetcode': '03001',  # Residential
        'Buildtcode': '04001',   # Apartment
        'Yearmake': '2020',
        'Property-area': 150.0,
        'Unitm-code': '05001',   # Square meter
        'Property-facade': 10.0,
        'Property-depth': 15.0,
        'N-of-bedrooms': 3,
        'N-of-bathrooms': 2,
        'Property-corner': 'N',
        'Offer-Type-Code': '06001', # For Sale
        'Province-code': '01001',   # Baghdad
        'Region-code': '02001',     # Baghdad City
        'Property-address': 'Test Address 123',
        'Ownercode': 'A001',  # Assuming this owner exists
        'Descriptions': 'Test property for photo relationship verification'
    }

    # Add property to database
    print("Adding property to database...")
    property_code = api.add_property(property_data)

    if not property_code:
        print("Failed to add property")
        return False

    print(f"Property added with code: {property_code}")

    # Create temporary test images
    temp_dir = tempfile.mkdtemp()
    test_images = []

    try:
        for i, color in enumerate(['red', 'green', 'blue'], 1):
            img_path = os.path.join(temp_dir, f'test_image_{i}.png')
            create_test_image(img_path, color=color)
            test_images.append(img_path)
            print(f"Created test image: {img_path}")

        # Add photos to the property
        print(f"Adding {len(test_images)} photos to property {property_code}...")

        storage_dir = f"data/realstateimages/{property_code}"
        os.makedirs(storage_dir, exist_ok=True)

        for i, img_path in enumerate(test_images, 1):
            filename = f"test_photo_{i}.png"
            success = api.add_property_photo(
                property_code=property_code,
                file_path=storage_dir,
                photo_filename=filename,
                photo_extension='.png'
            )

            if success:
                print(f"Successfully added photo {filename} to property {property_code}")
            else:
                print(f"Failed to add photo {filename}")
                return False

        # Verify the relationship by checking the database
        print("\nVerifying property-photo relationship...")

        # Get property from database
        property_record = api.get_property_by_code(property_code)
        if not property_record:
            print(f"Property {property_code} not found in database!")
            return False

        print(f"Property found in database with code: {property_record.get('realstatecode')}")

        # Get photos for this property
        photos = api.get_property_photos(property_code)
        if not photos:
            print(f"No photos found for property {property_code}")
            return False

        print(f"Found {len(photos)} photos for property {property_code}:")

        for photo in photos:
            photo_property_code = photo.get('realstatecode')
            filename = photo.get('photofilename')
            print(f"  - Photo {filename} linked to property code: {photo_property_code}")

            if photo_property_code != property_code:
                print(f"ERROR: Photo {filename} is linked to {photo_property_code} but should be linked to {property_code}")
                return False

        print("\n✅ SUCCESS: All photos are correctly linked to the property!")
        print(f"Property code: {property_code}")
        print(f"All {len(photos)} photos reference the same property code: {property_code}")

        return True

    except Exception as e:
        print(f"Error during test: {e}")
        return False

    finally:
        # Cleanup
        import shutil
        try:
            shutil.rmtree(temp_dir)
            print(f"Cleaned up temporary directory: {temp_dir}")
        except:
            pass

if __name__ == "__main__":
    if test_property_photo_relationship():
        print("\n🎉 Property-photo relationship test PASSED!")
        sys.exit(0)
    else:
        print("\n❌ Property-photo relationship test FAILED!")
        sys.exit(1)
