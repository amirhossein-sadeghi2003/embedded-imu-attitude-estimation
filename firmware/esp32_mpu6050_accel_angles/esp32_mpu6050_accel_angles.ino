#include <Wire.h>
#include <math.h>

#define I2C_SDA 21
#define I2C_SCL 22

#define MPU6050_ADDR 0x68
#define MPU6050_PWR_MGMT_1 0x6B
#define MPU6050_ACCEL_XOUT_H 0x3B

int16_t readWord(uint8_t registerAddress) {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(registerAddress);
  Wire.endTransmission(false);

  Wire.requestFrom(MPU6050_ADDR, 2, true);

  int16_t highByte = Wire.read();
  int16_t lowByte = Wire.read();

  return (highByte << 8) | lowByte;
}

void wakeUpMPU6050() {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(MPU6050_PWR_MGMT_1);
  Wire.write(0x00);
  Wire.endTransmission(true);
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println();
  Serial.println("ESP32 MPU6050 Accelerometer Roll/Pitch");
  Serial.println("--------------------------------------");

  Wire.begin(I2C_SDA, I2C_SCL);
  wakeUpMPU6050();

  delay(100);

  Serial.println("time_ms,accel_x_g,accel_y_g,accel_z_g,roll_deg,pitch_deg");
}

void loop() {
  int16_t rawAccelX = readWord(MPU6050_ACCEL_XOUT_H);
  int16_t rawAccelY = readWord(MPU6050_ACCEL_XOUT_H + 2);
  int16_t rawAccelZ = readWord(MPU6050_ACCEL_XOUT_H + 4);

  float accelX = rawAccelX / 16384.0;
  float accelY = rawAccelY / 16384.0;
  float accelZ = rawAccelZ / 16384.0;

  float rollRad = atan2(accelY, accelZ);
  float pitchRad = atan2(-accelX, sqrt(accelY * accelY + accelZ * accelZ));

  float rollDeg = rollRad * 180.0 / PI;
  float pitchDeg = pitchRad * 180.0 / PI;

  Serial.print(millis());
  Serial.print(",");
  Serial.print(accelX, 4);
  Serial.print(",");
  Serial.print(accelY, 4);
  Serial.print(",");
  Serial.print(accelZ, 4);
  Serial.print(",");
  Serial.print(rollDeg, 2);
  Serial.print(",");
  Serial.println(pitchDeg, 2);

  delay(100);
}