import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Hello World App",
    page_icon="👋",
)

st.title('Hello World')
st.text('This is a web app to export data to csv')
st.markdown('This is **markdown**')

uploaded_file = st.file_uploader('Upload your file here')

if uploaded_file:
    st.header('Table Statics')
    df = pd.read_csv(uploaded_file)
    st.write(df.describe())

    st.header('Table Title')
    st.write(df.head())

# Persistent Data Storage
if 'form_data_list' not in st.session_state:
    st.session_state.form_data_list = []

# Form Section
st.title("Form to CSV")

form_data = {
    "name": st.text_input("Name"),
    "age": st.number_input("Age", 0, 120),
    "email": st.text_input("Email"),
    "phone": st.text_input("Phone")
}

if st.button("Add Line"):
    st.session_state.form_data_list.append(form_data)
    st.success("Line added to table!")

# Display Table of Entries
if st.session_state.form_data_list:
    st.header("Entries")
    entries_df = pd.DataFrame(st.session_state.form_data_list)
    st.write(entries_df)

# Create or Append CSV Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Create New CSV"):
        entries_df.to_csv('new_form_data.csv', index=False)
        st.download_button(
            label="Download New CSV",
            data=entries_df.to_csv(index=False),
            file_name="new_form_data.csv"
        )

with col2:
    existing_file = st.file_uploader("Select CSV to Append to")
    if existing_file:
        existing_df = pd.read_csv(existing_file)
        combined_df = pd.concat([existing_df, entries_df], ignore_index=True)
        combined_df.to_csv('combined_form_data.csv', index=False)
        st.download_button(
            label="Download Combined CSV",
            data=combined_df.to_csv(index=False),
            file_name="combined_form_data.csv"
        )