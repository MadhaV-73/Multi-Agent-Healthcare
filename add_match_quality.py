"""
Add match quality indicator to pharmacy display
"""

# Read the file
with open("app_integrated.py", "r", encoding="utf-8") as f:
    content = f.read()

# Old section to replace
old_section = """            # Display location info prominently
            location_info_cols = st.columns(2)
            location_info_cols[0].info(f"📍 **City:** {pharmacy.get('city', 'N/A')}")
            location_info_cols[1].info(f"� **Pincode:** {pharmacy.get('pincode', 'N/A')}")"""

# New section with match quality
new_section = """            # Display location info prominently with match quality
            location_match = pharmacy.get('location_match', 'nearby')
            match_icon = "✅" if location_match == 'exact_pincode' else "📍" if location_match == 'same_city' else "📌"
            match_text = {
                'exact_pincode': 'Exact Pincode Match',
                'same_city': 'Same City',
                'nearby': 'Nearby Area'
            }.get(location_match, 'Matched')
            
            location_info_cols = st.columns(3)
            location_info_cols[0].info(f"📍 **City:** {pharmacy.get('city', 'N/A')}")
            location_info_cols[1].info(f"📮 **Pincode:** {pharmacy.get('pincode', 'N/A')}")
            
            # Show match quality indicator
            if location_match == 'exact_pincode':
                location_info_cols[2].success(f"{match_icon} **{match_text}**")
            elif location_match == 'same_city':
                location_info_cols[2].info(f"{match_icon} **{match_text}**")
            else:
                location_info_cols[2].warning(f"{match_icon} **{match_text}**")"""

# Replace
if old_section in content:
    content = content.replace(old_section, new_section)
    print("✅ Match quality indicator added successfully!")
else:
    print("❌ Old section not found - may already be updated")

# Write back
with open("app_integrated.py", "w", encoding="utf-8") as f:
    f.write(content)

print("File updated!")
