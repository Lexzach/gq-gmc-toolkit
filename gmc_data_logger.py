import csv
import time
import serial

def read_2byte_value(ser):
    byte1 = ser.read(1)
    byte2 = ser.read(1)
    combined = int.from_bytes(byte1 + byte2, byteorder='big')
    return combined

# Open serial port
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)
ser.write(b"<REBOOT>>")

# Open/Create CSV file
timestamp_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
csvfile = open(f'cpm_log_{timestamp_str}.csv', 'w', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['TIME', 'CPM'])

print("Please wait 60 seconds for CPM to stabalize")
time.sleep(61) # 61 seconds to allow geiger counter to boot 

try:
    while True:
        ser.write(b"<GETCPM>>")

        count = read_2byte_value(ser)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        csvwriter.writerow([timestamp, count])
        print(f'{timestamp}: {count}')
        time.sleep(10)

except KeyboardInterrupt:
    csvfile.close()
    ser.close()
