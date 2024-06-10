import machine
import time
import utime
from machine import Pin, I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
# Constants
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
# Main loop
while True:
        # Read the temperature
        temperature = ReadTemperature()
        # I2C address of the LCD
        I2C_ADDR = 0x27
        # Define the number of rows and columns of the LCD  
        I2C_NUM_ROWS = 2
        I2C_NUM_COLS = 16
        # Initialize I2C interface (SDA on GPIO 0, SCL on GPIO 1, frequency 400kHz)
        i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000) 
        # Initialize the LCD
        lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
        a=str(temperature)
        # Move the cursor to the first row, first column
        lcd.move_to(0, 0)
        # Display the first message
        lcd.putstr(f"{a}C Temperature")
        # Move the cursor to the second row, first column
        lcd.move_to(0, 1)
        # Display the second message
        time = utime.localtime()
        lcd.putstr("{year:>04d}/{month:>02d}/{day:>02d} {HH:>02d}:{MM:>02d}".format(
            year=time[0], month=time[1], day=time[2],
            HH=time[3], MM=time[4], SS=time[5]))
        utime.sleep(30)


        

