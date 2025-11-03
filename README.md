# Job Monitoring Dashboard (Simulated Autosys)

Professional Streamlit dashboard (majorly Python) that simulates Autosys job runs with SLA tracking.

## Quick start (local)
1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. Open http://localhost:8501

## What is included
- `app.py` : main Streamlit app
- `simulated_data.py`: generates and steps simulated Autosys jobs
- `utils.py`: helper functions (KPIs, SLA checks, upstream chain)
- `assets/logo.png`: placeholder logo
- `requirements.txt`, `Dockerfile`, and small `frontend/` stub
- `azure-deploy.md` with deployment notes
