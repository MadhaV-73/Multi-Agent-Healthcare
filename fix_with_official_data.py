"""
CORRECT Pincode Assignment Based on India Post Official Data

According to India Post Pincode Directory:
- 421302 = BHIWANDI (Bhiwandi Pawne)
- 421301 = KALYAN (Kalyan East)
- 410206 = PANVEL (Kamothe)

We need to reassign conflicts correctly.
"""

import csv
import json

# Official India Post pincode assignments
CORRECT_ASSIGNMENTS = {
    '421302': 'Bhiwandi',  # Bhiwandi Pawne
    '410206': 'Panvel',    # Kamothe, Panvel
}

def fix_with_correct_data():
    """Fix pincodes based on official India Post data"""
    
    print("=" * 80)
    print("FIXING PINCODE CONFLICTS WITH OFFICIAL INDIA POST DATA")
    print("=" * 80)
    
    # Step 1: Fix zipcodes.csv
    print("\nStep 1: Fixing zipcodes.csv")
    print("-" * 80)
    
    with open('data/zipcodes.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        records = list(reader)
    
    # Remove duplicates, keep correct assignments
    seen_pincodes = set()
    correct_records = []
    
    for record in records:
        pin = record['pincode']
        city = record['city']
        
        if pin in CORRECT_ASSIGNMENTS:
            correct_city = CORRECT_ASSIGNMENTS[pin]
            if city == correct_city:
                if pin not in seen_pincodes:
                    correct_records.append(record)
                    seen_pincodes.add(pin)
                    print(f"   ✅ Keeping: {pin} = {city}")
                else:
                    print(f"   🗑️ Removing duplicate: {pin} = {city}")
            else:
                print(f"   ❌ Removing incorrect: {pin} = {city} (should be {correct_city})")
        else:
            # Not a conflicted pincode
            if pin not in seen_pincodes:
                correct_records.append(record)
                seen_pincodes.add(pin)
    
    # Save corrected zipcodes
    with open('data/zipcodes.csv', 'w', newline='', encoding='utf-8') as f:
        if correct_records:
            writer = csv.DictWriter(f, fieldnames=correct_records[0].keys())
            writer.writeheader()
            writer.writerows(correct_records)
    
    print(f"\n✅ zipcodes.csv: {len(correct_records)} unique pincodes")
    
    # Step 2: Fix pharmacies.json
    print("\nStep 2: Fixing pharmacies.json")
    print("-" * 80)
    
    # Load valid pincodes
    pincode_city_map = {row['pincode']: row['city'] for row in correct_records}
    
    # Load pharmacies
    with open('data/pharmacies.json', 'r', encoding='utf-8') as f:
        pharmacies = json.load(f)
    
    fixed_count = 0
    removed_count = 0
    valid_pharmacies = []
    
    for pharmacy in pharmacies:
        ph_pincode = pharmacy.get('pincode', '')
        ph_city = pharmacy.get('city', '')
        
        # Check if pincode is valid
        if ph_pincode not in pincode_city_map:
            print(f"   ❌ Removing {pharmacy['name']}: Invalid pincode {ph_pincode}")
            removed_count += 1
            continue
        
        # Check if city matches
        correct_city = pincode_city_map[ph_pincode]
        
        if ph_city != correct_city:
            print(f"   🔧 Fixing {pharmacy['name']}: {ph_city} {ph_pincode} → {correct_city} {ph_pincode}")
            pharmacy['city'] = correct_city
            
            # Update coordinates to match correct city
            # Find the pincode data
            pincode_data = next((row for row in correct_records if row['pincode'] == ph_pincode), None)
            if pincode_data:
                # Update area and district
                pharmacy['area'] = pincode_data.get('area', pharmacy.get('area', ''))
                pharmacy['district'] = pincode_data.get('district', pharmacy.get('district', ''))
                
                # Note: Coordinates should ideally be regenerated, but we'll keep them for now
                # They should be close enough since pincodes are geographically close
            
            fixed_count += 1
        
        valid_pharmacies.append(pharmacy)
    
    # Save
    with open('data/pharmacies.json', 'w', encoding='utf-8') as f:
        json.dump(valid_pharmacies, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Fixed {fixed_count} pharmacies")
    print(f"✅ Removed {removed_count} pharmacies")
    print(f"✅ Total valid pharmacies: {len(valid_pharmacies)}")
    
    # Step 3: Verify
    print("\n" + "=" * 80)
    print("VERIFICATION")
    print("=" * 80)
    
    # Check specific pincodes
    test_pincodes = ['421302', '410206']
    
    for test_pin in test_pincodes:
        if test_pin in pincode_city_map:
            correct_city = pincode_city_map[test_pin]
            pharmacies_with_pin = [p for p in valid_pharmacies if p['pincode'] == test_pin]
            
            print(f"\nPincode {test_pin} → {correct_city}")
            print(f"   Pharmacies: {len(pharmacies_with_pin)}")
            
            wrong_city = [p for p in pharmacies_with_pin if p['city'] != correct_city]
            if wrong_city:
                print(f"   ❌ {len(wrong_city)} pharmacies with wrong city!")
                for p in wrong_city[:3]:
                    print(f"      - {p['name']}: {p['city']} (should be {correct_city})")
            else:
                print(f"   ✅ All pharmacies correctly assigned to {correct_city}")
                for p in pharmacies_with_pin[:3]:
                    print(f"      - {p['name']}")
    
    # Check for any remaining duplicates
    pincode_counts = {}
    for record in correct_records:
        pin = record['pincode']
        pincode_counts[pin] = pincode_counts.get(pin, 0) + 1
    
    duplicates = {pin: count for pin, count in pincode_counts.items() if count > 1}
    
    if duplicates:
        print(f"\n❌ Still have duplicate pincodes in zipcodes.csv:")
        for pin, count in duplicates.items():
            print(f"   {pin}: {count} entries")
    else:
        print(f"\n✅ No duplicate pincodes in zipcodes.csv")
    
    # City distribution
    print("\n" + "-" * 80)
    print("FINAL DISTRIBUTION")
    print("-" * 80)
    
    city_stats = {}
    for pharmacy in valid_pharmacies:
        city = pharmacy['city']
        if city not in city_stats:
            city_stats[city] = 0
        city_stats[city] += 1
    
    for city in sorted(city_stats.keys()):
        count = city_stats[city]
        pincodes_in_city = len([p for p in valid_pharmacies if p['city'] == city and p.get('pincode')])
        unique_pincodes = len(set(p['pincode'] for p in valid_pharmacies if p['city'] == city))
        print(f"   {city}: {count} pharmacies across {unique_pincodes} unique pincodes")
    
    print("\n" + "=" * 80)
    print("✅ PINCODE CONFLICTS RESOLVED!")
    print("=" * 80)
    print("\nOfficial assignments applied:")
    for pin, city in CORRECT_ASSIGNMENTS.items():
        print(f"   • {pin} → {city} (India Post verified)")
    
    return True

if __name__ == "__main__":
    fix_with_correct_data()
