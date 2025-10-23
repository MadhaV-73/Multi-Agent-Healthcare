"""
Test script to verify pharmacy matching works correctly with city/pincode filtering.
"""

import json
from pathlib import Path
from agents.pharmacy_agent import PharmacyAgent


def test_pharmacy_matching():
    """Test pharmacy matching for different cities and pincodes."""
    print("=" * 80)
    print("TESTING PHARMACY MATCHING WITH CITY/PINCODE FILTERING")
    print("=" * 80)
    
    # Initialize agent
    agent = PharmacyAgent(data_dir="./data")
    
    # Test cases for different cities
    test_cases = [
        {
            "name": "Mumbai - 400001",
            "therapy_result": {
                "otc_options": [
                    {"sku": "OTC001", "drug_name": "Paracetamol", "dosage": "500mg", "frequency": "twice daily", "duration": "3 days"},
                ]
            },
            "location": {
                "pincode": "400001",
                "city": "Mumbai"
            }
        },
        {
            "name": "Thane - 400601",
            "therapy_result": {
                "otc_options": [
                    {"sku": "OTC001", "drug_name": "Paracetamol", "dosage": "500mg", "frequency": "twice daily", "duration": "3 days"},
                ]
            },
            "location": {
                "pincode": "400601",
                "city": "Thane"
            }
        },
        {
            "name": "Navi Mumbai - 400701",
            "therapy_result": {
                "otc_options": [
                    {"sku": "OTC001", "drug_name": "Paracetamol", "dosage": "500mg", "frequency": "twice daily", "duration": "3 days"},
                ]
            },
            "location": {
                "pincode": "400701",
                "city": "Navi Mumbai"
            }
        },
        {
            "name": "Kalyan - 421301",
            "therapy_result": {
                "otc_options": [
                    {"sku": "OTC001", "drug_name": "Paracetamol", "dosage": "500mg", "frequency": "twice daily", "duration": "3 days"},
                ]
            },
            "location": {
                "pincode": "421301",
                "city": "Kalyan"
            }
        },
        {
            "name": "Vasai - 401201",
            "therapy_result": {
                "otc_options": [
                    {"sku": "OTC001", "drug_name": "Paracetamol", "dosage": "500mg", "frequency": "twice daily", "duration": "3 days"},
                ]
            },
            "location": {
                "pincode": "401201",
                "city": "Vasai"
            }
        }
    ]
    
    print("\n🔍 Running test cases...\n")
    
    results = []
    for test in test_cases:
        print(f"{'='*80}")
        print(f"TEST: {test['name']}")
        print(f"{'='*80}")
        
        result = agent.process(
            therapy_result=test['therapy_result'],
            location=test['location']
        )
        
        if result.get('status') == 'success':
            pharmacy_city = result.get('city', 'Unknown')
            pharmacy_pincode = result.get('pincode', 'Unknown')
            pharmacy_name = result.get('pharmacy_name', 'Unknown')
            distance = result.get('distance_km', 0)
            location_match = result.get('location_match', 'unknown')
            
            print(f"✅ SUCCESS")
            print(f"   Requested: {test['location']['city']} - {test['location']['pincode']}")
            print(f"   Matched:   {pharmacy_city} - {pharmacy_pincode}")
            print(f"   Pharmacy:  {pharmacy_name}")
            print(f"   Distance:  {distance:.2f} km")
            print(f"   Match:     {location_match}")
            
            match_quality = "EXCELLENT" if location_match == 'exact_pincode' else "GOOD" if location_match == 'same_city' else "OK"
            print(f"   Quality:   {match_quality}")
            
            results.append({
                "test": test['name'],
                "status": "✅ PASS",
                "match_quality": match_quality,
                "distance": distance
            })
        else:
            print(f"❌ FAILED")
            print(f"   Status: {result.get('status')}")
            print(f"   Message: {result.get('message', 'Unknown error')}")
            results.append({
                "test": test['name'],
                "status": "❌ FAIL",
                "match_quality": "N/A",
                "distance": 0
            })
        
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\n{'Test Case':<30} {'Status':<15} {'Match Quality':<15} {'Distance (km)':<15}")
    print("-" * 80)
    for r in results:
        print(f"{r['test']:<30} {r['status']:<15} {r['match_quality']:<15} {r['distance']:.2f}")
    
    passed = sum(1 for r in results if r['status'] == "✅ PASS")
    total = len(results)
    print("-" * 80)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 80)


if __name__ == "__main__":
    test_pharmacy_matching()
