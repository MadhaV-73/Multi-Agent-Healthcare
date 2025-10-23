"""
Add essential OTC medicines to Bhiwandi 421302 pharmacies
"""
import pandas as pd
import json
import random

# Load data
inventory_df = pd.read_csv("data/inventory.csv")
with open("data/pharmacies.json", "r") as f:
    pharmacies = json.load(f)

# Get Bhiwandi 421302 pharmacies
bhiwandi_421302_pharmacies = [p['id'] for p in pharmacies if str(p.get('pincode', '')) == '421302']

print("=" * 80)
print("ADDING ESSENTIAL OTC INVENTORY TO BHIWANDI 421302 PHARMACIES")
print("=" * 80)

# Essential OTC medicines (most commonly needed)
essential_skus = ['OTC001', 'OTC002', 'OTC003', 'OTC004', 'OTC005', 
                  'OTC006', 'OTC007', 'OTC008', 'OTC009', 'OTC010']

new_records = []
for ph_id in bhiwandi_421302_pharmacies:
    ph_inventory = inventory_df[inventory_df['pharmacy_id'] == ph_id]
    
    for sku in essential_skus:
        # Check if already exists
        has_sku = len(ph_inventory[ph_inventory['sku'] == sku]) > 0
        
        if not has_sku:
            # Add with random quantity
            qty = random.randint(20, 100)
            new_records.append({
                'pharmacy_id': ph_id,
                'sku': sku,
                'qty_available': qty,
                'price': round(random.uniform(10, 150), 2)
            })
            print(f"  Adding {sku} to {ph_id}: {qty} units")

# Append new records
if new_records:
    new_df = pd.DataFrame(new_records)
    inventory_df = pd.concat([inventory_df, new_df], ignore_index=True)
    
    # Save back
    inventory_df.to_csv("data/inventory.csv", index=False)
    print(f"\n✅ Added {len(new_records)} inventory records")
    print(f"✅ Total inventory records now: {len(inventory_df)}")
else:
    print("\n✅ All Bhiwandi 421302 pharmacies already have essential OTC items")

print("\n" + "=" * 80)
print("VERIFICATION")
print("=" * 80)

for ph_id in bhiwandi_421302_pharmacies:
    ph_inventory = inventory_df[inventory_df['pharmacy_id'] == ph_id]
    has_otc001 = len(ph_inventory[ph_inventory['sku'] == 'OTC001']) > 0
    has_otc002 = len(ph_inventory[ph_inventory['sku'] == 'OTC002']) > 0
    
    ph = next((p for p in pharmacies if p['id'] == ph_id), None)
    ph_name = ph['name'] if ph else ph_id
    
    print(f"  {ph_name}: OTC001={has_otc001}, OTC002={has_otc002}")
