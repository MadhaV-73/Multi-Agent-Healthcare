"""
Add back Bhiwandi 421302 and Panvel 410206 with correct data
Then regenerate pharmacies for these pincodes
"""

import csv
import json
import random
import math

# Add the missing pincodes with CORRECT city assignments
MISSING_PINCODES = [
    {
        'city': 'Bhiwandi',
        'pincode': '421302',
        'area': 'Bhiwandi City',
        'lat': '19.2967',
        'lon': '73.0631',
        'district': 'Thane'
    },
    {
        'city': 'Panvel',
        'pincode': '410206',
        'area': 'Kamothe',
        'lat': '19.0194',
        'lon': '73.0950',
        'district': 'Raigad'
    }
]

PHARMACY_CHAINS = [
    "Apollo Pharmacy", "MedPlus", "Wellness Forever", "PharmEasy Store",
    "Netmeds Pharmacy", "1mg Store", "HealthBuddy", "CarePlus Pharmacy",
    "LifeCare Chemist", "MediHub", "PharmaOne", "HealthFirst"
]

def generate_coordinate_within_area(center_lat: float, center_lon: float, radius_km: float = 1.0):
    """Generate a random coordinate within radius"""
    distance_km = random.uniform(0.1, radius_km)
    angle = random.uniform(0, 2 * math.pi)
    R = 6371.0
    
    center_lat_rad = math.radians(center_lat)
    center_lon_rad = math.radians(center_lon)
    
    new_lat_rad = math.asin(
        math.sin(center_lat_rad) * math.cos(distance_km / R) +
        math.cos(center_lat_rad) * math.sin(distance_km / R) * math.cos(angle)
    )
    
    new_lon_rad = center_lon_rad + math.atan2(
        math.sin(angle) * math.sin(distance_km / R) * math.cos(center_lat_rad),
        math.cos(distance_km / R) - math.sin(center_lat_rad) * math.sin(new_lat_rad)
    )
    
    return round(math.degrees(new_lat_rad), 6), round(math.degrees(new_lon_rad), 6)

