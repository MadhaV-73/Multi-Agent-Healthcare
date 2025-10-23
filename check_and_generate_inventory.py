"""
Check inventory coverage and generate missing data if needed.
"""

import json
import pandas as pd
import random
from pathlib import Path


def check_inventory_coverage():
    """Check which pharmacies are missing inventory."""
    print("=" * 80)
    print("CHECKING INVENTORY COVERAGE")
    print("=" * 80)
    
    # Load data
    data_dir = Path("./data")
    
    with open(data_dir / "pharmacies.json") as f:
        pharmacies = json.load(f)
    
    inventory_df = pd.read_csv(data_dir / "inventory.csv")
    meds_df = pd.read_csv(data_dir / "meds.csv")
    
    print(f"\n📊 Current State:")
    print(f"   Total pharmacies: {len(pharmacies)}")
    print(f"   Pharmacies with inventory: {inventory_df['pharmacy_id'].nunique()}")
    print(f"   Total inventory records: {len(inventory_df)}")
    print(f"   Available medicine SKUs: {len(meds_df)}")
    
    # Find pharmacies without inventory
    pharm_ids = {p['id'] for p in pharmacies}
    inv_ids = set(inventory_df['pharmacy_id'].unique())
    missing_ids = pharm_ids - inv_ids
    
    print(f"\n❌ Missing inventory: {len(missing_ids)} pharmacies")
    
    if missing_ids:
        print(f"\n🔧 Generating inventory for missing pharmacies...")
        generate_missing_inventory(missing_ids, meds_df, inventory_df, data_dir)
    else:
        print(f"\n✅ All pharmacies have inventory!")
    
    return missing_ids


def generate_missing_inventory(missing_ids, meds_df, existing_inv, data_dir):
    """Generate inventory for pharmacies that don't have any."""
    
    new_records = []
    
    # Get available SKUs from meds
    available_skus = meds_df['sku'].unique()[:30]  # Use first 30 SKUs like existing data
    
    for pharmacy_id in sorted(missing_ids):
        # Each pharmacy gets 10-15 random medicines
        num_items = random.randint(10, 15)
        selected_skus = random.sample(list(available_skus), num_items)
        
        for sku in selected_skus:
            med_info = meds_df[meds_df['sku'] == sku].iloc[0]
            
            record = {
                'pharmacy_id': pharmacy_id,
                'sku': sku,
                'drug_name': med_info['drug_name'],
                'form': med_info.get('form', 'Tablet'),
                'strength': med_info.get('strength', '500mg'),
                'price': round(random.uniform(10, 150), 2),
                'qty': random.randint(20, 200)
            }
            new_records.append(record)
    
    if new_records:
        # Combine with existing inventory
        new_df = pd.DataFrame(new_records)
        combined_df = pd.concat([existing_inv, new_df], ignore_index=True)
        
        # Save
        output_file = data_dir / "inventory.csv"
        combined_df.to_csv(output_file, index=False)
        
        print(f"✅ Generated {len(new_records)} new inventory records")
        print(f"   Total records now: {len(combined_df)}")
        print(f"   Total pharmacies with inventory: {combined_df['pharmacy_id'].nunique()}")
        print(f"💾 Saved to {output_file}")
    
    return new_records


def verify_inventory():
    """Verify all pharmacies now have inventory."""
    print("\n" + "=" * 80)
    print("VERIFICATION")
    print("=" * 80)
    
    data_dir = Path("./data")
    
    with open(data_dir / "pharmacies.json") as f:
        pharmacies = json.load(f)
    
    inventory_df = pd.read_csv(data_dir / "inventory.csv")
    
    pharm_ids = {p['id'] for p in pharmacies}
    inv_ids = set(inventory_df['pharmacy_id'].unique())
    missing = pharm_ids - inv_ids
    
    print(f"\n📊 Final State:")
    print(f"   Total pharmacies: {len(pharmacies)}")
    print(f"   Pharmacies with inventory: {len(inv_ids)}")
    print(f"   Total inventory records: {len(inventory_df)}")
    
    if missing:
        print(f"\n❌ Still missing: {len(missing)} pharmacies")
        print(f"   IDs: {sorted(missing)[:10]}...")
    else:
        print(f"\n✅ SUCCESS! All pharmacies have inventory!")
    
    # Show some stats
    print(f"\n📈 Inventory Statistics:")
    avg_items = len(inventory_df) / len(inv_ids)
    print(f"   Average items per pharmacy: {avg_items:.1f}")
    
    # Group by city (need to match pharmacy IDs to cities)
    print(f"\n🏙️ Coverage by City:")
    pharm_city_map = {p['id']: p.get('city', 'Unknown') for p in pharmacies}
    inventory_df['city'] = inventory_df['pharmacy_id'].map(pharm_city_map)
    city_coverage = inventory_df.groupby('city')['pharmacy_id'].nunique()
    for city, count in city_coverage.items():
        print(f"   {city}: {count} pharmacies")


if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    check_inventory_coverage()
    verify_inventory()
    print("\n" + "=" * 80)
