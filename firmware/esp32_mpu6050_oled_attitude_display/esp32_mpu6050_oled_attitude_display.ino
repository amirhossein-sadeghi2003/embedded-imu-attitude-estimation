#include <Wire.h>
#include <math.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define I2C_SDA 21
#define I2C_SCL 22

#define MPU6050_ADDR 0x68
#define OLED_ADDR 0x3C

#define MPU6050_PWR_MGMT_1 0x6B
#define MPU6050_ACCEL_XOUT_H 0x3B

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

float filteredRoll = 0.0;
float filteredPitch = 0.0;

float gyroXBias = 0.0;
float gyroYBias = 0.0;

unsigned long previousUpdateMicros = 0;
unsigned long previousDisplayMillis = 0;

const float alpha = 0.98;
const unsigned long updateIntervalMicros = 20000;  // 50 Hz filter update
const unsigned long displayIntervalMillis = 100;   // 10 Hz OLED refresh

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

void showMessage(const char *line1, const char *line2) {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);

  display.setCursor(0, 16);
  display.println(line1);

  display.setCursor(0, 32);
  display.println(line2);

  display.display();
}

void calibrateGyro() {
  const int samples = 500;
  float sumGyroX = 0.0;
  float sumGyroY = 0.0;

  Serial.println("Calibrating gyro. Keep sensor still.");
  showMessage("Calibrating gyro", "Keep sensor still");

  for (int i = 0; i < samples; i++) {
    float gyroX, gyroY;
    readGyro(gyroX, gyroY);

    sumGyroX += gyroX;
    sumGyroY += gyroY;

    delay(5);
  }

  gyroXBias = sumGyroX / samples;
  gyroYBias = sumGyroY / samples;

  Serial.println("Gyro calibration complete.");
  Serial.print("gyro_x_bias_dps=");
  Serial.println(gyroXBias, 6);
  Serial.print("gyro_y_bias_dps=");
  Serial.println(gyroYBias, 6);

  showMessage("Calibration done", "Starting display...");
  delay(800);
}

void initializeFilterFromAccelerometer() {
  float accelX, accelY, accelZ;
  readAccel(accelX, accelY, accelZ);

  filteredRoll = computeAccelRoll(accelX, accelY, accelZ);
  filteredPitch = computeAccelPitch(accelX, accelY, accelZ);
}

void updateOLED(float rollDeg, float pitchDeg) {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);

  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("IMU Attitude Estimation");

  display.drawLine(0, 11, 127, 11, SSD1306_WHITE);

  display.setTextSize(2);
  display.setCursor(0, 18);
  display.print("R:");
  display.print(rollDeg, 1);

  display.setCursor(0, 42);
  display.print("P:");
  display.print(pitchDeg, 1);

  display.setTextSize(1);
  display.setCursor(86, 22);
  display.print("deg");

  display.setCursor(86, 46);
  display.print("deg");

  display.display();
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Wire.begin(I2C_SDA, I2C_SCL);

  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("OLED initialization failed.");
    while (true) {
      delay(1000);
    }
  }

  showMessage("OLED OK", "Starting IMU...");

  wakeUpMPU6050();
  delay(100);

  calibrateGyro();
  initializeFilterFromAccelerometer();

  previousUpdateMicros = micros();
  previousDisplayMillis = millis();

  Serial.println("time_ms,filtered_roll_deg,filtered_pitch_deg");
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

  unsigned long currentMillis = millis();

  if (currentMillis - previousDisplayMillis >= displayIntervalMillis) {
    previousDisplayMillis = currentMillis;

    updateOLED(filteredRoll, filteredPitch);

    Serial.print(currentMillis);
    Serial.print(",");
    Serial.print(filteredRoll, 2);
    Serial.print(",");
    Serial.println(filteredPitch, 2);
  }
}