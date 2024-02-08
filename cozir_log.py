# Test UART data exchange with COZIR BLINK, read a CO2 measurement and print ppm

# UART configuration according to: https://www.gassensing.co.uk/wp-content/uploads/2023/05/CozIR-Blink-DataSheet-Rev-4.25_3.pdf, p. 29
# AT commands according to: https://www.gassensing.co.uk/wp-content/uploads/2023/05/CozIR-Blink-DataSheet-Rev-4.25_3.pdf, p. 30

# Import libraries
from machine import UART, Pin
import utime
import ubinascii

# Anschluss und 3.3V-Bezug durch COZIR an GP15 (Position 20, unten links)
COZIR = machine.Pin(15, machine.Pin.OUT)

# UART configuration
# UART 0 [Pico W], TX=GP0 (Pin 1), RX=GP1 (Pin 2)
# UART 1 [Cozir Blink], TX= Pin 11, RX= Pin 12
uart = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1)

# Return firmware version and sensor serial number from COZIR -> AT commend to COZIR: "Y"
uart.write('Y\r\n')
firm_ser = uart.read()
print("Firmware and serial number:")
print(firm_ser)
print("\n")

# COZIR power Off 
COZIR.value(0)
utime.sleep(2)

# COZIR Power On
COZIR.value(1)
utime.sleep(2)

# Read and print CO2 measurement
uart.write('Z\r\n')
rxData = uart.read()
print('CO2 measurement data')
print(rxData)

# Transform CO2 measurement into ppm value integer
# hexstr = ubinascii.hexlify(rxData)
# print(hexstr)

# integer=int.from_bytes(rxData, 'big')
# print(integer)

# text = rxData.decode('utf-8')
# print(text)
