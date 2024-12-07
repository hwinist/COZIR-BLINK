The target of this project is long-term CO2 measurement in a closed glass container to measure the CO2 consumption of growing plants.
Due to the given restrictions (space, power supply, wireless operation), I chose the folllowing hardware components:
- Tinypico, a ESP32 development board by Unexpected Maker: https://www.tinypico.com/
- CozIR®-LP 5000 CO2 Sensor by GSS: https://www.co2meter.com/products/cozir-lp-ambient-air-co2-sensor
- 600mAh, 3.7V Lithium Ion Polymer (LiPo) Rechargeable battery pack taken from UPS Module for Raspberry Pi Pico by Waveshare: https://www.waveshare.com/pico-ups-b.htm

I have decided to use Micropython on Thonny 4.1.4 IDE.
My challenge: I am completely new to programming and am learning on the project.
The key resources are the Micropython documentation (https://docs.micropython.org/en/latest/micropython-docs.pdf), similar projects documented on github, forums and guidance on https://www.elektronik-kompendium.de/ .

The test operation with a 600mAh 3.7V Li-po battery and a reduced time between mesurements of 1h showed the battery capacity was sufficient for 110 hours of operation. Extrapolated to daily measurements instead, a total measurement period of three months at least can be expected. Combined with a battery pack of 3 x 1.5V AA batteries that brings another 3000mAh, more than an entire year of daily measurements should be possible.
