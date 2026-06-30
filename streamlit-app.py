import streamlit as st
from datetime import datetime

# Define standard stand lists
REC_STANDS = ["Rec 1", "Rec 2", "Rove 1", "Rec 3", "Rove 2"]
COMP_STANDS = ["Comp 1", "Comp 2", "Comp 3", "Comp 4"]
SLIDE_STANDS = ["Top Slide", "Bottom Slide"]

# Set up page config
st.set_page_config(page_title="Lifeguard Rotation Calculator", layout="centered")
st.title("🛟 Lifeguard Rotation Calculator")

# --- UI Layout using Columns ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("⏱️ Shift Times")
    # Time entry layout
    t_start_col, ampm_start_col = st.columns([2, 1])
    with t_start_col:
        shift_start_input = st.text_input("Shift Start (e.g., 10:15)", value="10:00")
    with ampm_start_col:
        shift_start_ampm = st.selectbox("AM/PM", ["AM", "PM"], key="start_ampm")

    t_end_col, ampm_end_col = st.columns([2, 1])
    with t_end_col:
        shift_end_input = st.text_input("Shift End (e.g., 2:45)", value="4:00")
    with ampm_end_col:
        shift_end_ampm = st.selectbox("AM/PM", ["AM", "PM"], key="end_ampm", index=1)

with col2:
    st.subheader("⚙️ Rotation Options")
    rec_open = st.checkbox("Rec open?", value=True)
    
    # Conditional sub-options for Rec
    rec_split = False
    rec_extra = False
    if rec_open:
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            rec_split = st.checkbox("Rec split?", value=True)
        with sub_col2:
            rec_extra = st.checkbox("Rec extra?", value=False)
            
    comp_open = st.checkbox("Comp open?", value=True)
    
    # Conditional sub-options for Comp
    comp_split = False
    if comp_open:
        comp_split = st.checkbox("Comp split?", value=False)
        if comp_split:
            st.caption("Select Active Comp Stands:")
            comp_selections = {
                "Comp 1": st.checkbox("1", value=False),
                "Comp 2": st.checkbox("2", value=False),
                "Comp 3": st.checkbox("3", value=False),
                "Comp 4": st.checkbox("4", value=False),
            }

    slide_open = False
    if rec_open: # Slide option only shows if rec is open based on your original logic
        slide_open = st.checkbox("Slide open?", value=True)

st.write("---")

# --- Dynamic Break Spinboxes ---
st.subheader("☕ Breaks After Stands")
b_col1, b_col2, b_col3, b_col4 = st.columns(4)

with b_col1:
    rec_break_count = st.number_input("Rec Breaks", min_value=0, max_value=4, value=2) if rec_open else 0
with b_col2:
    rec_split_break_count = st.number_input("Split Breaks", min_value=0, max_value=4, value=2) if (rec_open and rec_split) else 0
with b_col3:
    comp_break_count = st.number_input("Comp Breaks", min_value=0, max_value=4, value=2) if comp_open else 0
with b_col4:
    slide_break_count = st.number_input("Slide Breaks", min_value=0, max_value=4, value=1) if slide_open else 0


# --- Build the Rotation Dynamically ---
full_rotation = []

if comp_open:
    if comp_split:
        for stand, active in comp_selections.items():
            if active:
                full_rotation.append(stand)
    else:
        full_rotation.extend(COMP_STANDS)
        
    for i in range(1, comp_break_count + 1):
        full_rotation.append(f"Comp Break {i}")

if rec_open:
    for stand in REC_STANDS:
        full_rotation.append(stand)
        if stand == "Rec 2":
            if rec_extra:
                full_rotation.append("Rec Extra")
            if rec_split:
                for i in range(1, rec_split_break_count + 1):
                    full_rotation.append(f"Rec Split Break {i}")

    for i in range(1, rec_break_count + 1):
        full_rotation.append(f"Rec Break {i}")

if slide_open:
    full_rotation.extend(SLIDE_STANDS)
    for i in range(1, slide_break_count + 1):
        full_rotation.append(f"Slide Break {i}")


st.write("---")

# --- Starting Location & Calculation ---
st.subheader("📍 Deployment")
starting_stand = st.selectbox("Which stand are you starting on?", options=full_rotation if full_rotation else ["No active stands"])

if st.button("Calculate Rotation", type="primary"):
    if not full_rotation:
        st.error("The rotation list is empty! Please enable some stands.")
    else:
        time_format = "%I:%M %p"
        shift_start_time = f"{shift_start_input.strip()} {shift_start_ampm}"
        shift_end_time = f"{shift_end_input.strip()} {shift_end_ampm}"
        
        try:
            parsed_start = datetime.strptime(shift_start_time, time_format)
            parsed_end = datetime.strptime(shift_end_time, time_format)
            
            # Handle overnight shifts or direct comparisons
            time_diff = parsed_end - parsed_start
            h, m, _ = map(int, str(time_diff).split(':'))
            decimal_time = h + (m / 60)
            
            if decimal_time <= 0:
                st.error("Shift end time must be after shift start time.")
            else:
                total_rotations = int(decimal_time / 0.25) # 15 min intervals
                
                if starting_stand not in full_rotation:
                    st.error("Selected starting stand is no longer in the rotation.")
                else:
                    start_index = full_rotation.index(starting_stand)
                    end_index = ((start_index + total_rotations) % len(full_rotation)) - 1
                    end_stand = full_rotation[end_index]
                    
                    # Output clear metrics card style
                    st.success("### Calculations Complete!")
                    st.info(f"""
                    * **Shift Start:** {shift_start_time}
                    * **Shift End:** {shift_end_time}
                    * **Total Shift Length:** {decimal_time:.2f} hours ({total_rotations} intervals)
                    
                    👉 If you go out to **{starting_stand}** at **{shift_start_time}**, you'll end your shift on **{end_stand}**.
                    """)
                    
        except ValueError:
            st.error("Execution failed. Please make sure time fields match standard HH:MM formats (e.g., 10:15).")