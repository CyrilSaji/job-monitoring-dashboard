# simulated_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

STATUSES = ["RUNNING", "COMPLETED", "FAILED", "QUEUED"]

def generate_jobs(n=80, start_time=None):
    if start_time is None:
        start_time = datetime.utcnow()

    jobs = []
    for i in range(n):
        job_id = f"JOB_{i+1:03d}"
        status = random.choices(STATUSES, weights=[0.25,0.5,0.15,0.1])[0]
        run_duration = max(1, int(random.gauss(10, 5)))  # in minutes
        sla = random.choice([5,10,15,30,60])
        start = start_time - timedelta(minutes=random.randint(0, 180))
        end = start + timedelta(minutes=run_duration) if status in ("COMPLETED","FAILED") else None
        next_run = start_time + timedelta(minutes=random.randint(5, 120))

        jobs.append({
            "job_id": job_id,
            "job_name": job_id,
            "status": status,
            "start_time": start,
            "end_time": end,
            "duration_min": run_duration,
            "sla_min": sla,
            "next_run": next_run,
            "owner": random.choice(["team-a","team-b","team-c"]),
            "host": random.choice(["host1","host2","host3"]),
        })

    df = pd.DataFrame(jobs)

    # Create random upstream dependencies (DAG-ish)
    upstream_map = {r["job_id"]: [] for _, r in df.iterrows()}
    all_jobs = list(upstream_map.keys())
    for job in all_jobs:
        k = random.choices([0,1,2], weights=[0.5,0.35,0.15])[0]
        if k > 0:
            upstreams = random.sample([j for j in all_jobs if j != job], k)
            upstream_map[job] = upstreams

    df["upstream"] = df["job_id"].map(upstream_map)
    df["last_updated"] = datetime.utcnow()

    return df

def step_simulation(df: pd.DataFrame):
    df = df.copy()
    now = datetime.utcnow()

    for idx, row in df.sample(frac=0.25).iterrows():
        if row["status"] == "RUNNING":
            r = random.random()
            if r < 0.12:
                df.at[idx, "status"] = "FAILED"
                df.at[idx, "end_time"] = now
            elif r < 0.6:
                df.at[idx, "status"] = "COMPLETED"
                df.at[idx, "end_time"] = now
        elif row["status"] == "QUEUED":
            if random.random() < 0.5:
                df.at[idx, "status"] = "RUNNING"
                df.at[idx, "start_time"] = now
        elif row["status"] == "COMPLETED":
            if random.random() < 0.15:
                df.at[idx, "status"] = "QUEUED"
                df.at[idx, "start_time"] = now + timedelta(minutes=random.randint(1,60))
                df.at[idx, "end_time"] = None
        elif row["status"] == "FAILED":
            if random.random() < 0.3:
                df.at[idx, "status"] = "QUEUED"
                df.at[idx, "start_time"] = now + timedelta(minutes=random.randint(1,60))
                df.at[idx, "end_time"] = None

        df.at[idx, "last_updated"] = now

    df["duration_min"] = df.apply(lambda r: ( (r["end_time"] - r["start_time"]).total_seconds()/60 ) if pd.notnull(r.get("end_time")) and pd.notnull(r.get("start_time")) else r["duration_min"], axis=1)
    return df
