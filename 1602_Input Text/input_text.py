from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
import time

# Raspberry Pi Pico: sda=Pin(0), scl=Pin(1) for I2C0

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

I2C_ADDR = 0x27  # Replace with your actual I2C address

lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)  # 2 lines, 16 columns


ADCPIN = 4
ADC_RESOLUTION = 65535
VOLTAGE_REFERENCE = 3.3
# Initialize the ADC 
sensor = machine.ADC(ADCPIN)
def ReadTemperature():
    # Read the raw ADC value
    adc_value = sensor.read_u16()
    # Convert the raw ADC value to a voltage
    volt = (VOLTAGE_REFERENCE / ADC_RESOLUTION) * adc_value
    # Convert the voltage to temperature (in Celsius)
    temperature = 27 - (volt - 0.706) / 0.001721
    # Return the temperature rounded to one decimal place
    return round(temperature)
# 

# Input Based Code

lcd.putstr(ReadTemperature())
time.sleep(2)
lcd.move_to(0, 1)
lcd.putstr(input("Second Row: "))
