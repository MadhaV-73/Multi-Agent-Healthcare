"""
Debug: Check which pharmacies have stock for OTC001 and OTC002
"""
import pandas as pd
import json

# Load data
inventory_df = pd.read_csv("data/inventory.csv")
with open("data/pharmacies.json", "r") as f:
    pharmacies = json.load(f)

# Create pharmacy lookup
pharmacy_dict = {p['id']: p for p in pharmacies}

print("=" * 80)
print("CHECKING INVENTORY FOR OTC001 and OTC002")
print("=" * 80)

# Find pharmacies with pincode 421302
pincode_421302_pharmacies = [p for p in pharmacies if str(p.get('pincode', '')) == '421302']
print(f"\nPharmacies with pincode 421302: {len(pincode_421302_pharmacies)}")

for pharmacy in pincode_421302_pharmacies:
    ph_id = pharmacy['id']
    ph_name = pharmacy['name']
    ph_city = pharmacy.get('city', 'N/A')
    
    # Check inventory
    ph_inventory = inventory_df[inventory_df['pharmacy_id'] == ph_id]
    has_otc001 = len(ph_inventory[ph_inventory['sku'] == 'OTC001']) > 0
    has_otc002 = len(ph_inventory[ph_inventory['sku'] == 'OTC002']) > 0
    
    print(f"\n  {ph_name} (ID: {ph_id})")
    print(f"    City: {ph_city}, Pincode: 421302")
    print(f"    Total inventory records: {len(ph_inventory)}")
    print(f"    Has OTC001: {has_otc001}")
    print(f"    Has OTC002: {has_otc002}")
    print(f"    Has BOTH: {'✅' if (has_otc001 and has_otc002) else '❌'}")

print("\n" + "=" * 80)
print("SAMPLE: Pharmacies with BOTH OTC001 and OTC002 (any location)")
print("=" * 80)

# Find ANY pharmacies with both
both_sku_pharmacies = []
for pharmacy in pharmacies[:100]:  # Check first 100
    ph_id = pharmacy['id']
    ph_inventory = inventory_df[inventory_df['pharmacy_id'] == ph_id]
    has_otc001 = len(ph_inventory[ph_inventory['sku'] == 'OTC001']) > 0
    has_otc002 = len(ph_inventory[ph_inventory['sku'] == 'OTC002']) > 0
    
    if has_otc001 and has_otc002:
        both_sku_pharmacies.append({
            'id': ph_id,
            'name': pharmacy['name'],
            'city': pharmacy.get('city', 'N/A'),
            'pincode': pharmacy.get('pincode', 'N/A')
        })

print(f"\nFound {len(both_sku_pharmacies)} pharmacies (from first 100) with both OTC001 and OTC002:")
for ph in both_sku_pharmacies[:5]:
    print(f"  - {ph['name']} | {ph['city']} {ph['pincode']}")

print("\n" + "=" * 80)
print("INVENTORY STATISTICS")
print("=" * 80)

sku_counts = inventory_df['sku'].value_counts()
print(f"\nTotal inventory records: {len(inventory_df)}")
print(f"Unique SKUs: {inventory_df['sku'].nunique()}")
print(f"\nTop SKUs:")
print(sku_counts.head(10))

print(f"\nOTC001 availability: {len(inventory_df[inventory_df['sku'] == 'OTC001'])} pharmacies")
print(f"OTC002 availability: {len(inventory_df[inventory_df['sku'] == 'OTC002'])} pharmacies")
