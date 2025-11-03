import streamlit as st
import plotly.express as px
from utils import apply_shared_style, get_data, refresh_button

st.set_page_config(
    page_title="Job Monitoring — Overview",
    page_icon="📊",
    layout="wide"
)

apply_shared_style()
refresh_button()  # sidebar refresh button

st.markdown("<h1>Job Monitoring Dashboard — Overview</h1>", unsafe_allow_html=True)

df = get_data(40)
st.write(f"Loaded {len(df)} rows (overview dataset).")

st.sidebar.header("Filters")
status_filter = st.sidebar.multiselect(
    "Status", options=df["Status"].unique(), default=list(df["Status"].unique())
)
search_job = st.sidebar.text_input("Search job name")

filtered = df[df["Status"].isin(status_filter)]
if search_job:
    filtered = filtered[filtered["Job Name"].str.contains(search_job, case=False)]

st.write(f"Showing {len(filtered)} rows after filters.")

total = len(filtered)
succ = len(filtered[filtered["Status"] == "Success"])
failed = len(filtered[filtered["Status"] == "Failed"])
running = len(filtered[filtered["Status"] == "Running"])

st.markdown(f"""
<div style="display:flex; gap:16px; margin-bottom:18px;">
  <div class="kpi-card" style="background:#4CAF50; width:22%; text-align:center;">
    <div style="font-size:14px;">Total Jobs</div>
    <div style="font-size:26px; font-weight:700;">{total}</div>
  </div>
  <div class="kpi-card" style="background:#2196F3; width:22%; text-align:center;">
    <div style="font-size:14px;">Successful</div>
    <div style="font-size:26px; font-weight:700;">{succ}</div>
  </div>
  <div class="kpi-card" style="background:#f44336; width:22%; text-align:center;">
    <div style="font-size:14px;">Failed</div>
    <div style="font-size:26px; font-weight:700;">{failed}</div>
  </div>
  <div class="kpi-card" style="background:#ff9800; width:22%; text-align:center;">
    <div style="font-size:14px;">Running</div>
    <div style="font-size:26px; font-weight:700;">{running}</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h2>Overview Charts</h2>", unsafe_allow_html=True)
c1, c2 = st.columns([2,1])

with c1:
    fig = px.bar(
        filtered.sort_values("Duration (min)", ascending=False).head(20),
        x="Job Name", y="Duration (min)", color="Status",
        color_discrete_map={
            "Success":"#2ca02c",
            "Failed":"#d62728",
            "Running":"#ff7f0e",
            "Queued":"#9467bd"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig2 = px.pie(
        filtered, names="Status",
        color_discrete_map={
            "Success":"#2ca02c",
            "Failed":"#d62728",
            "Running":"#ff7f0e",
            "Queued":"#9467bd"
        }
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("### Recent jobs")
st.dataframe(filtered.sort_values("Start Time", ascending=False).reset_index(drop=True))
