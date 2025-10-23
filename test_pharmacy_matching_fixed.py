"""
Test pharmacy matching with Bhiwandi 421302 vs Navi Mumbai 400715
"""
import sys
sys.path.insert(0, '.')

from agents.pharmacy_agent import PharmacyAgent
import json

# Initialize agent
agent = PharmacyAgent()

print("=" * 80)
print("TEST 1: Bhiwandi 421302 - Should match Bhiwandi pharmacies")
print("=" * 80)

# Simulate therapy result
therapy_result = {
    "otc_options": [
        {"sku": "OTC001", "drug_name": "Paracetamol"},
        {"sku": "OTC002", "drug_name": "Cough Syrup"}
    ]
}

location_bhiwandi = {
    "pincode": "421302",
    "city": "Bhiwandi"
}

result = agent.process(therapy_result, location_bhiwandi)

if result.get("pharmacy_name"):
    print(f"\n✅ MATCHED PHARMACY:")
    print(f"   Name: {result['pharmacy_name']}")
    print(f"   City: {result.get('city', 'N/A')}")
    print(f"   Pincode: {result.get('pincode', 'N/A')}")
    print(f"   Distance: {result.get('distance_km', 'N/A')} km")
    print(f"   Location Match: {result.get('location_match', 'N/A')}")
    
    # Check if it's correct
    pharmacy_pincode = str(result.get('pincode', ''))
    pharmacy_city = result.get('city', '')
    
    if pharmacy_pincode == "421302":
        print("\n   ✅ CORRECT: Exact pincode match!")
    elif pharmacy_city == "Bhiwandi":
        print("\n   ⚠️ ACCEPTABLE: Same city but different pincode")
    else:
        print(f"\n   ❌ ERROR: Wrong location! Expected Bhiwandi 421302, got {pharmacy_city} {pharmacy_pincode}")
else:
    print("\n❌ No pharmacy matched")
    print(f"Error: {result.get('error', 'Unknown error')}")

print("\n" + "=" * 80)
print("TEST 2: Navi Mumbai 400715 - Should match Navi Mumbai pharmacies")
print("=" * 80)

location_navi_mumbai = {
    "pincode": "400715",
    "city": "Navi Mumbai"
}

result2 = agent.process(therapy_result, location_navi_mumbai)

if result2.get("pharmacy_name"):
    print(f"\n✅ MATCHED PHARMACY:")
    print(f"   Name: {result2['pharmacy_name']}")
    print(f"   City: {result2.get('city', 'N/A')}")
    print(f"   Pincode: {result2.get('pincode', 'N/A')}")
    print(f"   Distance: {result2.get('distance_km', 'N/A')} km")
    print(f"   Location Match: {result2.get('location_match', 'N/A')}")
    
    pharmacy_pincode = str(result2.get('pincode', ''))
    pharmacy_city = result2.get('city', '')
    
    if pharmacy_pincode == "400715":
        print("\n   ✅ CORRECT: Exact pincode match!")
    elif pharmacy_city == "Navi Mumbai":
        print("\n   ⚠️ ACCEPTABLE: Same city but different pincode")
    else:
        print(f"\n   ❌ ERROR: Wrong location! Expected Navi Mumbai 400715, got {pharmacy_city} {pharmacy_pincode}")
else:
    print("\n❌ No pharmacy matched")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("\nThe pharmacy matching should now:")
print("  1. ✅ Prioritize exact pincode matches (421302 → 421302)")
print("  2. ✅ Fall back to same city if no exact pincode")
print("  3. ✅ Only show nearby cities as last resort")
print("\nPriority scoring: exact_pincode (-100000) >>> same_city (-10000) >> distance (km)")
