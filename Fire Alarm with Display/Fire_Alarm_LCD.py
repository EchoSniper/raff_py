# Import
from machine import Pin
import utime 
#Setting for Pins and Constants 
gas_pin=14
ir_pin=15
from machine import Pin, I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
gas=Pin(gas_pin, Pin.IN)
IR=Pin(ir_pin, Pin.IN)
        # I2C address of the LCD
I2C_ADDR = 0x27
# Define the number of rows and columns of the LCD  
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
# Initialize I2C interface (SDA on GPIO 0, SCL on GPIO 1, frequency 400kHz)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000) 
# Initialize the LCD
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Constants
ADCPIN = 4
ADC_RESOLUTION = 65535
VOLTAGE_REFERENCE = 3.3
sensor1 = machine.ADC(ADCPIN)

#Temperature Sensor Function 
def ReadTemperature():
    adc_value = sensor1.read_u16()
    volt = (VOLTAGE_REFERENCE / ADC_RESOLUTION) * adc_value
    temperature = 27 - (volt - 0.706) / 0.001721
    return round(temperature, 1)
a="Hello"
#Main Loop 
while True:
    time = utime.localtime()
    last_check=("{year:>04d}/{month:>02d}/{day:>02d} {HH:>02d}:{MM:>02d}".format(
            year=time[0], month=time[1], day=time[2],
            HH=time[3], MM=time[4], SS=time[5]))
    Gas=gas.value()
    ir= IR.value()
    temp=ReadTemperature()

    if  ir==0 and Gas==0 and temp==50:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Fire at Level 1")
        lcd.move_to(0, 1)
        lcd.putstr("Last Check:{HH:>02d}:{MM:>02d}".format(HH=time[3], MM=time[4], SS=time[5]))
        print("Fire")
    elif Gas==0:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Gas Detected")
        lcd.move_to(0, 1)
        lcd.putstr("LastCheck{HH:>02d}:{MM:>02d}".format(HH=time[3], MM=time[4], SS=time[5]))
        print("Gas")
    else:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Status:Normal")
        lcd.move_to(0, 1)
        lcd.putstr("LastCheck:{HH:>02d}:{MM:>02d}".format(HH=time[3], MM=time[4], SS=time[5]))
        print("Status Normal")
    print()
    utime.sleep(10)
    

        
        
        
