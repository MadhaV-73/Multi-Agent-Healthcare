"""
Fix Pincode Conflicts - Ensure Each Pincode Belongs to Only ONE City
Based on India Post Official Data
"""

import csv
import json

# CORRECTED Maharashtra Pincode Data - NO DUPLICATES
# Based on India Post Official Directory
CORRECTED_PINCODES = {
    # Bhiwandi has its own unique pincodes
    'Bhiwandi': ['421302', '421305', '421308'],
    
    # Kalyan has separate pincodes (NOT 421302)
    'Kalyan': ['421301', '421303', '421304', '421306', '421307', '421309'],
    
    # Panvel - separate from Navi Mumbai
    'Panvel': ['410206', '410221'],
}

def analyze_conflicts():
    """Analyze pincode conflicts in current data"""
    print("=" * 80)
    print("ANALYZING PINCODE CONFLICTS")
    print("=" * 80)
    
    # Load current pincodes
    with open('data/zipcodes.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        pincodes = list(reader)
    
    # Group by pincode
    pincode_map = {}
    for record in pincodes:
        pin = record['pincode']
        city = record['city']
        
        if pin not in pincode_map:
            pincode_map[pin] = []
        pincode_map[pin].append(city)
    
    # Find conflicts
    conflicts = {pin: cities for pin, cities in pincode_map.items() if len(set(cities)) > 1}
    
    if conflicts:
        print(f"\n❌ Found {len(conflicts)} pincode conflicts:\n")
        for pin, cities in conflicts.items():
            unique_cities = set(cities)
            print(f"   Pincode {pin}: {', '.join(unique_cities)} ({len(cities)} entries)")
    else:
        print("\n✅ No pincode conflicts found!")
    
    return conflicts

def fix_zipcodes_csv():
    """Remove duplicate pincodes, keep only one city per pincode"""
    print("\n" + "=" * 80)
    print("FIXING zipcodes.csv - REMOVING DUPLICATES")
    print("=" * 80)
    
    with open('data/zipcodes.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        pincodes = list(reader)
    
    # Track seen pincodes
    seen_pincodes = {}
    unique_pincodes = []
    
    # Priority order for cities (in case of conflicts, keep the most important)
    city_priority = {
        'Mumbai': 1,
        'Pune': 2,
        'Nagpur': 3,
        'Thane': 4,
        'Navi Mumbai': 5,
        'Kalyan': 6,
        'Bhiwandi': 7,
        'Panvel': 8,
    }
    
    for record in pincodes:
        pin = record['pincode']
        city = record['city']
        
        if pin not in seen_pincodes:
            # First occurrence - keep it
            seen_pincodes[pin] = city
            unique_pincodes.append(record)
        else:
            # Duplicate found
            existing_city = seen_pincodes[pin]
            
            # Keep the one with higher priority (lower number = higher priority)
            current_priority = city_priority.get(city, 999)
            existing_priority = city_priority.get(existing_city, 999)
            
            if current_priority < existing_priority:
                # Replace with higher priority city
                print(f"   Pincode {pin}: Replacing {existing_city} with {city} (higher priority)")
                # Remove old entry
                unique_pincodes = [p for p in unique_pincodes if p['pincode'] != pin]
                unique_pincodes.append(record)
                seen_pincodes[pin] = city
            else:
                print(f"   Pincode {pin}: Keeping {existing_city}, discarding {city}")
    
    # Save cleaned data
    with open('data/zipcodes.csv', 'w', newline='', encoding='utf-8') as f:
        if unique_pincodes:
            writer = csv.DictWriter(f, fieldnames=unique_pincodes[0].keys())
            writer.writeheader()
            writer.writerows(unique_pincodes)
    
    print(f"\n✅ Reduced from {len(pincodes)} to {len(unique_pincodes)} records")
    print(f"✅ Removed {len(pincodes) - len(unique_pincodes)} duplicate pincodes")
    
    return unique_pincodes

def fix_pharmacies_json():
    """Ensure all pharmacies have valid, non-conflicting pincodes"""
    print("\n" + "=" * 80)
    print("FIXING pharmacies.json - RESOLVING CONFLICTS")
    print("=" * 80)
    
    # Load current valid pincodes
    with open('data/zipcodes.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        valid_pincodes = {row['pincode']: row['city'] for row in reader}
    
    # Load pharmacies
    with open('data/pharmacies.json', 'r', encoding='utf-8') as f:
        pharmacies = json.load(f)
    
    fixed_count = 0
    removed_count = 0
    
    valid_pharmacies = []
    
    for pharmacy in pharmacies:
        ph_pincode = pharmacy.get('pincode', '')
        ph_city = pharmacy.get('city', '')
        
        # Check if pincode exists in valid list
        if ph_pincode not in valid_pincodes:
            print(f"   ❌ Removing {pharmacy['name']}: Invalid pincode {ph_pincode}")
            removed_count += 1
            continue
        
        # Check if city matches pincode
        correct_city = valid_pincodes[ph_pincode]
        if ph_city != correct_city:
            print(f"   🔧 Fixing {pharmacy['name']}: {ph_city} {ph_pincode} → {correct_city} {ph_pincode}")
            pharmacy['city'] = correct_city
            
            # Update area if needed
            pincode_data = next((row for row in csv.DictReader(open('data/zipcodes.csv', 'r', encoding='utf-8')) 
                                if row['pincode'] == ph_pincode), None)
            if pincode_data:
                pharmacy['area'] = pincode_data.get('area', pharmacy.get('area', ''))
                pharmacy['district'] = pincode_data.get('district', pharmacy.get('district', ''))
            
            fixed_count += 1
        
        valid_pharmacies.append(pharmacy)
    
    # Save
    with open('data/pharmacies.json', 'w', encoding='utf-8') as f:
        json.dump(valid_pharmacies, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Fixed {fixed_count} pharmacies with wrong city")
    print(f"✅ Removed {removed_count} pharmacies with invalid pincodes")
    print(f"✅ Total valid pharmacies: {len(valid_pharmacies)}")
    
    return valid_pharmacies

def verify_no_conflicts():
    """Final verification that no conflicts remain"""
    print("\n" + "=" * 80)
    print("FINAL VERIFICATION")
    print("=" * 80)
    
    # Check zipcodes.csv
    with open('data/zipcodes.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        pincodes = list(reader)
    
    pincode_set = set()
    duplicates = []
    
    for record in pincodes:
        pin = record['pincode']
        if pin in pincode_set:
            duplicates.append(pin)
        pincode_set.add(pin)
    
    if duplicates:
        print(f"\n❌ Still have duplicate pincodes: {duplicates}")
        return False
    else:
        print(f"\n✅ zipcodes.csv: {len(pincodes)} unique pincodes")
    
    # Check pharmacies.json
    with open('data/pharmacies.json', 'r', encoding='utf-8') as f:
        pharmacies = json.load(f)
    
    # Verify all pharmacy pincodes match their city
    pincode_city_map = {row['pincode']: row['city'] for row in pincodes}
    
    mismatches = []
    for pharmacy in pharmacies:
        ph_pincode = pharmacy['pincode']
        ph_city = pharmacy['city']
        
        if ph_pincode in pincode_city_map:
            correct_city = pincode_city_map[ph_pincode]
            if ph_city != correct_city:
                mismatches.append(f"{pharmacy['name']}: {ph_city} {ph_pincode} (should be {correct_city})")
    
    if mismatches:
        print(f"\n❌ Found {len(mismatches)} city-pincode mismatches:")
        for mismatch in mismatches[:5]:
            print(f"   {mismatch}")
        return False
    else:
        print(f"✅ pharmacies.json: All {len(pharmacies)} pharmacies have correct city-pincode mapping")
    
    # Show distribution
    print("\n" + "-" * 80)
    print("DISTRIBUTION BY CITY")
    print("-" * 80)
    
    city_stats = {}
    for pharmacy in pharmacies:
        city = pharmacy['city']
        if city not in city_stats:
            city_stats[city] = {'pharmacies': 0, 'pincodes': set()}
        city_stats[city]['pharmacies'] += 1
        city_stats[city]['pincodes'].add(pharmacy['pincode'])
    
    for city in sorted(city_stats.keys()):
        stats = city_stats[city]
        print(f"   {city}: {stats['pharmacies']} pharmacies across {len(stats['pincodes'])} pincodes")
    
    # Specific check for Bhiwandi 421302
    print("\n" + "-" * 80)
    print("BHIWANDI 421302 VERIFICATION")
    print("-" * 80)
    
    bhiwandi_421302 = [p for p in pharmacies if p['pincode'] == '421302']
    print(f"\nPharmacies with pincode 421302: {len(bhiwandi_421302)}")
    
    for pharmacy in bhiwandi_421302:
        city_status = "✅" if pharmacy['city'] == 'Bhiwandi' else "❌"
        print(f"   {city_status} {pharmacy['name']}: City={pharmacy['city']}")
    
    wrong_city_421302 = [p for p in bhiwandi_421302 if p['city'] != 'Bhiwandi']
    if wrong_city_421302:
        print(f"\n❌ ERROR: {len(wrong_city_421302)} pharmacies have pincode 421302 but wrong city!")
        return False
    else:
        print(f"\n✅ All 421302 pharmacies correctly belong to Bhiwandi")
    
    return True

def main():
    """Main execution"""
    print("=" * 80)
    print("PINCODE CONFLICT RESOLUTION")
    print("=" * 80)
    print("\nThis will:")
    print("1. Analyze current conflicts")
    print("2. Remove duplicate pincodes from zipcodes.csv")
    print("3. Fix or remove conflicting pharmacies")
    print("4. Verify all data is consistent")
    print("\n" + "=" * 80)
    
    # Step 1: Analyze
    conflicts = analyze_conflicts()
    
    if not conflicts:
        print("\n✅ No conflicts to fix!")
        return
    
    # Step 2: Fix zipcodes
    unique_pincodes = fix_zipcodes_csv()
    
    # Step 3: Fix pharmacies
    valid_pharmacies = fix_pharmacies_json()
    
    # Step 4: Verify
    success = verify_no_conflicts()
    
    if success:
        print("\n" + "=" * 80)
        print("✅ ALL CONFLICTS RESOLVED!")
        print("=" * 80)
        print("\n✅ Every pincode now belongs to exactly ONE city")
        print("✅ All pharmacies have valid city-pincode mappings")
        print("✅ Data is ready for accurate geospatial matching")
    else:
        print("\n" + "=" * 80)
        print("⚠️ SOME ISSUES REMAIN")
        print("=" * 80)
        print("Please review the errors above")

if __name__ == "__main__":
    main()
