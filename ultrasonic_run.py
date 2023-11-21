import subprocess



while True:
    process = subprocess.Popen(["C:\\Projects\\embedded-final\\run.bat"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout = process.stdout.readline().decode().strip()

    print(stdout)