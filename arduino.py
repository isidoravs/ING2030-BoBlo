import serial

arduino = serial.Serial('COM4', 38400, timeout=1.0)

while True:
    line = arduino.readline()  # bytes
    weight = line.decode('utf-8').strip()
    if weight == "1" or weight == "-0":
        weight = "0"

    if weight != "":
        print(weight, "gr.")

arduino.close()
