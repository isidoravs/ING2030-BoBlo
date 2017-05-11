import serial

arduino = serial.Serial('COM4', 38400, timeout=1.0)
weight = 0
print("0 gr.")

while True:
    line = arduino.readline()  # bytes
    read_weight = line.decode('utf-8').strip()
    if read_weight == "1" or read_weight == "-0":
        read_weight = "0"

    if read_weight != "":
        if int(read_weight) != weight:
            weight = int(read_weight)
            print(read_weight, " gr.")

arduino.close()