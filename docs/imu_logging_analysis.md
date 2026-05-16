# IMU Serial Logging and Analysis

This stage logs complementary-filter attitude estimates from the ESP32 over Serial and analyzes the recorded data with Python.

The project now includes two logging stages:

1. an initial human-readable Serial logging demo
2. a higher-rate CSV logging workflow for cleaner engineering analysis

## Goal

The goal is to move beyond Serial Monitor inspection and create a repeatable data-analysis workflow:

1. stream IMU attitude data from ESP32
2. log the Serial output to a file
3. clean malformed or non-data lines
4. save a clean CSV dataset
5. generate plots for roll, pitch, accelerometer measurements, and corrected gyroscope measurements

## Initial Serial Logging Demo

The initial logging script is located at:

`scripts/log_imu_demo.py`

It records Serial output from:

`/dev/ttyUSB0`

The initial log is saved to:

`data/raw/complementary_filter_demo_log.csv`

Clean output:

`data/raw/complementary_filter_demo_clean.csv`

The plotting script is:

`scripts/plot_imu_log.py`

It generates:

- `results/roll_estimation_comparison.png`
- `results/pitch_estimation_comparison.png`
- `results/corrected_gyro_measurements.png`
- `results/imu_demo_summary.csv`

## Initial Demo Scenario

The initial logged demo included three motion stages:

- flat on desk
- tilted and held still
- slowly rotated / tilted by hand

## Initial Demo Results

The initial recorded demo contained:

- 126 samples
- approximately 38.0 seconds of data
- filtered roll range: about -34.0 to +34.8 degrees
- filtered pitch range: about -90.5 to +71.6 degrees

This was sufficient for a first hardware-analysis milestone, but the output rate was intentionally slow for human readability.

## High-Rate Logging Firmware

A separate high-rate firmware was added for cleaner CSV-style logging:

`firmware/esp32_mpu6050_high_rate_logger/esp32_mpu6050_high_rate_logger.ino`

This firmware outputs:

- reconstructed timestamp information
- accelerometer x/y/z values in g
- accelerometer-only roll and pitch
- complementary-filter roll and pitch
- corrected gyroscope x/y values in deg/s

The target logging rate is approximately 50 Hz.

## High-Rate Data Files

Raw high-rate log:

`data/raw/high_rate_imu_demo_log.csv`

Cleaned high-rate dataset:

`data/raw/high_rate_imu_demo_clean.csv`

Cleaning script:

`scripts/clean_high_rate_imu_log.py`

Plotting script:

`scripts/plot_high_rate_imu_log.py`

Generated results:

- `results/high_rate_roll_estimation_comparison.png`
- `results/high_rate_pitch_estimation_comparison.png`
- `results/high_rate_corrected_gyro_measurements.png`
- `results/high_rate_accelerometer_measurements.png`
- `results/high_rate_imu_demo_summary.csv`

## High-Rate Demo Results

The high-rate demo contains:

| Metric | Value |
|---|---:|
| Samples | 1909 |
| Duration | 38.16 s |
| Mean timestep | 0.020 s |
| Estimated sampling rate | 50.0 Hz |
| Filtered roll range | -43.1° to +48.8° |
| Filtered pitch range | -67.1° to +64.1° |
| Mean accel-z | 0.851 g |

## Cleaning Notes

During high-rate logging, one malformed Serial line was detected and skipped.

The cleaner reconstructs `time_s` from `dt_s` instead of relying only on raw ESP32 `millis()` timestamps. This makes the cleaned dataset more robust to Serial startup artifacts or partial lines.

## Interpretation

This stage confirms that:

- ESP32 Serial attitude data can be logged reproducibly
- raw Serial output can be cleaned into usable CSV datasets
- complementary-filter roll and pitch estimates can be analyzed with Python
- high-rate logging provides smoother and denser motion data than the initial human-readable Serial demo
- the project now includes a complete embedded-data workflow from firmware to dataset to plots

The next hardware-facing improvement is to add an OLED display for live roll/pitch visualization.
