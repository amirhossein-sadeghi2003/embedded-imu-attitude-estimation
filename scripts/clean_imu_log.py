from pathlib import Path
import csv

raw_path = Path("data/raw/complementary_filter_demo_log.csv")
clean_path = Path("data/raw/complementary_filter_demo_clean.csv")

header = [
    "time_ms",
    "accel_roll_deg",
    "accel_pitch_deg",
    "filtered_roll_deg",
    "filtered_pitch_deg",
    "gyro_x_corrected_dps",
    "gyro_y_corrected_dps",
]

rows = []

with raw_path.open("r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line.startswith("time_ms"):
            continue

        parts = line.split(",")
        if len(parts) != 7:
            continue

        try:
            values = [float(p) for p in parts]
        except ValueError:
            continue

        rows.append(values)

clean_path.parent.mkdir(parents=True, exist_ok=True)

with clean_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Saved clean CSV: {clean_path}")
print(f"Rows: {len(rows)}")
