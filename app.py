import streamlit as st
import pandas as pd
import requests
from collections import Counter
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="skillscope-dashboard",
    page_icon="📊",
    layout="wide"
)

# Dashboard Title
st.title("📊 Automated Skillscope Dashboard")

st.markdown("Analyze trending technologies from live job postings.")

# API URL
url = "https://remotive.com/api/remote-jobs"

# Fetch API Data
response = requests.get(url)
data = response.json()

# Keywords
keywords = [
    "Python",
    "AWS",
    "Docker",
    "SQL",
    "Kubernetes",
    "Java",
    "React",
    "Machine Learning"
]

skills = []
job_titles = []

# Analyze Jobs
for job in data['jobs']:

    description = job['description']
    title = job['title']

    job_titles.append(title)

    for keyword in keywords:
        if keyword.lower() in description.lower():
            skills.append(keyword)

# Count Skills
skill_count = Counter(skills)

# Convert to DataFrame
df = pd.DataFrame(
    skill_count.items(),
    columns=["Skill", "Count"]
)

# Sort Values
df = df.sort_values(by="Count", ascending=False)

# Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs Analyzed", len(data['jobs']))
col2.metric("Unique Skills Tracked", len(df))
col3.metric("Top Skill", df.iloc[0]["Skill"])

st.divider()

# Sidebar Filter
st.sidebar.header("Dashboard Filters")

selected_skills = st.sidebar.multiselect(
    "Select Skills",
    df["Skill"],
    default=df["Skill"]
)

filtered_df = df[df["Skill"].isin(selected_skills)]

# Data Table
st.subheader("📋 Skill Demand Table")
st.dataframe(filtered_df, use_container_width=True)

# Bar Chart
st.subheader("📈 Skill Demand Bar Chart")

st.bar_chart(filtered_df.set_index("Skill"))

# Pie Chart
st.subheader("🥧 Skill Distribution")

fig = px.pie(
    filtered_df,
    names="Skill",
    values="Count",
    title="Technology Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# Top Job Titles
st.subheader("💼 Sample Job Titles")

top_titles = pd.DataFrame(job_titles[:10], columns=["Job Titles"])

st.table(top_titles)

# Footer
st.markdown("---")
st.markdown("Built using Python, Streamlit, and Live Job APIs")
