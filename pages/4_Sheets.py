import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.title('Todo Sheets')
st.text('This is a web app to manage Google Sheets for todo events.')

# Establish connection
conn = st.connection("gsheets", type=GSheetsConnection)

def create_datetime_string(date, time):
    return datetime.combine(date, time).strftime('%Y-%m-%d, %H:%M:%S')

def fetch_todos():
    existing_data = conn.read(worksheet="Todo", usecols=list(range(4)), ttl=5)
    existing_data = existing_data.dropna(how="all")
    if existing_data.empty:
        return pd.DataFrame(columns=['todoId', 'todoName', 'startTime', 'endTime'])
    df = pd.DataFrame(existing_data, columns=['todoId', 'todoName', 'startTime', 'endTime'])
    return df

todos_df = fetch_todos()  # Fetch data once

with st.form("new_todo_form"):
    todo_id = st.text_input("Todo ID")
    todo_name = st.text_input("Todo Name (only if new)")
    start_date = st.date_input("Start Date")
    start_time = st.time_input("Start Time")
    end_date = st.date_input("End Date")
    end_time = st.time_input("End Time")
    
    start_datetime = create_datetime_string(start_date, start_time)
    end_datetime = create_datetime_string(end_date, end_time)
    
    submitted = st.form_submit_button("Add New Event")
    if submitted:
        new_event = pd.DataFrame({
            'todoId': [None],
            'todoName': [None],
            'startTime': [start_datetime],
            'endTime': [end_datetime]
        })

        if todo_id in todos_df['todoId'].values:
            # Find the last occurrence of todoId
            last_todo_index = todos_df[todos_df['todoId'] == todo_id].index[-1]
            insert_position = last_todo_index + 1

            # Find the first non-empty row after the last_todo_index
            for i in range(insert_position, len(todos_df)):
                if todos_df.at[i, 'todoId'] != '' and not pd.isna(todos_df.at[i, 'todoId']):
                    insert_position = i
                    break
            else:
                # If no non-empty row is found, append at the end
                insert_position = len(todos_df)

            todos_df = pd.concat([todos_df.iloc[:insert_position], new_event, todos_df.iloc[insert_position:]]).reset_index(drop=True)
        else:
            # New todoId, append at the end
            new_event['todoId'] = todo_id
            new_event['todoName'] = todo_name
            todos_df = pd.concat([todos_df, new_event]).reset_index(drop=True)

        conn.update(worksheet="Todo", data=todos_df.to_dict('list'))  # Update Google Sheets
        st.success("Event added successfully!")
              

# Display the current todo events
with st.expander("Current Todos ⤵", expanded=True):
    st.dataframe(todos_df)


