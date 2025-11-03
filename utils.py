import streamlit as st
import pandas as pd
import numpy as np
import base64
import os
import time

@st.cache_data
def get_data(n: int = 40, seed: int = 123) -> pd.DataFrame:
    """Return a simulated jobs DataFrame (cached)."""
    # Use dynamic seed from session_state if available
    seed = st.session_state.get("_refresh_time", seed)
    np.random.seed(int(seed) % (2**32 - 1))
    
    rng = pd.date_range("2025-09-20 08:00", periods=n, freq="h")  # lowercase 'h' to avoid FutureWarning
    data = pd.DataFrame({
        "Job Name": [f"Job_{i:03d}" for i in range(1, n+1)],
        "Status": np.random.choice(["Success", "Failed", "Running", "Queued"], n, p=[0.6,0.15,0.2,0.05]),
        "Duration (min)": np.random.randint(1, 240, size=n),
        "Start Time": rng,
        "Owner": np.random.choice(["team-a","team-b","etl-team","ops"], n),
        "Group": np.random.choice(["ETL","Ingest","Reporting","Batch"], n)
    })
    return data

@st.cache_data
def compute_job_sla(df: pd.DataFrame) -> pd.DataFrame:
    """Compute SLA summary per job."""
    jobs = df["Job Name"].unique()
    rows = []
    rng = np.random.RandomState(42)
    for job in jobs:
        job_rows = df[df["Job Name"] == job]
        base = 90 + rng.randint(-5, 6)
        success_like = (job_rows["Status"] == "Success").sum()
        if success_like == 0:
            base -= rng.randint(0, 10)
        sla = int(np.clip(base + rng.randint(-8, 8), 60, 100))
        avg_duration = int(job_rows["Duration (min)"].mean()) if not job_rows.empty else int(rng.randint(5,120))
        failed_runs_24h = int(np.clip(rng.poisson(lam=1.5), 0, 20))
        owner = job_rows["Owner"].iloc[0] if not job_rows.empty else rng.choice(["team-a","team-b","etl-team","ops"])
        group = job_rows["Group"].iloc[0] if not job_rows.empty else rng.choice(["ETL","Ingest","Reporting","Batch"])
        rows.append({
            "Job Name": job,
            "Owner": owner,
            "Group": group,
            "SLA Compliance (%)": sla,
            "Avg Duration (min)": avg_duration,
            "Failed Runs (last 24h)": failed_runs_24h
        })
    sla_df = pd.DataFrame(rows).sort_values("SLA Compliance (%)", ascending=False).reset_index(drop=True)
    return sla_df

def apply_shared_style(background_image: str = "background.png", overlay_alpha: float = 0.2, brightness: float = 1.08) -> None:
    """Apply background image, overlay, fonts, and styling."""
    overlay_alpha = max(0.0, min(1.0, float(overlay_alpha)))
    try:
        brightness = float(brightness)
    except Exception:
        brightness = 1.08

    bg_css = ""
    found_msg = ""
    try:
        if os.path.exists(background_image):
            with open(background_image, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            bg_url = f"data:image/png;base64,{data}"
            bg_css = f"""
                .stApp {{
                    background-image: url("{bg_url}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                    filter: brightness({brightness});
                }}
            """
            found_msg = f"Background image '{background_image}' embedded (brightness={brightness})."
        else:
            bg_css = """
                .stApp {
                    background: linear-gradient(180deg, #f7fbfe 0%, #ffffff 100%);
                }
            """
            found_msg = f"Background image '{background_image}' not found. Using gradient fallback."
    except Exception as e:
        bg_css = """
            .stApp {
                background: linear-gradient(180deg, #f7fbfe 0%, #ffffff 100%);
            }
        """
        found_msg = f"Error embedding background: {e}. Using gradient fallback."

    css = f"""
    <style>
    {bg_css}

    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(245,247,250,{overlay_alpha});
        pointer-events: none;
        z-index: 0;
    }}

    .main > div {{
        z-index: 1;
    }}

    h1 {{ color: #1f77b4; font-family: "Segoe UI", Roboto, Arial, sans-serif; }}
    h2 {{ color: #ff7f0e; font-family: "Segoe UI", Roboto, Arial, sans-serif; }}
    h3 {{ color: #2ca02c; font-family: "Segoe UI", Roboto, Arial, sans-serif; }}

    .kpi-card {{
        padding: 14px;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 10px rgba(31,119,180,0.06);
    }}

    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(0,0,0,0.12); border-radius: 10px; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    st.session_state.setdefault("_bg_info_shown", False)
    if not st.session_state["_bg_info_shown"]:
        st.info(f"{found_msg} Overlay alpha={overlay_alpha}")
        st.session_state["_bg_info_shown"] = True

def refresh_button(key: str = "refresh_data"):
    """
    Add refresh button in sidebar.
    Clears cache and sets a dynamic seed to generate new data.
    """
    if st.sidebar.button("🔄 Refresh Data", key=key):
        st.cache_data.clear()
        st.session_state["_refresh_time"] = time.time()
        st.experimental_rerun()
