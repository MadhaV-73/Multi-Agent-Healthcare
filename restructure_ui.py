"""
Script to restructure the X-Ray analysis page:
1. Move location section after patient info
2. Put location inside the form (no need for dynamic filtering now)
"""

# Read the file
with open("app_integrated.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find and replace the xray_analysis_page function structure
old_section = """    # Check API status
    api_status, _ = check_api_status()
    if not api_status:
        st.error("❌ **Backend API is offline!** Please start it first: `python api/main.py`")
        return
    
    # Location selection OUTSIDE form for dynamic updates
    st.markdown("### 📍 Location Selection")
    loc_col1, loc_col2 = st.columns(2)
    with loc_col1:
        selected_city = st.selectbox("City", zip_df["city"].unique().tolist(), help="Select your city", key="xray_city")
    with loc_col2:
        # Filter pincodes by selected city
        city_subset = zip_df[zip_df["city"] == selected_city]
        pincode_options = city_subset["pincode"].tolist() if not city_subset.empty else []
        
        if not pincode_options:
            st.warning(f"No pincodes found for {selected_city}")
            zip_code = st.text_input("Enter ZIP/PIN Code", help="6-digit pincode", key="xray_pincode_manual")
        else:
            zip_code = st.selectbox(
                "ZIP / PIN Code",
                pincode_options,
                help=f"Available pincodes for {selected_city} - helps pharmacy matcher",
                key="xray_pincode"
            )
    
    # Input form
    with st.form("xray_form"):
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### 📋 Patient Snapshot")
            age = st.number_input("Age", min_value=1, max_value=120, value=40, help="Required for dosage safety checks")
            gender = st.selectbox("Gender", ["M", "F", "U"], help="Used for anonymised patient context")
            selected_meds = st.multiselect(
                "Current Medications",
                med_names,
                help="Choose from sample OTC catalog",
            )

        with col2:
            st.markdown("#### 🩺 Presenting Symptoms")
            symptom_choices = list(symptom_display.keys())
            default_symptoms = symptom_choices[:2] if symptom_choices else []
            selected_symptoms = st.multiselect(
                "Primary symptoms",
                symptom_choices,
                default=default_symptoms,
                help="Tags derived from sample medicine indications",
            )
            symptom_notes = st.text_area(
                "Additional notes / history",
                placeholder="Optional clinical summary, vitals, lab findings",
                height=110,
            )
            spo2 = st.slider("SpO2 (%)", min_value=80, max_value=100, value=98)
            allergy_choices = list(allergy_display.keys())
            selected_allergies = st.multiselect(
                "Medication allergies",
                allergy_choices,
                help="Known sensitizers from sample OTC catalog",
            )"""

new_section = """    # Check API status
    api_status, _ = check_api_status()
    if not api_status:
        st.error("❌ **Backend API is offline!** Please start it first: `python api/main.py`")
        return
    
    # Input form with location at the end
    with st.form("xray_form"):
        st.markdown("### 📋 Patient Information")
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### 👤 Basic Details")
            age = st.number_input("Age", min_value=1, max_value=120, value=40, help="Required for dosage safety checks")
            gender = st.selectbox("Gender", ["M", "F", "U"], help="Used for anonymised patient context")
            selected_meds = st.multiselect(
                "Current Medications",
                med_names,
                help="Choose from sample OTC catalog",
            )

        with col2:
            st.markdown("#### 🩺 Presenting Symptoms")
            symptom_choices = list(symptom_display.keys())
            default_symptoms = symptom_choices[:2] if symptom_choices else []
            selected_symptoms = st.multiselect(
                "Primary symptoms",
                symptom_choices,
                default=default_symptoms,
                help="Tags derived from sample medicine indications",
            )
            symptom_notes = st.text_area(
                "Additional notes / history",
                placeholder="Optional clinical summary, vitals, lab findings",
                height=110,
            )
            spo2 = st.slider("SpO2 (%)", min_value=80, max_value=100, value=98)
            allergy_choices = list(allergy_display.keys())
            selected_allergies = st.multiselect(
                "Medication allergies",
                allergy_choices,
                help="Known sensitizers from sample OTC catalog",
            )
        
        st.markdown("---")
        st.markdown("### 📍 Location Information")
        loc_col1, loc_col2 = st.columns(2)
        with loc_col1:
            selected_city = st.selectbox(
                "City", 
                zip_df["city"].unique().tolist(), 
                help="Your city - used for pharmacy matching",
                key="xray_city_form"
            )
        with loc_col2:
            # Get pincodes for selected city
            city_subset = zip_df[zip_df["city"] == selected_city]
            pincode_options = city_subset["pincode"].tolist() if not city_subset.empty else zip_df["pincode"].unique().tolist()
            zip_code = st.selectbox(
                "ZIP / PIN Code",
                pincode_options,
                help="Your pincode - critical for accurate pharmacy matching",
                key="xray_pincode_form"
            )"""

content = content.replace(old_section, new_section)

# Write back
with open("app_integrated.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Successfully restructured X-Ray analysis page")
print("✅ Location section moved after patient information")
print("✅ Location now inside form for better layout")
