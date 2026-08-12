import argparse
import time
from pathlib import Path

import serial

parser = argparse.ArgumentParser(description="Capture the complementary-filter IMU demo.")
parser.add_argument("--port", default="/dev/ttyUSB0", help="Serial port for the ESP32")
args = parser.parse_args()

BAUD = 115200
OUT = Path("data/raw/complementary_filter_demo_log.csv")

OUT.parent.mkdir(parents=True, exist_ok=True)

def run_stage(name, seconds):
    print(f"\n{name}")
    print(f"Duration: {seconds} seconds")
    start = time.time()
    while time.time() - start < seconds:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        if line:
            f.write(line + "\n")
            f.flush()

print("Opening serial port...")
print("Close Arduino Serial Monitor before running this script.")

with serial.Serial(args.port, BAUD, timeout=1) as ser, OUT.open("w", encoding="utf-8") as f:
    time.sleep(2)
    ser.reset_input_buffer()

    print("\nKeep the sensor still. Waiting for calibration / settle...")
    run_stage("Calibration / settle: keep sensor still", 8)

    run_stage("Stage 1/3: FLAT on desk", 10)
    run_stage("Stage 2/3: TILT and HOLD", 10)
    run_stage("Stage 3/3: SLOWLY ROTATE / TILT", 10)

print(f"\nDone. Saved log to: {OUT}")