def add_missing_pincodes():
    """Add missing pincodes to zipcodes.csv"""
    print("=" * 80)
    print("ADDING MISSING PINCODES")
    print("=" * 80)
    
    # Load existing
    with open('data/zipcodes.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing = list(reader)
    
    existing_pincodes = {row['pincode'] for row in existing}
    
    # Add missing
    added = 0
    for pincode_data in MISSING_PINCODES:
        if pincode_data['pincode'] not in existing_pincodes:
            existing.append(pincode_data)
            print(f"   ✅ Added: {pincode_data['pincode']} - {pincode_data['city']} ({pincode_data['area']})")
            added += 1
        else:
            print(f"   ⚠️ Already exists: {pincode_data['pincode']}")
    
    # Save
    with open('data/zipcodes.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = existing[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    
    print(f"\n✅ Added {added} pincodes")
    print(f"✅ Total pincodes now: {len(existing)}")
    
    return existing

def generate_pharmacies_for_pincode(pincode_data, num_pharmacies=3):
    """Generate pharmacies for a pincode"""
    pharmacies = []
    center_lat = float(pincode_data['lat'])
    center_lon = float(pincode_data['lon'])
    
    # Get existing pharmacy IDs to avoid duplicates
    with open('data/pharmacies.json', 'r', encoding='utf-8') as f:
        existing = json.load(f)
    existing_ids = {p['id'] for p in existing}
    
    for i in range(num_pharmacies):
        lat, lon = generate_coordinate_within_area(center_lat, center_lon, 0.8)
        
        chain = random.choice(PHARMACY_CHAINS)
        area_name = pincode_data['area'].split()[0]
        name = f"{chain} {area_name}"
        if i > 0:
            name = f"{name} {i+1}"
        
        # Generate unique ID
        ph_id = f"ph{random.randint(10000, 99999)}"
        while ph_id in existing_ids:
            ph_id = f"ph{random.randint(10000, 99999)}"
        existing_ids.add(ph_id)
        
        pharmacy = {
            'id': ph_id,
            'name': name,
            'lat': lat,
            'lon': lon,
            'city': pincode_data['city'],
            'pincode': pincode_data['pincode'],
            'area': pincode_data['area'],
            'district': pincode_data['district'],
            'services': random.choice([
                ["24x7", "home_delivery"],
                ["home_delivery", "online_ordering"],
                ["home_delivery"]
            ]),
            'delivery_km': random.choice([5, 7, 10]),
            'rating': round(random.uniform(3.8, 5.0), 1),
            'verified': True
        }
        
        pharmacies.append(pharmacy)
    
    return pharmacies

def add_pharmacies_for_missing_pincodes():
    """Generate and add pharmacies for missing pincodes"""
    print("\n" + "=" * 80)
    print("GENERATING PHARMACIES FOR MISSING PINCODES")
    print("=" * 80)
    
    # Load existing pharmacies
    with open('data/pharmacies.json', 'r', encoding='utf-8') as f:
        pharmacies = json.load(f)
    
    original_count = len(pharmacies)
    
    # Generate for each missing pincode
    for pincode_data in MISSING_PINCODES:
        print(f"\n{pincode_data['city']} {pincode_data['pincode']}:")
        new_pharmacies = generate_pharmacies_for_pincode(pincode_data, 3)
        
        for pharmacy in new_pharmacies:
            pharmacies.append(pharmacy)
            print(f"   ✅ {pharmacy['name']} at ({pharmacy['lat']}, {pharmacy['lon']})")
    
    # Save
    with open('data/pharmacies.json', 'w', encoding='utf-8') as f:
        json.dump(pharmacies, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Added {len(pharmacies) - original_count} new pharmacies")
    print(f"✅ Total pharmacies now: {len(pharmacies)}")
    
    return pharmacies

def add_inventory_for_new_pharmacies():
    """Add inventory for the new pharmacies"""
    print("\n" + "=" * 80)
    print("GENERATING INVENTORY FOR NEW PHARMACIES")
    print("=" * 80)
    
    # Load existing inventory
    with open('data/inventory.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        inventory = list(reader)
    
    original_count = len(inventory)
    
    # Load pharmacies
    with open('data/pharmacies.json', 'r', encoding='utf-8') as f:
        pharmacies = json.load(f)
    
    # Get existing pharmacy IDs in inventory
    inventory_ph_ids = {inv['pharmacy_id'] for inv in inventory}
    
    # Find new pharmacies
    new_pharmacies = [p for p in pharmacies if p['id'] not in inventory_ph_ids]
    
    # Essential OTC medicines
    essential_skus = [f'OTC{str(i).zfill(3)}' for i in range(1, 21)]
    
    for pharmacy in new_pharmacies:
        # Add 10-15 items per pharmacy
        num_items = random.randint(10, 15)
        selected_skus = random.sample(essential_skus, num_items)
        
        for sku in selected_skus:
            inventory.append({
                'pharmacy_id': pharmacy['id'],
                'sku': sku,
                'qty_available': random.randint(20, 100),
                'price': round(random.uniform(15, 200), 2)
            })
    
    # Save
    with open('data/inventory.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['pharmacy_id', 'sku', 'qty_available', 'price']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inventory)
    
    print(f"✅ Added inventory for {len(new_pharmacies)} new pharmacies")
    print(f"✅ Added {len(inventory) - original_count} new inventory records")
    print(f"✅ Total inventory records: {len(inventory)}")

def verify_final_state():
    """Verify everything is correct"""
    print("\n" + "=" * 80)
    print("FINAL VERIFICATION")
    print("=" * 80)
    
    # Load all data
    with open('data/zipcodes.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        pincodes = list(reader)
    
    with open('data/pharmacies.json', 'r', encoding='utf-8') as f:
        pharmacies = json.load(f)
    
    # Check specific pincodes
    test_cases = [
        ('421302', 'Bhiwandi'),
        ('410206', 'Panvel')
    ]
    
    for pincode, expected_city in test_cases:
        print(f"\n{pincode} ({expected_city}):")
        
        # Check in zipcodes
        zip_entry = next((p for p in pincodes if p['pincode'] == pincode), None)
        if zip_entry:
            if zip_entry['city'] == expected_city:
                print(f"   ✅ zipcodes.csv: {pincode} → {zip_entry['city']}")
            else:
                print(f"   ❌ zipcodes.csv: {pincode} → {zip_entry['city']} (expected {expected_city})")
        else:
            print(f"   ❌ zipcodes.csv: {pincode} NOT FOUND")
        
        # Check pharmacies
        ph_list = [p for p in pharmacies if p['pincode'] == pincode]
        if ph_list:
            correct_city = all(p['city'] == expected_city for p in ph_list)
            if correct_city:
                print(f"   ✅ pharmacies.json: {len(ph_list)} pharmacies, all in {expected_city}")
                for p in ph_list:
                    print(f"      - {p['name']}")
            else:
                wrong = [p for p in ph_list if p['city'] != expected_city]
                print(f"   ❌ {len(wrong)} pharmacies have wrong city")
        else:
            print(f"   ⚠️ No pharmacies for {pincode}")
    
    print("\n" + "=" * 80)
    print("✅ DATA RESTORATION COMPLETE")
    print("=" * 80)

def main():
    # Step 1: Add missing pincodes
    add_missing_pincodes()
    
    # Step 2: Generate pharmacies
    add_pharmacies_for_missing_pincodes()
    
    # Step 3: Generate inventory
    add_inventory_for_new_pharmacies()
    
    # Step 4: Verify
    verify_final_state()

if __name__ == "__main__":
    main()
