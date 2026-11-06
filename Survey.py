# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Screen Time and Sleep Quality Survey 📱")
st.write("Help us explore the relationship between screen time and sleep quality! Please answer the questions below.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    screen_time_input = st.text_input("How many hours of screen time do you average per day?")
    sleep_quality_input = st.text_input("Rate your sleep quality from 1 to 10:")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.

    # This block runs when the Submit button is clicked.
    if submitted:
        try:
            screen_time = float(screen_time_input)
            sleep_quality = int(sleep_quality_input)

            if screen_time < 0 or screen_time > 24:
                st.error("Screen time must be between 0 and 24 hours.")

            elif sleep_quality < 1 or sleep_quality > 10:
                st.error("Sleep quality must be between 1 and 10.")

            else:
                new_data = pd.DataFrame({
                    "Screen Time (hours)": [screen_time],
                    "Sleep Quality": [sleep_quality]
                })

                file_exists = os.path.exists("data.csv")
                new_data.to_csv("data.csv", mode="a", header=not file_exists, index=False)

                st.success("Your data has been submitted!")
                st.write(
                    f"You entered: **Screen Time:** {screen_time} hours, **Sleep Quality:** {sleep_quality}/10"
                )

        except ValueError:
            st.error("Please enter valid numbers for both questions.")
            
# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")