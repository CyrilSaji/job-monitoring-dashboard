import streamlit as st
from utils import apply_shared_style, get_data, refresh_button

st.set_page_config(page_title="Job Monitoring — Job Details", layout="wide")
apply_shared_style()
refresh_button()

st.markdown("<h1>Job Details</h1>", unsafe_allow_html=True)

df = get_data(200)
st.write(f"Loaded {len(df)} rows (job details dataset).")

st.sidebar.header("Job Details Filters")
status = st.sidebar.multiselect("Status", options=df["Status"].unique(), default=list(df["Status"].unique()))
owner = st.sidebar.multiselect("Owner", options=df["Owner"].unique(), default=list(df["Owner"].unique()))
group = st.sidebar.multiselect("Group", options=df["Group"].unique(), default=list(df["Group"].unique()))
search = st.sidebar.text_input("Search Job")

filtered = df[df["Status"].isin(status) & df["Owner"].isin(owner) & df["Group"].isin(group)]
if search:
    filtered = filtered[filtered["Job Name"].str.contains(search, case=False)]

st.write(f"Showing {len(filtered)} jobs after filters.")

if filtered.empty:
    st.warning("No jobs match the selected filters.")
else:
    st.dataframe(filtered.sort_values(["Start Time"], ascending=False).reset_index(drop=True))
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(label="Download filtered CSV", data=csv, file_name="job_details_filtered.csv", mime="text/csv")
