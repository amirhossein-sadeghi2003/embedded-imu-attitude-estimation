# Complementary Filter with Gyro Calibration

This stage combines accelerometer-based attitude estimates with gyroscope measurements using a complementary filter.

## Firmware

The firmware is located at:

firmware/esp32_mpu6050_complementary_filter/esp32_mpu6050_complementary_filter.ino

## Why a Complementary Filter?

The accelerometer provides a long-term reference to gravity, which is useful for estimating roll and pitch. However, accelerometer readings can be noisy during motion.

The gyroscope measures angular velocity and is useful for short-term motion tracking. However, gyroscope integration can drift over time because of bias.

A complementary filter combines both:

- gyroscope integration for short-term smooth motion
- accelerometer angle estimates for long-term correction

## Gyroscope Calibration

During the first test, the complementary filter showed drift because the gyroscope output was not exactly zero while the sensor was stationary.

To fix this, the firmware performs startup calibration:

1. Keep the sensor still.
2. Collect 300 gyroscope samples.
3. Compute average gyro X and gyro Y bias.
4. Subtract this bias from future gyro readings.

This reduced the corrected gyroscope values close to zero during stationary tests.

## Filter Equation

For roll:

filtered_roll = alpha * (previous_filtered_roll + gyro_x * dt) + (1 - alpha) * accel_roll

For pitch:

filtered_pitch = alpha * (previous_filtered_pitch + gyro_y * dt) + (1 - alpha) * accel_pitch

The current filter coefficient is:

alpha = 0.98

## Stationary Test

After gyro calibration, the flat-on-desk output was stable.

Typical values:

- accel_roll: about -0.1 to -0.6 degrees
- accel_pitch: about -1.4 to -2.1 degrees
- filtered_roll: close to 0 degrees
- filtered_pitch: about -1.9 to -2.1 degrees
- corrected gyro values: close to 0 deg/s

This confirms that gyro bias correction improved stability.

## Tilted Test

When the board was tilted and held still:

- accel_pitch reached about -50 to -53 degrees
- filtered_pitch followed the tilted orientation at about -55 to -60 degrees
- corrected gyro values returned close to zero after motion stopped

One final sample showed a large gyro_y value during movement, which is expected and indicates the board was being moved at that moment.

## Interpretation

This stage confirms that:

- raw accelerometer and gyroscope readings can be combined
- gyroscope bias must be handled for stable attitude estimation
- startup calibration improves complementary filter behavior
- the filter can track real physical board orientation changes
- the project is ready for serial logging and Python-based analysis
