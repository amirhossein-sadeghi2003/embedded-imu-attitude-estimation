# IMU Serial Logging and Analysis

This stage logs complementary-filter attitude estimates from the ESP32 over Serial and analyzes the recorded data with Python.

## Goal

The goal is to move beyond Serial Monitor inspection and create a repeatable data-analysis workflow:

1. stream IMU attitude data from ESP32
2. log the Serial output to a file
3. clean repeated headers and non-data lines
4. save a clean CSV dataset
5. generate plots for roll, pitch, and corrected gyroscope measurements

## Logging Script

The logging script is located at:

scripts/log_imu_demo.py

It records Serial output from:

/dev/ttyUSB0

The log is saved to:

data/raw/complementary_filter_demo_log.csv

## Demo Scenario

The logged demo includes three motion stages:

- flat on desk
- tilted and held still
- slowly rotated / tilted by hand

## Cleaning Script

The cleaning script is located at:

scripts/clean_imu_log.py

It removes repeated headers and non-numeric lines from the Serial log.

Clean output:

data/raw/complementary_filter_demo_clean.csv

## Plotting Script

The plotting script is located at:

scripts/plot_imu_log.py

It generates:

- results/roll_estimation_comparison.png
- results/pitch_estimation_comparison.png
- results/corrected_gyro_measurements.png
- results/imu_demo_summary.csv

## Summary Results

The recorded demo contained:

- 126 samples
- approximately 38.0 seconds of data
- filtered roll range: about -34.0 to +34.8 degrees
- filtered pitch range: about -90.5 to +71.6 degrees

## Interpretation

This stage confirms that:

- ESP32 Serial attitude data can be logged reproducibly
- raw Serial output can be cleaned into a usable CSV dataset
- complementary-filter roll and pitch estimates can be analyzed with Python
- real IMU motion produces visible roll, pitch, and gyroscope response plots

The current sampling rate is suitable for a basic hardware demo and analysis milestone. A future improvement may increase the sampling rate for smoother attitude plots and better motion analysis.
