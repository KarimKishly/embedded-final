import subprocess
import threading


def read_sensor() -> float:
    process = subprocess.Popen(["C:\\Projects\\embedded-final\\ultrasonic\\run_sensor.bat"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    data = process.stdout.read().decode().strip()
    return float(data)

if __name__ == '__main__':
    print(read_sensor())
