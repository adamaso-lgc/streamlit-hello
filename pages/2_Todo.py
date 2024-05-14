import streamlit as st
import pandas as pd
from collections import defaultdict

# Page Configuration
st.set_page_config(
    page_title="Todo Management App",
    page_icon="📝",
)


# Initialize Session State
if 'todo_data' not in st.session_state:
    st.session_state.todo_data = defaultdict(list)

# Page Title
st.title('Todo Management')
st.text('This is a web app to manage your todo items and their time periods.')

# Form for Adding/Updating Todo Items
st.header("Add/Update Todo")
with st.form(key='todo_form'):
    todo_id = st.text_input("Todo ID", key='todo_id')
    todo_name = st.text_input("Todo Name", key='todo_name')
    start_time = st.date_input("Start Date")  # Date Input
    start_hour = st.time_input("Start Time")  # Time Input
    end_time = st.date_input("End Date")  # Date Input
    end_hour = st.time_input("End Time")  # Time Input

    start_datetime = f"{start_time}, {start_hour}"
    end_datetime = f"{end_time}, {end_hour}"

    # Form Submit Button
    submit_button = st.form_submit_button("Add/Update Todo")

# Handle Form Submission
if submit_button:
    # Update the todo item in the session state
    st.session_state.todo_data[todo_id].append([todo_name, start_datetime, end_datetime])
    st.success(f'Todo "{todo_id}" updated successfully!')

# Display the Data
if st.session_state.todo_data:
    st.header("Todo List")
    data = []
    for todo_id, timings in st.session_state.todo_data.items():
        first = True
        for timing in timings:
            if first:
                data.append([todo_id] + timing)
                first = False
            else:
                data.append([''] + timing)

    # Convert to DataFrame for easy manipulation
    todo_df = pd.DataFrame(data, columns=["todoId", "todoName", "startTime", "endTime"])
    st.write(todo_df)

    # Download New CSV Button
    st.download_button(
        label="Download CSV",
        data=todo_df.to_csv(index=False),
        file_name="todo_data.csv",
        mime="text/csv"
    )
else:
    st.write("No todo items available yet.")

# File Upload Section for Merging
st.header("Upload CSV for Merging")
existing_file = st.file_uploader("Select CSV to Append to")

if existing_file:
    existing_df = pd.read_csv(existing_file)
    combined_df = pd.concat([existing_df, todo_df], ignore_index=True)
    combined_df.to_csv('combined_todo_data.csv', index=False)
    st.download_button(
        label="Download Merged CSV",
        data=combined_df.to_csv(index=False),
        file_name="combined_todo_data.csv",
        mime="text/csv"
    )
