# I2C Scanner Test

The first hardware test verifies that the ESP32 can detect the MPU6050 module over the I2C bus.

## Wiring Used

| MPU6050 Pin | ESP32 Pin |
|---|---|
| VCC | 3V3 |
| GND | GND |
| SDA | GPIO 21 |
| SCL | GPIO 22 |

## Test Firmware

The scanner firmware is located at:

firmware/esp32_i2c_scanner/esp32_i2c_scanner.ino

The firmware scans all I2C addresses and reports detected devices over the Serial Monitor.

## Serial Monitor Settings

| Setting | Value |
|---|---|
| Baud rate | 115200 |
| Board | ESP32 Dev Module |

## Result

The MPU6050 was successfully detected at:

0x68

Example Serial Monitor output:

ESP32 I2C Scanner
----------------
Scanning I2C bus...
I2C device found at address 0x68
Devices found: 1

## Interpretation

This confirms that:

- the MPU6050 soldered header is usable
- VCC and GND are connected correctly
- SDA and SCL are connected correctly
- ESP32 I2C communication is working
- the IMU is ready for raw accelerometer and gyroscope reading
