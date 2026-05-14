# MPU6050 Wiring Notes

This document describes the initial wiring for connecting an MPU6050 / GY-521 IMU module to an ESP32.

## Initial Wiring

| MPU6050 Pin | ESP32 Pin | Notes |
|---|---|---|
| VCC | 3V3 | Use 3.3V for ESP32-safe I2C logic |
| GND | GND | Common ground |
| SDA | GPIO 21 | ESP32 default I2C SDA |
| SCL | GPIO 22 | ESP32 default I2C SCL |

## Important Notes

- Do not connect MPU6050 VCC to the external 5V servo power rail for this project stage.
- Use ESP32 3V3 for the MPU6050 module.
- Keep wiring short for stable I2C communication.
- If the I2C scan fails, check SDA/SCL orientation and ground connection first.

## Unused Pins for Initial Test

The following pins are not required for the first raw-reading test:

- XDA
- XCL
- AD0
- INT

They may be used later for advanced configurations, address selection, or interrupt-based reading.
