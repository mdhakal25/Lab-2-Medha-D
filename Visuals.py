# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
infile = open("data.json", "r")
data = json.load(infile)
infile.close()

df = pd.DataFrame(data[0])

fig, ax = plt.subplots()
ax.bar(df["Student"], df["Screen Time (hours)"])
ax.set_title("Daily Screen Time by Student")
ax.set_xlabel("Student Number")
ax.set_ylabel("Screen Time (hours)")
st.pyplot(fig)
st.subheader("Screen Time vs. Sleep Quality")
if "max_hours" not in st.session_state:
    st.session_state.max_hours = 10
max_hours = st.slider(
    "Maximum Daily Screen Time (hours)",
    min_value=2,
    max_value=10,
    value=st.session_state.max_hours
)
st.session_state.max_hours = max_hours
filtered_df = df[df["Screen Time (hours)"] <= max_hours]
st.scatter_chart(
    filtered_df,
    x="Screen Time (hours)",
    y="Sleep Quality"
)


# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
st.header("Part 2: Survey Results")
csv_df = pd.read_csv("data.csv")

# Convert the survey answers into numbers
csv_df["Screen Time (hours)"] = pd.to_numeric(csv_df["Screen Time (hours)"], errors="coerce")
csv_df["Sleep Quality"] = pd.to_numeric(csv_df["Sleep Quality"], errors="coerce")
csv_df = csv_df.dropna(subset=["Screen Time (hours)", "Sleep Quality"])

# STATIC GRAPH

# STATIC GRAPH
st.subheader("Average Sleep Quality by Screen Time")

average_sleep = csv_df.groupby("Screen Time (hours)")["Sleep Quality"].mean()

fig3, ax3 = plt.subplots()

ax3.bar(
    average_sleep.index,
    average_sleep.values,
    width=0.5
)

ax3.set_title("Average Sleep Quality by Screen Time")
ax3.set_xlabel("Screen Time (hours)")
ax3.set_ylabel("Average Sleep Quality (1-10)")
ax3.set_xticks(average_sleep.index)
ax3.tick_params(axis="x", labelrotation=0)

st.pyplot(fig3)

# DYNAMIC GRAPH
st.subheader("Screen Time vs. Sleep Quality (Survey Responses)")
if "csv_max_hours" not in st.session_state:
    st.session_state.csv_max_hours = 10

csv_max_hours = st.slider(
    "Maximum Screen Time for Survey Responses (hours)",
    min_value=0,
    max_value=10,
    value=st.session_state.csv_max_hours
)

st.session_state.csv_max_hours = csv_max_hours
csv_filtered_df = csv_df[csv_df["Screen Time (hours)"] <= csv_max_hours]
fig2, ax2 = plt.subplots()

ax2.scatter(
    csv_filtered_df["Screen Time (hours)"],
    csv_filtered_df["Sleep Quality"]
)

ax2.set_title("Screen Time vs. Sleep Quality (Survey Data)")
ax2.set_xlabel("Screen Time (hours)")
ax2.set_ylabel("Sleep Quality (1-10)")

st.pyplot(fig2)
