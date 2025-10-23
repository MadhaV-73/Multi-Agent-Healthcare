"""
Script to enrich pharmacies.json with city and pincode information
by finding the nearest zipcode location for each pharmacy.
"""

import json
import math
import pandas as pd
from pathlib import Path


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates using Haversine formula."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Earth radius in kilometers
    return c * r


def find_nearest_zipcode(pharmacy_lat, pharmacy_lon, zipcodes_df):
    """Find the nearest zipcode for a pharmacy based on coordinates."""
    min_distance = float('inf')
    nearest_zipcode = None
    nearest_city = None
    
    for _, row in zipcodes_df.iterrows():
        distance = haversine_distance(
            pharmacy_lat, pharmacy_lon,
            row['lat'], row['lon']
        )
        
        if distance < min_distance:
            min_distance = distance
            nearest_zipcode = str(row['pincode'])
            nearest_city = row['city']
    
    return nearest_city, nearest_zipcode, min_distance


def enrich_pharmacies():
    """Add city and pincode to each pharmacy."""
    print("=" * 70)
    print("ENRICHING PHARMACIES WITH CITY AND PINCODE DATA")
    print("=" * 70)
    
    # Load data
    data_dir = Path("./data")
    pharmacies_file = data_dir / "pharmacies.json"
    zipcodes_file = data_dir / "zipcodes.csv"
    
    print("\n📂 Loading data...")
    with open(pharmacies_file, 'r') as f:
        pharmacies = json.load(f)
    
    zipcodes_df = pd.read_csv(zipcodes_file)
    # Filter out Ahmedabad since we only have Mumbai region pharmacies
    zipcodes_df = zipcodes_df[zipcodes_df["city"] != "Ahmedabad"].copy()
    
    print(f"   Loaded {len(pharmacies)} pharmacies")
    print(f"   Loaded {len(zipcodes_df)} zipcodes (Mumbai region only)")
    
    print("\n🔍 Matching pharmacies to nearest zipcodes...")
    enriched_count = 0
    
    for pharmacy in pharmacies:
        if 'city' not in pharmacy or 'pincode' not in pharmacy:
            city, pincode, distance = find_nearest_zipcode(
                pharmacy['lat'],
                pharmacy['lon'],
                zipcodes_df
            )
            
            pharmacy['city'] = city
            pharmacy['pincode'] = pincode
            pharmacy['nearest_zipcode_distance_km'] = round(distance, 2)
            enriched_count += 1
            
            if enriched_count <= 5:  # Show first 5 as examples
                print(f"   {pharmacy['name']}: {city} - {pincode} ({distance:.2f} km)")
    
    print(f"\n✅ Enriched {enriched_count} pharmacies with location data")
    
    # Save enriched data
    output_file = data_dir / "pharmacies.json"
    print(f"\n💾 Saving to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(pharmacies, f, indent=2)
    
    print("✅ Done!")
    
    # Show statistics
    print("\n📊 Statistics:")
    cities = {}
    for p in pharmacies:
        city = p.get('city', 'Unknown')
        cities[city] = cities.get(city, 0) + 1
    
    for city, count in sorted(cities.items()):
        print(f"   {city}: {count} pharmacies")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    enrich_pharmacies()
