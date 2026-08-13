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

The firmware performs startup calibration:

1. Keep the sensor still.
2. Collect 300 gyroscope samples.
3. Compute average gyro X and gyro Y bias.
4. Subtract this bias from future gyro readings.

After startup bias subtraction, the corrected gyroscope values stayed closer to zero during stationary tests.

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

## Tilted Test

When the board was tilted and held still:

- accel_pitch reached about -50 to -53 degrees
- filtered_pitch reached about -55 to -60 degrees
- corrected gyro values returned close to zero after motion stopped

One final sample showed a large gyro_y value during movement, consistent with the board being moved at that moment.

## Interpretation

Observed in this stage:

- accelerometer and gyroscope measurements were combined in the roll/pitch estimator
- startup bias subtraction reduced the stationary gyroscope offset seen in the earlier raw-reading stage
- the filtered estimates responded consistently during the recorded manual tilt tests
- the same estimator output was used by the Serial logging and Python analysis stages
