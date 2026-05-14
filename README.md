# Embedded IMU Attitude Estimation

ESP32-based attitude estimation project using an MPU6050 IMU sensor.

This project estimates board orientation using real accelerometer and gyroscope data. It is designed as a practical bridge between simulation-based state estimation and embedded hardware sensing.

## Portfolio Context

This project is part of an Intelligent Physical Systems portfolio focused on:

- embedded sensing
- real sensor data
- inertial measurement
- filtering and estimation
- hardware-in-the-loop experimentation
- robotics and aerospace-inspired orientation estimation

## Project Goal

The goal is to estimate roll and pitch angles from an MPU6050 IMU connected to an ESP32.

The project will start with raw IMU reading and then progress toward filtered attitude estimation.

## Planned Stages

1. Read raw accelerometer and gyroscope data from MPU6050
2. Compute roll and pitch from accelerometer measurements
3. Study gyroscope drift and accelerometer noise
4. Implement a complementary filter for stable roll/pitch estimation
5. Log serial data for Python analysis
6. Plot raw and filtered attitude estimates
7. Add OLED live display as a hardware output

## Hardware

Initial hardware:

- ESP32 development board
- MPU6050 / GY-521 IMU module
- Breadboard
- Jumper wires
- USB cable

Planned extension:

- OLED display for live roll/pitch visualization

## Wiring

Initial ESP32 to MPU6050 wiring:

| MPU6050 Pin | ESP32 Pin |
|---|---|
| VCC | 3V3 |
| GND | GND |
| SDA | GPIO 21 |
| SCL | GPIO 22 |

## Project Structure

embedded-imu-attitude-estimation/
- firmware/
  - esp32_mpu6050_raw_reading/
- docs/
- data/
  - raw/
- results/
- scripts/
- README.md
- .gitignore


## Hardware Bring-Up

The first hardware bring-up test was completed using an ESP32 I2C scanner.

Result:

MPU6050 detected at I2C address 0x68

This confirms that the soldered MPU6050 module, wiring, and ESP32 I2C communication are working correctly.

See:

[docs/i2c_test.md](docs/i2c_test.md)


## Current Status

Initial hardware bring-up is complete. The ESP32 successfully detected the MPU6050 at I2C address 0x68. The next step is to read raw accelerometer and gyroscope data.
