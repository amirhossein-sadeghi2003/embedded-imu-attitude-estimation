# MPU6050 Raw Reading Test

This test reads raw accelerometer and gyroscope data from the MPU6050 using an ESP32.

## Firmware

The firmware is located at:

firmware/esp32_mpu6050_raw_reading/esp32_mpu6050_raw_reading.ino

The code reads MPU6050 registers directly over I2C without using an external IMU library.

## Serial Output Format

The firmware prints CSV-style data at 115200 baud:

time_ms,accel_x_g,accel_y_g,accel_z_g,gyro_x_dps,gyro_y_dps,gyro_z_dps

## Example Output

29098,0.0349,-0.0120,1.0046,-0.6718,2.0229,-0.6641
29202,0.0391,-0.0083,1.0161,-0.7481,2.0840,-0.4580
29306,0.0369,-0.0112,1.0173,-0.6565,2.0382,-0.4656

## Interpretation

During the first test, the sensor was stationary on the desk.

The accelerometer readings were close to:

- accel_z approximately 1.01 g
- accel_x and accel_y close to 0 g

These values are consistent with a stationary, approximately level sensor dominated by gravity.

The gyroscope readings were close to zero but not exactly zero, exposing the small stationary bias and noise handled later by startup calibration.

Observed in this test:

- the MPU6050 responded to direct register reads
- accelerometer and gyroscope samples were streamed over Serial
- the stationary accelerometer pattern was consistent with gravity along the sensor z-axis
- a small gyroscope bias was visible before calibration
- these measurements provided the input for the later roll/pitch estimation stages
