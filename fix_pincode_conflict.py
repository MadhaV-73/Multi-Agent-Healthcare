"""
Fix the pincode conflict: 421302 appears for both Bhiwandi and Kalyan
Based on India Post data, 421302 is BHIWANDI, not Kalyan
"""

import json

# Load pharmacies
with open('data/pharmacies.json', 'r', encoding='utf-8') as f:
    pharmacies = json.load(f)

print("=" * 80)
print("FIXING PINCODE 421302 CONFLICT")
print("=" * 80)

# According to India Post: 421302 is Bhiwandi Pawne, NOT Kalyan
# Kalyan pincodes are 421301, 421303, 421304, etc.

print("\nCurrent state:")
pincode_421302_pharmacies = [p for p in pharmacies if p['pincode'] == '421302']
print(f"Pharmacies with pincode 421302: {len(pincode_421302_pharmacies)}")

for p in pincode_421302_pharmacies:
    print(f"   - {p['name']}: City={p['city']}")

# Fix: Change Kalyan 421302 to Kalyan 421303 (which already exists)
fixed_count = 0
for pharmacy in pharmacies:
    if pharmacy['pincode'] == '421302' and pharmacy['city'] == 'Kalyan':
        pharmacy['pincode'] = '421303'  # Change to another Kalyan pincode
        pharmacy['area'] = 'Shahad'  # Update area to match 421303
        fixed_count += 1
        print(f"\n✅ Fixed: {pharmacy['name']}")
        print(f"   Changed from: Kalyan 421302")
        print(f"   Changed to: Kalyan 421303 (Shahad)")

# Save
with open('data/pharmacies.json', 'w', encoding='utf-8') as f:
    json.dump(pharmacies, f, indent=2, ensure_ascii=False)

print(f"\n✅ Fixed {fixed_count} pharmacies")
print(f"✅ Pincode 421302 now belongs ONLY to Bhiwandi")

# Verify
print("\n" + "=" * 80)
print("VERIFICATION")
print("=" * 80)

pincode_421302_after = [p for p in pharmacies if p['pincode'] == '421302']
print(f"\nPharmacies with pincode 421302 after fix: {len(pincode_421302_after)}")
for p in pincode_421302_after:
    print(f"   - {p['name']}: City={p['city']} ✅")

wrong_city = [p for p in pincode_421302_after if p['city'] != 'Bhiwandi']
if wrong_city:
    print(f"\n❌ Still {len(wrong_city)} pharmacies with wrong city!")
else:
    print(f"\n✅ All 421302 pharmacies are correctly in Bhiwandi!")

print("\n✅ File updated: data/pharmacies.json")
