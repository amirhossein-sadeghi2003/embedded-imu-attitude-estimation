from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

input_path = Path("data/raw/high_rate_imu_demo_clean.csv")
results_dir = Path("results")
results_dir.mkdir(exist_ok=True)

df = pd.read_csv(input_path)

# Use reconstructed time from the cleaner.
time_s = df["time_s"]

plt.figure(figsize=(10, 5))
plt.plot(time_s, df["accel_roll_deg"], label="Accelerometer roll")
plt.plot(time_s, df["filtered_roll_deg"], label="Filtered roll")
plt.xlabel("Time (s)")
plt.ylabel("Roll angle (deg)")
plt.title("High-Rate Roll Estimation: Accelerometer vs Complementary Filter")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(results_dir / "high_rate_roll_estimation_comparison.png", dpi=200)
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(time_s, df["accel_pitch_deg"], label="Accelerometer pitch")
plt.plot(time_s, df["filtered_pitch_deg"], label="Filtered pitch")
plt.xlabel("Time (s)")
plt.ylabel("Pitch angle (deg)")
plt.title("High-Rate Pitch Estimation: Accelerometer vs Complementary Filter")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(results_dir / "high_rate_pitch_estimation_comparison.png", dpi=200)
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(time_s, df["gyro_x_corrected_dps"], label="Corrected gyro X")
plt.plot(time_s, df["gyro_y_corrected_dps"], label="Corrected gyro Y")
plt.xlabel("Time (s)")
plt.ylabel("Angular velocity (deg/s)")
plt.title("High-Rate Corrected Gyroscope Measurements")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(results_dir / "high_rate_corrected_gyro_measurements.png", dpi=200)
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(time_s, df["accel_x_g"], label="Accel X")
plt.plot(time_s, df["accel_y_g"], label="Accel Y")
plt.plot(time_s, df["accel_z_g"], label="Accel Z")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (g)")
plt.title("High-Rate Accelerometer Measurements")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(results_dir / "high_rate_accelerometer_measurements.png", dpi=200)
plt.close()

summary = pd.DataFrame(
    {
        "metric": [
            "samples",
            "duration_s",
            "mean_dt_s",
            "estimated_sampling_rate_hz",
            "filtered_roll_min_deg",
            "filtered_roll_max_deg",
            "filtered_pitch_min_deg",
            "filtered_pitch_max_deg",
            "accel_z_mean_g",
        ],
        "value": [
            len(df),
            time_s.iloc[-1] - time_s.iloc[0],
            df["dt_s"].mean(),
            1.0 / df["dt_s"].mean(),
            df["filtered_roll_deg"].min(),
            df["filtered_roll_deg"].max(),
            df["filtered_pitch_deg"].min(),
            df["filtered_pitch_deg"].max(),
            df["accel_z_g"].mean(),
        ],
    }
)

summary.to_csv(results_dir / "high_rate_imu_demo_summary.csv", index=False)

print("Saved high-rate plots to results/")
print(summary.to_string(index=False))
