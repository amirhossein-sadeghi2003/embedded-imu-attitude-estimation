#include <Wire.h>
#include <math.h>

#define I2C_SDA 21
#define I2C_SCL 22

#define MPU6050_ADDR 0x68
#define MPU6050_PWR_MGMT_1 0x6B
#define MPU6050_ACCEL_XOUT_H 0x3B

float filteredRoll = 0.0;
float filteredPitch = 0.0;

float gyroXBias = 0.0;
float gyroYBias = 0.0;

unsigned long previousUpdateMicros = 0;
unsigned long previousPrintMicros = 0;

const float alpha = 0.98;

// 50 Hz logging rate = one CSV row every 20 ms
const unsigned long logIntervalMicros = 20000;

// Optional internal update limiter.
// Keeping this equal to the log interval makes the filter and output both run at 50 Hz.
const unsigned long updateIntervalMicros = 20000;

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

void readAccel(float &accelX, float &accelY, float &accelZ) {
  int16_t rawAccelX = readWord(MPU6050_ACCEL_XOUT_H);
  int16_t rawAccelY = readWord(MPU6050_ACCEL_XOUT_H + 2);
  int16_t rawAccelZ = readWord(MPU6050_ACCEL_XOUT_H + 4);

  accelX = rawAccelX / 16384.0;
  accelY = rawAccelY / 16384.0;
  accelZ = rawAccelZ / 16384.0;
}

void readGyro(float &gyroX, float &gyroY) {
  int16_t rawGyroX = readWord(MPU6050_ACCEL_XOUT_H + 8);
  int16_t rawGyroY = readWord(MPU6050_ACCEL_XOUT_H + 10);

  gyroX = rawGyroX / 131.0;
  gyroY = rawGyroY / 131.0;
}

float computeAccelRoll(float accelX, float accelY, float accelZ) {
  return atan2(accelY, accelZ) * 180.0 / PI;
}

float computeAccelPitch(float accelX, float accelY, float accelZ) {
  return atan2(-accelX, sqrt(accelY * accelY + accelZ * accelZ)) * 180.0 / PI;
}

void calibrateGyro() {
  const int samples = 500;
  float sumGyroX = 0.0;
  float sumGyroY = 0.0;

  Serial.println("# Calibrating gyro. Keep the sensor still.");

  for (int i = 0; i < samples; i++) {
    float gyroX, gyroY;
    readGyro(gyroX, gyroY);

    sumGyroX += gyroX;
    sumGyroY += gyroY;

    delay(5);
  }

  gyroXBias = sumGyroX / samples;
  gyroYBias = sumGyroY / samples;

  Serial.print("# gyro_x_bias_dps=");
  Serial.println(gyroXBias, 6);

  Serial.print("# gyro_y_bias_dps=");
  Serial.println(gyroYBias, 6);

  Serial.println("# Calibration complete.");
}

void initializeFilterFromAccelerometer() {
  float accelX, accelY, accelZ;
  readAccel(accelX, accelY, accelZ);

  filteredRoll = computeAccelRoll(accelX, accelY, accelZ);
  filteredPitch = computeAccelPitch(accelX, accelY, accelZ);
}

void printCsvHeader() {
  Serial.println("time_ms,dt_s,accel_x_g,accel_y_g,accel_z_g,accel_roll_deg,accel_pitch_deg,filtered_roll_deg,filtered_pitch_deg,gyro_x_corrected_dps,gyro_y_corrected_dps");
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Wire.begin(I2C_SDA, I2C_SCL);
  wakeUpMPU6050();

  delay(100);

  Serial.println("# ESP32 MPU6050 High-Rate Complementary Filter Logger");
  Serial.println("# Target output rate: 50 Hz");
  Serial.println("# Lines beginning with # are metadata/comments.");

  calibrateGyro();
  initializeFilterFromAccelerometer();

  previousUpdateMicros = micros();
  previousPrintMicros = micros();

  printCsvHeader();
}

void loop() {
  unsigned long currentMicros = micros();

  if (currentMicros - previousUpdateMicros < updateIntervalMicros) {
    return;
  }

  float dt = (currentMicros - previousUpdateMicros) / 1000000.0;
  previousUpdateMicros = currentMicros;

  float accelX, accelY, accelZ;
  float gyroX, gyroY;

  readAccel(accelX, accelY, accelZ);
  readGyro(gyroX, gyroY);

  gyroX -= gyroXBias;
  gyroY -= gyroYBias;

  float accelRoll = computeAccelRoll(accelX, accelY, accelZ);
  float accelPitch = computeAccelPitch(accelX, accelY, accelZ);

  filteredRoll = alpha * (filteredRoll + gyroX * dt) + (1.0 - alpha) * accelRoll;
  filteredPitch = alpha * (filteredPitch + gyroY * dt) + (1.0 - alpha) * accelPitch;

  if (currentMicros - previousPrintMicros >= logIntervalMicros) {
    previousPrintMicros = currentMicros;

    Serial.print(millis());
    Serial.print(",");
    Serial.print(dt, 6);
    Serial.print(",");
    Serial.print(accelX, 5);
    Serial.print(",");
    Serial.print(accelY, 5);
    Serial.print(",");
    Serial.print(accelZ, 5);
    Serial.print(",");
    Serial.print(accelRoll, 3);
    Serial.print(",");
    Serial.print(accelPitch, 3);
    Serial.print(",");
    Serial.print(filteredRoll, 3);
    Serial.print(",");
    Serial.print(filteredPitch, 3);
    Serial.print(",");
    Serial.print(gyroX, 4);
    Serial.print(",");
    Serial.println(gyroY, 4);
  }
}