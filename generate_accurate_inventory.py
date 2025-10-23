"""
Generate Accurate Inventory for the New Pharmacy Data
Maps medicines to pharmacies with realistic stock levels
"""

import json
import csv
import random
from pathlib import Path

# Load medicine data
def load_medicines():
    """Load medicine catalog"""
    medicines = []
    with open('data/meds.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            medicines.append({
                'sku': row.get('sku', ''),
                'drug_name': row.get('drug_name', ''),
                'form': row.get('form', 'Tablet')
            })
    return medicines

def generate_accurate_inventory():
    """Generate inventory for accurate pharmacy data"""
    
    print("=" * 80)
    print("GENERATING ACCURATE INVENTORY DATA")
    print("=" * 80)
    
    # Load pharmacies
    with open('data/pharmacies_accurate.json', 'r', encoding='utf-8') as f:
        pharmacies = json.load(f)
    
    print(f"\n✅ Loaded {len(pharmacies)} pharmacies")
    
    # Load medicines
    try:
        medicines = load_medicines()
        print(f"✅ Loaded {len(medicines)} medicine SKUs")
    except:
        # Generate basic SKUs if meds.csv doesn't exist
        medicines = [{'sku': f'OTC{str(i).zfill(3)}', 'drug_name': f'Medicine {i}', 'form': 'Tablet'} 
                     for i in range(1, 51)]
        print(f"✅ Generated {len(medicines)} basic medicine SKUs")
    
    inventory = []
    
    # Each pharmacy gets 60-80% of available medicines
    for pharmacy in pharmacies:
        ph_id = pharmacy['id']
        city = pharmacy['city']
        
        # Number of SKUs this pharmacy stocks (60-80% of total)
        num_skus = random.randint(int(len(medicines) * 0.6), int(len(medicines) * 0.8))
        
        # Randomly select SKUs
        selected_medicines = random.sample(medicines, num_skus)
        
        for med in selected_medicines:
            # Stock quantity (realistic ranges)
            if 'essential' in med['drug_name'].lower() or med['sku'] in ['OTC001', 'OTC002', 'OTC003']:
                # Essential medicines: higher stock
                qty = random.randint(50, 200)
            else:
                # Regular medicines
                qty = random.randint(10, 100)
            
            # Price (realistic INR prices)
            base_price = random.uniform(15, 250)
            price = round(base_price, 2)
            
            inventory.append({
                'pharmacy_id': ph_id,
                'sku': med['sku'],
                'qty_available': qty,
                'price': price
            })
    
    # Save to CSV
    with open('data/inventory_accurate.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['pharmacy_id', 'sku', 'qty_available', 'price']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inventory)
    
    print(f"\n✅ Generated {len(inventory)} inventory records")
    print(f"✅ Average {len(inventory) / len(pharmacies):.1f} items per pharmacy")
    
    # Statistics by city
    print("\nInventory distribution:")
    for city in ['Mumbai', 'Pune', 'Nagpur', 'Thane', 'Navi Mumbai']:
        city_pharmacies = [p for p in pharmacies if p['city'] == city]
        city_inventory = [inv for inv in inventory if any(p['id'] == inv['pharmacy_id'] for p in city_pharmacies)]
        if city_pharmacies:
            print(f"   - {city}: {len(city_inventory)} records across {len(city_pharmacies)} pharmacies")
    
    print("\n✅ File saved: data/inventory_accurate.csv")
    
    return inventory

if __name__ == "__main__":
    generate_accurate_inventory()
    print("\nInventory generation complete!")
