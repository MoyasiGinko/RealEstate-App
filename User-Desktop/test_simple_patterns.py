#!/usr/bin/env python3
"""
Test to find the correct pattern for province-city matching
"""

def test_simple_patterns():
    print("=== Testing Simple Pattern Matching ===\n")

    # Sample cities
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

    provinces = ['001', '002', '003', '004']

    print("Testing various patterns:")
    print()

    for province_code in provinces:
        print(f"Province: {province_code}")

        # Try different patterns
        patterns_to_test = [
            (f"{province_code}", "Direct match"),
            (f"00{province_code}", "00 + province"),
            (f"00{province_code[2:]}", "00 + last digit"),  # 001 -> 001, take last digit -> 1, so 001
            (f"00{province_code[1:]}", "00 + last 2 digits"),  # 001 -> 01, so 0001
        ]

        for pattern, description in patterns_to_test:
            matches = [city for city in cities if city['code'].startswith(pattern)]
            print(f"  {description} ('{pattern}'): {len(matches)} matches")
            for match in matches:
                print(f"    - {match['code']} - {match['name']}")

        # Special test: check if city code contains province digits in specific positions
        # City: 00101, Province: 001 - maybe positions 2,3,4 of city match province?
        # City: 00101 -> positions [0,0,1,0,1] -> [2,3,4] = [1,0,1] vs province 001? No.
        # Maybe: 00101 -> skip 00, get 101 -> first digit 1 matches last digit of 001? No.
        # Maybe: 00101 -> skip 00, get 101 -> 1 means province 1 -> which is 001? Let's try!

        province_last_digit = province_code[-1]  # '001' -> '1'
        city_indicator = f"00{province_last_digit}"  # '1' -> '001'
        matches_special = [city for city in cities if len(city['code']) >= 4 and city['code'][2] == province_last_digit]
        print(f"  Last digit match (city[2] == '{province_last_digit}'): {len(matches_special)} matches")
        for match in matches_special:
            print(f"    - {match['code']} - {match['name']}")

        print()

if __name__ == "__main__":
    test_simple_patterns()
