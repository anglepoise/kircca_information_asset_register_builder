import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="IAR Portal", layout="wide")

st.markdown("""
    <style>
    .stForm {
        background-color: #39542C;
    }
    /* This targets the labels above text inputs, select boxes, etc. */
    label {
        color: white !important;
        font-weight: bold;
        font-size: 1.6rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA PERSISTENCE LOGIC ---
if 'iar_list' not in st.session_state:
    st.session_state.iar_list = pd.DataFrame()

# --- SIDEBAR & UPLOAD ---
with st.sidebar:
    st.title("📂 Resume Progress")
    uploaded_file = st.file_uploader("Upload an existing IAR (CSV)", type="csv")
    
    if uploaded_file is not None:
        try:
            # Load the uploaded file into session state
            uploaded_df = pd.read_csv(uploaded_file)
            st.session_state.iar_list = uploaded_df
            st.success("Existing data loaded!")
        except Exception as e:
            st.error(f"Error loading file: {e}")

    st.divider()
    st.info("💡 **Tip:** Upload your previous file here to add new assets without starting from scratch.")

# Your original options (any order)
assets = [
    "Care Plans",
    "Care Planning Software",
    "Rota Planning Software",
    "Care Record Filing System",
    "Accounting Software",
    "HR Software",
    "CCTV Records",
    "Mobile Device",
]

# Locations
locations = [
    "On-Premises",
    "Off Site Storage",
    "Cloud Storage",
    "Third-Party Data Center",
    "Local Server Room",
    "Remote Workstations",
]

# Sort alphabetically
assets_sorted = sorted(assets)
locations_sorted = sorted(locations)

# Add "Other" as the final option
assets_sorted.append("Other")
locations_sorted.append("Other")

# --- THE FORM ---
st.title("🛡️ Information Asset Register Portal (version 1.1)")

with st.form("iar_form", clear_on_submit=True):
    st.subheader("➕ Add New Asset Entry")
    
    # Grid Layout for Inputs
    col1, col2 = st.columns(2)
    with col1:
        # Streamlit selectbox

        asset_name = st.selectbox("1. Information Asset Name*", assets_sorted )
        
        # Other asset name input
        other_value = None
        if asset_name == "Other":
            other_value = st.text_input("Please specify:")
            st.write("TESTING Selected option:", asset_name)

        if other_value:
            st.write("TESTING Other value:", other_value)
        
        owner = st.text_input("6. Asset Owner*")
        supplier = st.text_input("2a. Supplier Name")
        purpose = st.text_area("3. What & Why?")
    
    with col2:
        location = st.selectbox("4. Location*", locations_sorted )
        is_shared = st.selectbox("7. Shared Externally?", ["No", "Yes"])
        risks = st.text_area("9. Breach Risks")
        # is_mobile = st.checkbox("📱 This is a Mobile Device")

    # Audit & Security (Simplified for brevity)
    st.divider()
    c3, c4 = st.columns(2)
    with c3:
        last_audit = st.date_input("13. Date of Last Audit")
    with c4:
        breach_found = st.selectbox("14. Breach Since Last Audit?", ["No", "Yes"])

    submitted = st.form_submit_button("Append to Register")

    if submitted:
        if not asset_name or not owner:
            st.error("Please fill in the Asset Name and Owner.")
        else:
            # Create a dictionary for the new row
            new_row = {
                "Asset Name": asset_name,
                "Owner": owner,
                "Supplier": supplier,
                "Purpose": purpose,
                "Location": location,
                "Shared Externally": is_shared,
                "Breach Risks": risks,
                "Mobile Device": "Yes" if is_mobile else "No",
                "Last Audit": str(last_audit),
                "Breach Since Audit": breach_found
            }
            
            # Append new row to the session dataframe
            new_df = pd.DataFrame([new_row])
            st.session_state.iar_list = pd.concat([st.session_state.iar_list, new_df], ignore_index=True)
            st.success(f"Added '{asset_name}' to the list!")

# --- DISPLAY & DOWNLOAD ---
if not st.session_state.iar_list.empty:
    st.divider()
    st.subheader("📑 Current Register Preview")
    st.dataframe(st.session_state.iar_list, use_container_width=True)

    # Export to CSV
    csv_output = st.session_state.iar_list.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Updated IAR",
        data=csv_output,
        file_name=f"IAR_Export_{date.today()}.csv",
        mime="text/csv"
    )

    if st.button("🗑️ Clear All Rows (Reset)"):
        st.session_state.iar_list = pd.DataFrame()
        st.rerun()
