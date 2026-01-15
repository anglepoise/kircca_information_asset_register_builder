import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="IAR Portal", layout="wide")

# --- SIDEBAR HELP SECTION ---
with st.sidebar:
    st.title("📖 Guidance")
    st.info("""
    **What is an Information Asset?**
    A body of information, defined and managed as a single entity, so it can be understood, shared, protected and exploited efficiently.
    """)
    st.divider()
    st.markdown("""
    ### Compliance Checklist
    * [ ] Asset Name & Owner
    * [ ] Security Classification
    * [ ] Risks Identified
    * [ ] Audit Dates
    """)
    st.warning("⚠️ Remember to download the CSV before closing this browser tab!")

# --- PROGRESS TRACKING ---
st.title("🛡️ Information Asset Register Portal")
# Simple logic to calculate progress based on some key fields
fields_to_check = ['asset_name', 'owner', 'purpose', 'location']
completed = 0
# (Internal logic to check session state for progress would go here)

# --- THE FORM ---
with st.form("iar_form", clear_on_submit=True):
    
    # Progress bar (Visual cue for user)
    st.write("Current Entry Progress")
    st.progress(0) # Starts at 0, you can update this based on input

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.subheader("📋 Core Identity")
        asset_name = st.text_input("1. Information Asset Name*", placeholder="e.g., Client Billing Folder")
        owner = st.text_input("6. Information Asset Owner*", placeholder="e.g., Jane Smith (Head of Finance)")
        
        st.divider()
        st.subheader("🏢 Supply Chain")
        supplier = st.text_input("2a. Supplier Name")
        contract_loc = st.text_input("2b. Contract Location", help="Where is the physical or digital contract stored?")
        contract_dates = st.text_input("2c. Contract Dates", placeholder="e.g., 01/2024 - 01/2025")

    with col_right:
        st.subheader("🔍 Data Scope")
        purpose = st.text_area("3. What & Why?", help="Detail the type of data and the business reason for keeping it.")
        location = st.text_input("4. Location", placeholder="e.g., Azure Cloud, Locked Cabinet #4")
        special_cat = st.radio("5. Does this contain special category data?", ["No", "Yes"], horizontal=True, help="Racial/ethnic origin, political opinions, health data, etc.")

    st.divider()

    # Shared Logic
    st.subheader("🌐 External Sharing")
    is_shared = st.selectbox("7. Is the Information Shared Externally?", 
                            ["No", "Yes - Received from outside", "Yes - Shared externally", "Yes - Both"])
    
    if "Yes" in is_shared:
        ropa_status = st.selectbox("8. Is this on the Record of Processing Activities (ROPA)?", ["Yes", "No", "Under Review"])
    else:
        ropa_status = "N/A"

    st.divider()

    # Risk & Audit
    st.subheader("⚖️ Risk & Governance")
    r1, r2 = st.columns(2)
    with r1:
        risks = st.text_area("9. Breach Risks", placeholder="e.g., Identity theft, financial loss...")
        measures = st.text_area("10. Security Measures", placeholder="e.g., MFA, Encryption, Physical Keys...")
    
    with r2:
        is_mobile = st.checkbox("📱 This is a Mobile Device")
        if is_mobile:
            st.caption("Please provide issuance details:")
            d_issue = st.date_input("11. Date Issued", value=None)
            d_return = st.date_input("12. Date Returned", value=None)
        else:
            d_issue, d_return = "N/A", "N/A"

    # Final Audit Section
    st.subheader("📅 Audit Trail")
    a1, a2, a3 = st.columns(3)
    with a1:
        last_audit = st.date_input("13. Date of Last Audit")
    with a2:
        breach_found = st.selectbox("14. Breach Since Last Audit?", ["No", "Yes"])
    with a3:
        if breach_found == "Yes":
            breach_actions = st.selectbox("15. All Actions Taken?", ["Yes", "No", "In Progress"])
        else:
            breach_actions = "N/A"

    # Submission
    submitted = st.form_submit_button("✅ Save Asset to List")
    
    if submitted:
        if not asset_name or not owner:
            st.error("Missing required fields: Asset Name and Owner are mandatory.")
        else:
            # Logic to save to session state (same as previous code)
            st.session_state.iar_list.append({"Name": asset_name, "Owner": owner, "Audit": last_audit}) # etc
            st.success("Asset added! Scroll down to see the table.")

# --- DATA TABLE & DOWNLOAD ---
if st.session_state.iar_list:
    st.divider()
    df = pd.DataFrame(st.session_state.iar_list)
    st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Excel-Ready Register (CSV)", data=csv, file_name="IAR_Complete.csv")
