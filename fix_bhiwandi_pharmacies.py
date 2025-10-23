"""
Fix pharmacy data: Update pharmacies with Bhiwandi pincodes to have correct city
"""
import json

# Load pharmacies
with open("data/pharmacies.json", "r") as f:
    pharmacies = json.load(f)

# Bhiwandi pincodes according to zipcodes.csv
bhiwandi_pincodes = ['421302', '421303', '421304', '421305', '421306', '421307', '421308']

fixed_count = 0
for pharmacy in pharmacies:
    pincode = str(pharmacy.get('pincode', ''))
    current_city = pharmacy.get('city', '')
    
    if pincode in bhiwandi_pincodes and current_city != 'Bhiwandi':
        print(f"Fixing: {pharmacy['name']} - {pincode} - was '{current_city}' → now 'Bhiwandi'")
        pharmacy['city'] = 'Bhiwandi'
        fixed_count += 1

# Save back
with open("data/pharmacies.json", "w") as f:
    json.dump(pharmacies, f, indent=2)

print(f"\n✅ Fixed {fixed_count} pharmacies to have correct 'Bhiwandi' city")
print("✅ Pharmacies data updated")
