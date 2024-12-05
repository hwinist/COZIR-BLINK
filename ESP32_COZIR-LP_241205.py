#This is the leanest script I could find to do the following tasks:
#- Initiate a measurement cycle of ten consecutive CO2 measurements every 24 hours
#- Send each measurement value via WiFi to an MQTT broker
#- Store each measurement value consecutively in a text document in the internal flash memory of the ESP32
#- Go into deepsleep mode between measurement cycles to save power

import machine, time, esp32, network, config, deepsleep, micropython
import tinypico as TinyPICO
from time import sleep, sleep_ms
from machine import Pin, UART
from deepsleep import go_deepsleep
from umqtt.simple import MQTTClient
from micropython import const

# Network settings
WIFI_SSID = config.wifi_ssid
WIFI_PSWD = config.wifi_password

# Create Station interface
sta_if = network.WLAN(network.STA_IF)

# Initialize UART communication
# UART 1 [TinyPico], TX= Pin 33, RX= Pin 32
uart = UART(1, baudrate=9600, tx=32, rx=33, bits=8, parity=None, stop=1) 

# Initialize COZIR-LP
# 3.3V-Bezug UND on/off-Kontrolle durch COZIR an Pin21 TinyPico

# MQTT Parameters
MQTT_SERVER = config.mqtt_server
MQTT_PORT = config.mqtt_port
MQTT_USER = config.mqtt_username
MQTT_PASSWORD = config.mqtt_password
MQTT_CLIENT_ID = b"tinypico"
MQTT_KEEPALIVE = 7200
MQTT_SSL = False   # set to False if using local Mosquitto MQTT broker
MQTT_TOPIC_co2 = 'tinypico/co2'
client = MQTTClient(client_id=MQTT_CLIENT_ID,
                            server=MQTT_SERVER,
                            port=MQTT_PORT,
                            user=MQTT_USER,
                            password=MQTT_PASSWORD,
                            keepalive=MQTT_KEEPALIVE)

def connect_wifi():
    if not sta_if.isconnected():
        print("Connecting to Wi-Fi", end="")
        # Activate station/Wi-Fi client interface
        sta_if.active(True)
        # Connect
        sta_if.connect(WIFI_SSID, WIFI_PSWD)
        # Wait untill the connection is estalished
        while not sta_if.isconnected():
            print(".", end="")
            sleep_ms(100)
        print(" Connected")

def disconnect_wifi():
    if sta_if.active():
        sta_if.active(False)
    if not sta_if.isconnected():
        print("Disconnected")

# Initialize MQTT connection
def connect_mqtt():
    try:
        print('Waiting for MQTT connection...')
        client.connect()
        print('MQTT connection successful')
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)
        raise  # Re-raise the exception to see the full traceback

def COZIR_LP_measurement():
    time.sleep(6) # 'Time to Valid  Measurement After Power‐On = max. 6.5 sec.' (CozIR-Blink-DataSheet-Rev-4.25_3.pdf, p. 13)
    # uart.write('K 1\r\n') # MODE 1 STREAMING MODE - This is the factory default setting. Measurements are reported twice per second. Commands areprocessed when received, except during measurement activity, so there may be a time delay of up to 100ms in responding to commands.
    file = open ("tinypico_co2", "a")
    # Read and send CO2 measurement
    for i in range(10):
        uart.write('Z\r\n')
        time.sleep(1)
        data = uart.readline()
        if data:
            file.write(data)
            client.publish(MQTT_TOPIC_co2, data, qos=0)
            print("CO2 value published")
            time.sleep(1)
    file.write("\r\n")
    file.close()

def main():
    connect_wifi()
    connect_mqtt()
    COZIR_LP_measurement()
    client.disconnect()
    disconnect_wifi()
    go_deepsleep(88507156) # 24h minus measurement cycle ~25s, correctred by a factor of 1.0247 (due to measured inaccuracy of the internal clock of the ESP32); in milliseconds.

if __name__ == '__main__':
    main()