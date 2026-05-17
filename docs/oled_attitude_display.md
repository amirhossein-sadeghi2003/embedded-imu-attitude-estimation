# OLED Live Attitude Display

This stage adds a live OLED output to the ESP32 + MPU6050 attitude estimation project.

Instead of only streaming values to the Serial Monitor or logging data for Python analysis, the ESP32 now displays the filtered roll and pitch estimates directly on a small OLED screen.

## Goal

The goal is to make the embedded attitude estimator visible as a standalone hardware demo:

1. read accelerometer and gyroscope data from the MPU6050
2. calibrate gyroscope bias at startup
3. estimate roll and pitch using a complementary filter
4. refresh the OLED display with live attitude values
5. keep Serial output available for debugging

## Hardware

Additional hardware:

- 0.96 inch I2C OLED display, SSD1306-compatible
- ESP32 development board
- MPU6050 / GY-521 IMU module

## I2C Wiring

The OLED and MPU6050 share the same ESP32 I2C bus.

| Device | Pin | ESP32 Pin |
|---|---|---|
| OLED | VCC | 3V3 |
| OLED | GND | GND |
| OLED | SDA | GPIO 21 |
| OLED | SCL | GPIO 22 |
| MPU6050 | VCC | 3V3 |
| MPU6050 | GND | GND |
| MPU6050 | SDA | GPIO 21 |
| MPU6050 | SCL | GPIO 22 |

## I2C Scan Result

With both devices connected, the ESP32 I2C scanner detected:

- OLED display at address `0x3C`
- MPU6050 at address `0x68`

This confirms that both devices can operate on the same I2C bus.

## Firmware

The OLED display firmware is located at:

`firmware/esp32_mpu6050_oled_attitude_display/esp32_mpu6050_oled_attitude_display.ino`

The firmware uses:

- `Wire.h` for I2C communication
- `Adafruit_GFX.h`
- `Adafruit_SSD1306.h`

## Display Output

The OLED shows:

- `R`: filtered roll angle in degrees
- `P`: filtered pitch angle in degrees

Example flat-on-desk reading:

| Quantity | Value |
|---|---:|
| Roll | -0.1° |
| Pitch | -1.8° |

Small offsets around zero are expected because of sensor bias, breadboard alignment, and the physical surface not being perfectly level.

## Timing

The firmware uses:

- complementary-filter update rate: approximately 50 Hz
- OLED refresh rate: approximately 10 Hz

This keeps the estimator responsive while avoiding unnecessary OLED flicker.

## Interpretation

This stage turns the project from a Serial-only data collection system into a visible embedded hardware demo.

It demonstrates:

- shared I2C operation with multiple devices
- real-time roll/pitch estimation on ESP32
- OLED-based embedded feedback
- practical system integration beyond offline Python plots

The next possible improvement is to capture a short hardware demo video showing the OLED values changing as the IMU is tilted.
