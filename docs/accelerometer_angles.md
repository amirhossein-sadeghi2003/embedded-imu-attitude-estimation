# Accelerometer-Based Roll and Pitch Estimation

This test computes roll and pitch angles from MPU6050 accelerometer measurements using an ESP32.

## Firmware

The firmware is located at:

firmware/esp32_mpu6050_accel_angles/esp32_mpu6050_accel_angles.ino

The code reads accelerometer data directly from MPU6050 registers over I2C and computes roll and pitch from the gravity vector.

## Equations

Roll:

roll = atan2(accel_y, accel_z)

Pitch:

pitch = atan2(-accel_x, sqrt(accel_y^2 + accel_z^2))

The angles are converted from radians to degrees before being printed over Serial.

## Serial Output Format

The firmware prints CSV-style data at 115200 baud:

time_ms,accel_x_g,accel_y_g,accel_z_g,roll_deg,pitch_deg

## Flat Sensor Output

When the board was approximately flat on the desk, the readings were close to:

- roll: about -0.2 to -0.6 degrees
- pitch: about -1.5 to -2.1 degrees
- accel_z: about 1.01 g

This is reasonable because the sensor, breadboard, and desk are not perfectly aligned and the accelerometer has small offsets.

## Tilted Sensor Output

When the board was tilted by hand, the estimated angles changed clearly:

- roll reached about +44 degrees in one direction
- roll reached about -44 degrees in the opposite direction
- pitch also changed during forward/backward motion

The accelerometer-based attitude estimate changed consistently with manual board tilting.

## Interpretation

Observed in this test:

- accelerometer data was converted into roll and pitch estimates
- the estimated angles responded consistently to manual board tilting
- small nonzero angles at rest were consistent with mounting offset and sensor bias
- these accelerometer angles were used as the long-term reference in the later complementary-filter stage
