import streamlit as st
import plotly.express as px
from utils import apply_shared_style, get_data, compute_job_sla, refresh_button

st.set_page_config(
    page_title="Job Monitoring — SLA Tracking",
    layout="wide"
)

# Apply shared background, styling, overlay
apply_shared_style()

# Sidebar refresh button
refresh_button()

st.markdown("<h1>SLA Tracking</h1>", unsafe_allow_html=True)

# Load data
df = get_data(200)
st.write(f"Loaded {len(df)} rows (base data for SLA).")

# Compute SLA summary
sla_df = compute_job_sla(df)
st.write(f"Computed SLA for {len(sla_df)} jobs.")

# Sidebar filters
st.sidebar.header("SLA Filters")
group_filter = st.sidebar.multiselect(
    "Group", options=sla_df["Group"].unique(), default=list(sla_df["Group"].unique())
)
owner_filter = st.sidebar.multiselect(
    "Owner", options=sla_df["Owner"].unique(), default=list(sla_df["Owner"].unique())
)

# Apply filters
display = sla_df[sla_df["Group"].isin(group_filter) & sla_df["Owner"].isin(owner_filter)]
st.write(f"Showing {len(display)} SLA rows after filters.")

# Display SLA table
if display.empty:
    st.warning("No SLA rows match the selected filters.")
else:
    st.dataframe(display.sort_values("SLA Compliance (%)", ascending=False).reset_index(drop=True))

    # SLA Compliance Chart
    st.markdown("### SLA Compliance Chart")
    fig = px.bar(
        display.sort_values("SLA Compliance (%)"),
        x="Job Name",
        y="SLA Compliance (%)",
        color="SLA Compliance (%)",
        color_continuous_scale=["#d62728","#ff7f0e","#2ca02c"]
    )
    st.plotly_chart(fig, use_container_width=True)

    # Alerts for low SLA (<90%)
    low = display[display["SLA Compliance (%)"] < 90]
    if not low.empty:
        st.markdown("### Alerts 🚨")
        # Display 3 cards per row
        for i in range(0, len(low), 3):
            cols = st.columns(3)
            for j, idx in enumerate(range(i, min(i+3, len(low)))):
                row = low.iloc[idx]
                with cols[j]:
                    st.markdown(f"""
                    <div style='
                        padding:12px;
                        border-radius:10px;
                        background:#f8d7da;
                        color:#721c24;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                        margin-bottom:8px;
                    '>
                        <b>{row['Job Name']}</b><br>
                        SLA: {row['SLA Compliance (%)']}%<br>
                        Failed runs (24h): {row['Failed Runs (last 24h)']}<br>
                        Group: {row['Group']}<br>
                        Owner: {row['Owner']}
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.success("All selected SLAs are healthy ✅")
