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

This confirms that the accelerometer-based attitude estimate responds correctly to physical orientation changes.

## Interpretation

This test confirms that:

- accelerometer data can be converted into roll and pitch estimates
- the sensor responds correctly to board orientation
- small nonzero angles at rest are expected because of mounting offset and sensor bias
- the project is ready for gyroscope integration and complementary filtering
