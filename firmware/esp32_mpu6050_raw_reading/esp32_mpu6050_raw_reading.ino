#include <Wire.h>

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
  Serial.println("ESP32 MPU6050 Raw Reading");
  Serial.println("-------------------------");

  Wire.begin(I2C_SDA, I2C_SCL);
  wakeUpMPU6050();

  delay(100);

  Serial.println("time_ms,accel_x_g,accel_y_g,accel_z_g,gyro_x_dps,gyro_y_dps,gyro_z_dps");
}

void loop() {
  int16_t rawAccelX = readWord(MPU6050_ACCEL_XOUT_H);
  int16_t rawAccelY = readWord(MPU6050_ACCEL_XOUT_H + 2);
  int16_t rawAccelZ = readWord(MPU6050_ACCEL_XOUT_H + 4);

  int16_t rawGyroX = readWord(MPU6050_ACCEL_XOUT_H + 8);
  int16_t rawGyroY = readWord(MPU6050_ACCEL_XOUT_H + 10);
  int16_t rawGyroZ = readWord(MPU6050_ACCEL_XOUT_H + 12);

  float accelX = rawAccelX / 16384.0;
  float accelY = rawAccelY / 16384.0;
  float accelZ = rawAccelZ / 16384.0;

  float gyroX = rawGyroX / 131.0;
  float gyroY = rawGyroY / 131.0;
  float gyroZ = rawGyroZ / 131.0;

  Serial.print(millis());
  Serial.print(",");
  Serial.print(accelX, 4);
  Serial.print(",");
  Serial.print(accelY, 4);
  Serial.print(",");
  Serial.print(accelZ, 4);
  Serial.print(",");
  Serial.print(gyroX, 4);
  Serial.print(",");
  Serial.print(gyroY, 4);
  Serial.print(",");
  Serial.println(gyroZ, 4);

  delay(100);
}