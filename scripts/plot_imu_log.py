from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

input_path = Path("data/raw/complementary_filter_demo_clean.csv")
results_dir = Path("results")
results_dir.mkdir(exist_ok=True)

df = pd.read_csv(input_path)

df["time_s"] = (df["time_ms"] - df["time_ms"].iloc[0]) / 1000.0

plt.figure(figsize=(10, 5))
plt.plot(df["time_s"], df["accel_roll_deg"], label="Accelerometer roll")
plt.plot(df["time_s"], df["filtered_roll_deg"], label="Filtered roll")
plt.xlabel("Time (s)")
plt.ylabel("Roll angle (deg)")
plt.title("Roll Estimation: Accelerometer vs Complementary Filter")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(results_dir / "roll_estimation_comparison.png", dpi=200)
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(df["time_s"], df["accel_pitch_deg"], label="Accelerometer pitch")
plt.plot(df["time_s"], df["filtered_pitch_deg"], label="Filtered pitch")
plt.xlabel("Time (s)")
plt.ylabel("Pitch angle (deg)")
plt.title("Pitch Estimation: Accelerometer vs Complementary Filter")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(results_dir / "pitch_estimation_comparison.png", dpi=200)
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(df["time_s"], df["gyro_x_corrected_dps"], label="Corrected gyro X")
plt.plot(df["time_s"], df["gyro_y_corrected_dps"], label="Corrected gyro Y")
plt.xlabel("Time (s)")
plt.ylabel("Angular velocity (deg/s)")
plt.title("Corrected Gyroscope Measurements")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(results_dir / "corrected_gyro_measurements.png", dpi=200)
plt.close()

summary = pd.DataFrame(
    {
        "metric": [
            "samples",
            "duration_s",
            "filtered_roll_min_deg",
            "filtered_roll_max_deg",
            "filtered_pitch_min_deg",
            "filtered_pitch_max_deg",
        ],
        "value": [
            len(df),
            df["time_s"].iloc[-1] - df["time_s"].iloc[0],
            df["filtered_roll_deg"].min(),
            df["filtered_roll_deg"].max(),
            df["filtered_pitch_deg"].min(),
            df["filtered_pitch_deg"].max(),
        ],
    }
)

summary.to_csv(results_dir / "imu_demo_summary.csv", index=False)

print("Saved plots to results/")
print(summary.to_string(index=False))
