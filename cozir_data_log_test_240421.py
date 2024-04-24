# Test UART data exchange with COZIR BLINK, read a CO2 measurement and print ppm

# UART configuration according to: https://www.gassensing.co.uk/wp-content/uploads/2023/05/CozIR-Blink-DataSheet-Rev-4.25_3.pdf, p. 29
# AT commands according to: https://www.gassensing.co.uk/wp-content/uploads/2023/05/CozIR-Blink-DataSheet-Rev-4.25_3.pdf, p. 30

# Import libraries
from machine import UART, Pin
import utime
import ubinascii
import _thread
from struct import unpack

# Anschluss und 3.3V-Bezug durch COZIR an '3V3(OUT' (Position 36)

# "Pin 2 is the supply voltage & pin 4 is the control of the internal regulator. If you connect pin2 to the 3.3V supply, you can use pin 4 to control the sensor, high  enables the sensor & low disables the power. This pin is connected to the enable pin of the internal regulator, so it avoids powering the sensor from an I/O port." (Neil from GSS in mail from 10.04.'24)
power_switch = machine.Pin(22, machine.Pin.OUT, machine.Pin.PULL_DOWN) # 

# UART configuration
# UART 0 [Pico W], TX=GP0 (Pin 1), RX=GP1 (Pin 2)
# UART 1 [Cozir Blink], TX= Pin 11, RX= Pin 12
uart = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1) # 'The unit of communication is a character (not to be confused with a string character) which can be 8 or 9 bits wide.'

# Pico-internal LED shall be on for 2 seconds when Cozir gives data-ready message
led_onboard=machine.Pin("LED", machine.Pin.OUT)
data_ready_pin = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_DOWN) # '6 READY Digital Output Data ready pin. Pulsed high when data ready' (CozIR-Blink-DataSheet-Rev-4.25_3.pdf, p. 8)

def data_ready_thread():
    global data_ready
    data_ready = False
    while True:
        if data_ready_pin.value() == 1:
            data_ready = True
            led_onboard.value(1)
            utime.sleep(2)
            led_onboard.value(0)

# Return firmware version and sensor serial number from COZIR -> AT commend to COZIR: "Y"
uart.write('Y\r\n')
utime.sleep(2)
firm_ser = uart.read()
print("Firmware and serial number:")
print(firm_ser)
print("\n")

_thread.start_new_thread(data_ready_thread, ())

while True:
    
    # COZIR power Off 
    power_switch.value(0)
    utime.sleep(1)

    # COZIR Power On
    power_switch.value(1)
    utime.sleep(5) # At 16 pulses per reading (default setting), a reading takes about 3.5 seconds (CozIR-Blink-DataSheet-Rev-4.25_3.pdf, p. 13)

    # Read and print CO2 measurement
    if data_ready == True:
        uart.write('Z')
        utime.sleep(2)
        myFrame = bytearray(2) # 'The CO2 reading will be in 2 bytes, MSB first, then LSB followed by a status byte. Note that the default data output format is Binary.' (CozIR-Blink-DataSheet-Rev-4.25_3.pdf, p. 29)
        uart.readinto(myFrame)
        print('CO2 measurement data:')
        decimal_value = int.from_bytes(myFrame, 'big')
        print (decimal_value)

    else:
        print('No measurement data available')
        
    utime.sleep(60)
    
