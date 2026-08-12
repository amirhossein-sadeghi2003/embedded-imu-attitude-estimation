from pathlib import Path
import csv

raw_path = Path("data/raw/high_rate_imu_demo_log.csv")
clean_path = Path("data/raw/high_rate_imu_demo_clean.csv")

header = [
    "sample_index",
    "time_s",
    "raw_time_ms",
    "dt_s",
    "accel_x_g",
    "accel_y_g",
    "accel_z_g",
    "accel_roll_deg",
    "accel_pitch_deg",
    "filtered_roll_deg",
    "filtered_pitch_deg",
    "gyro_x_corrected_dps",
    "gyro_y_corrected_dps",
]

raw_header = [
    "time_ms",
    "dt_s",
    "accel_x_g",
    "accel_y_g",
    "accel_z_g",
    "accel_roll_deg",
    "accel_pitch_deg",
    "filtered_roll_deg",
    "filtered_pitch_deg",
    "gyro_x_corrected_dps",
    "gyro_y_corrected_dps",
]

rows = []
skipped_malformed = 0
skipped_bad_dt = 0

with raw_path.open("r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if line.startswith("time_ms"):
            continue

        parts = line.split(",")

        if len(parts) != len(raw_header):
            skipped_malformed += 1
            continue

        try:
            values = [float(p) for p in parts]
        except ValueError:
            skipped_malformed += 1
            continue

        dt_s = values[1]

        # For the 50 Hz logger, dt should be around 0.02 s.
        # Keep a wide range to avoid rejecting real samples unnecessarily.
        if not (0.005 <= dt_s <= 0.1):
            skipped_bad_dt += 1
            continue

        rows.append(values)

# Drop a stray startup row if it is far from the main timestamp sequence.
if len(rows) >= 2 and rows[1][0] - rows[0][0] > 1000:
    rows = rows[1:]

# Remove isolated corrupted timestamps while preserving real capture gaps.
validated_rows = []
for i, values in enumerate(rows):
    if 0 < i < len(rows) - 1:
        previous_time = rows[i - 1][0]
        current_time = values[0]
        next_time = rows[i + 1][0]

        if previous_time < next_time and not (
            previous_time < current_time < next_time
        ):
            continue

    validated_rows.append(values)

rows = validated_rows

clean_rows = []
start_time_ms = rows[0][0]

for idx, values in enumerate(rows):
    raw_time_ms = values[0]
    dt_s = values[1]
    time_s = (raw_time_ms - start_time_ms) / 1000.0

    clean_rows.append(
        [
            idx,
            time_s,
            raw_time_ms,
            dt_s,
            *values[2:],
        ]
    )

clean_path.parent.mkdir(parents=True, exist_ok=True)

with clean_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(clean_rows)

print(f"Saved clean CSV: {clean_path}")
print(f"Rows: {len(clean_rows)}")
print(f"Skipped malformed rows: {skipped_malformed}")
print(f"Skipped bad-dt rows: {skipped_bad_dt}")

if clean_rows:
    duration_s = clean_rows[-1][1] - clean_rows[0][1]
    mean_dt = sum(row[3] for row in clean_rows) / len(clean_rows)
    estimated_rate_hz = 1.0 / mean_dt if mean_dt > 0 else 0.0

    print(f"Duration from raw timestamps: {duration_s:.3f} s")
    print(f"Mean reported dt: {mean_dt:.6f} s")
    print(f"Nominal update rate from reported dt: {estimated_rate_hz:.2f} Hz")
