#!/usr/bin/env python3
"""
Test to verify the actual database pattern matching logic.
"""

# Test the pattern matching logic used in the database
def test_pattern_matching():
    print("=== Testing Pattern Matching Logic ===\n")

    # Sample cities (based on the observed data structure)
    cities = [
        {'code': '00101', 'name': 'Baghdad'},
        {'code': '00102', 'name': 'Basra'},
        {'code': '00103', 'name': 'Erbil'},
        {'code': '00201', 'name': 'Amman'},
        {'code': '00202', 'name': 'Zarqa'},
        {'code': '00301', 'name': 'Damascus'},
        {'code': '00302', 'name': 'Aleppo'},
        {'code': '00401', 'name': 'Beirut'},
        {'code': '00402', 'name': 'Tripoli'}
    ]

    provinces = [
        {'code': '001', 'name': 'Iraq'},
        {'code': '002', 'name': 'Jordan'},
        {'code': '003', 'name': 'Syria'},
        {'code': '004', 'name': 'Lebanon'}
    ]

    print("Available cities:")
    for city in cities:
        print(f"  {city['code']} - {city['name']}")
    print()

    # Test different pattern interpretations
    for province in provinces:
        province_code = province['code']
        province_name = province['name']

        print(f"Testing province: {province_code} - {province_name}")

        # Pattern 1: Database method pattern - '00' + province_code + '%'
        pattern1 = f"00{province_code}"
        matches1 = [city for city in cities if city['code'].startswith(pattern1)]
        print(f"  Pattern 1 ('00{province_code}*'): {len(matches1)} matches")
        for match in matches1:
            print(f"    - {match['code']} - {match['name']}")

        # Pattern 2: Remove first zero - '00' + province_code[1:] + '%'
        pattern2 = f"00{province_code[1:]}"
        matches2 = [city for city in cities if city['code'].startswith(pattern2)]
        print(f"  Pattern 2 ('00{province_code[1:]}*'): {len(matches2)} matches")
        for match in matches2:
            print(f"    - {match['code']} - {match['name']}")

        # Pattern 3: Direct province match in city code positions 2-4
        matches3 = [city for city in cities if len(city['code']) >= 5 and city['code'][2:5] == province_code]
        print(f"  Pattern 3 (province at pos 2-4): {len(matches3)} matches")
        for match in matches3:
            print(f"    - {match['code']} - {match['name']}")

        print()

if __name__ == "__main__":
    test_pattern_matching()
