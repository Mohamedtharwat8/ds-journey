"""Generate a realistic (and intentionally messy) service-desk tickets dataset."""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)          # seed → نفس النتيجة عند أي حد
n = 500

categories  = ["Network", "Access", "Hardware", "Software", "Email"]
priorities  = ["Low", "Medium", "High", "Critical"]
departments = ["HR", "Finance", "IT", "Legal", "Operations"]

created  = pd.Timestamp("2026-01-01") + pd.to_timedelta(rng.integers(0, 270 * 24, n), unit="h")
priority = rng.choice(priorities, n, p=[0.35, 0.35, 0.20, 0.10])

# متوسط وقت الحل بيقل كل ما الأولوية تزيد
base_hours = {"Low": 30, "Medium": 18, "High": 8, "Critical": 3}
hours = np.array([rng.exponential(base_hours[p]) for p in priority]).round(1)

df = pd.DataFrame({
    "ticket_id": np.arange(1001, 1001 + n),
    "created_at": created,
    "category": rng.choice(categories, n, p=[0.30, 0.25, 0.15, 0.20, 0.10]),
    "priority": priority,
    "department": rng.choice(departments, n),
    "language": rng.choice(["ar", "en"], n, p=[0.6, 0.4]),
    "resolution_hours": hours,
    "satisfaction": rng.integers(1, 6, n).astype(float),   # 1..5
})

# ---------- inject realistic mess (زي الحقيقة) ----------
df.loc[rng.choice(n, 25, replace=False), "satisfaction"] = np.nan        # عميل ما قيّمش
df.loc[rng.choice(n, 10, replace=False), "resolution_hours"] = np.nan    # لسه ما اتقفلتش
df.loc[rng.choice(n, 5, replace=False), "resolution_hours"] = -1         # bug في النظام
df.loc[rng.choice(n, 15, replace=False), "category"] = df["category"].str.lower()  # "network"
df = pd.concat([df, df.sample(8, random_state=1)], ignore_index=True)   # تكرار

Path("data/raw").mkdir(parents=True, exist_ok=True)
df.to_csv("data/raw/tickets.csv", index=False)
print("Saved:", df.shape)