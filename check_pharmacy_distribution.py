"""
Check pharmacy distribution by city and pincode
"""
import json
import pandas as pd

# Load pharmacies
with open("data/pharmacies.json", "r") as f:
    pharmacies = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(pharmacies)

print("=" * 80)
print("PHARMACY DISTRIBUTION BY CITY")
print("=" * 80)

city_counts = df['city'].value_counts()
print(f"\n{city_counts}\n")

print("=" * 80)
print("BHIWANDI PHARMACIES")
print("=" * 80)
bhiwandi = df[df['city'] == 'Bhiwandi']
print(f"Total Bhiwandi pharmacies: {len(bhiwandi)}")
print(f"Pincodes: {sorted(bhiwandi['pincode'].unique())}\n")

if len(bhiwandi) > 0:
    print("Sample Bhiwandi pharmacies:")
    for idx, row in bhiwandi.head(5).iterrows():
        print(f"  - {row['name']} | Pincode: {row['pincode']} | Lat: {row['lat']}, Lon: {row['lon']}")

print("\n" + "=" * 80)
print("NAVI MUMBAI PHARMACIES")
print("=" * 80)
navi_mumbai = df[df['city'] == 'Navi Mumbai']
print(f"Total Navi Mumbai pharmacies: {len(navi_mumbai)}")
print(f"Pincodes: {sorted(navi_mumbai['pincode'].unique())}\n")

if len(navi_mumbai) > 0:
    print("Sample Navi Mumbai pharmacies:")
    for idx, row in navi_mumbai.head(5).iterrows():
        print(f"  - {row['name']} | Pincode: {row['pincode']} | Lat: {row['lat']}, Lon: {row['lon']}")

print("\n" + "=" * 80)
print("PINCODE 421302 (BHIWANDI) PHARMACIES")
print("=" * 80)
pincode_421302 = df[df['pincode'] == '421302']
print(f"Pharmacies with pincode 421302: {len(pincode_421302)}\n")

if len(pincode_421302) > 0:
    for idx, row in pincode_421302.iterrows():
        print(f"  - {row['name']} | City: {row['city']} | Lat: {row['lat']}, Lon: {row['lon']}")

print("\n" + "=" * 80)
print("PINCODE 400715 (NAVI MUMBAI) PHARMACIES")
print("=" * 80)
pincode_400715 = df[df['pincode'] == '400715']
print(f"Pharmacies with pincode 400715: {len(pincode_400715)}\n")

if len(pincode_400715) > 0:
    for idx, row in pincode_400715.iterrows():
        print(f"  - {row['name']} | City: {row['city']} | Lat: {row['lat']}, Lon: {row['lon']}")

print("\n" + "=" * 80)
print("DISTANCE CALCULATION CHECK")
print("=" * 80)

# Get coordinates for Bhiwandi 421302
from utils.geo_utils import get_coordinates_for_pincode

zip_df = pd.read_csv("data/zipcodes.csv")
bhiwandi_coords = zip_df[(zip_df['city'] == 'Bhiwandi') & (zip_df['pincode'] == '421302')]
navi_mumbai_coords = zip_df[(zip_df['city'] == 'Navi Mumbai') & (zip_df['pincode'] == '400715')]

if not bhiwandi_coords.empty:
    print(f"\nBhiwandi 421302 coordinates: Lat {bhiwandi_coords.iloc[0]['lat']}, Lon {bhiwandi_coords.iloc[0]['lon']}")
else:
    print("\nBhiwandi 421302 NOT found in zipcodes.csv")

if not navi_mumbai_coords.empty:
    print(f"Navi Mumbai 400715 coordinates: Lat {navi_mumbai_coords.iloc[0]['lat']}, Lon {navi_mumbai_coords.iloc[0]['lon']}")
else:
    print("Navi Mumbai 400715 NOT found in zipcodes.csv")

print("\n" + "=" * 80)
