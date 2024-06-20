# Import
from machine import Pin, I2C
import utime
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

#Setting for Pins and Constants 
gas_pin=14 # Insert Gas Sensor Digital Input Pin 
ir_pin=15    # Insert IR Sensor Digital Input Pin 
gas=Pin(gas_pin, Pin.IN)
IR=Pin(ir_pin, Pin.IN)
ADCPIN = 4 #For using the built in Pin
ADC_RESOLUTION = 65535 
VOLTAGE_REFERENCE = 3.3
sensor1 = machine.ADC(ADCPIN)

#LCD1602 Settings 
I2C_ADDR = 0x27 # I2C address of the LCD
I2C_NUM_ROWS = 2 # Define the number of rows 
I2C_NUM_COLS = 16 # And columns of the LCD 
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000) # Initialize I2C interface (SDA on GPIO 0, SCL on GPIO 1, frequency 400kHz)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS) # Initialize the LCD

#Temperature Sensor Function 
def ReadTemperature():
    adc_value = sensor1.read_u16()
    volt = (VOLTAGE_REFERENCE / ADC_RESOLUTION) * adc_value
    temperature = 27 - (volt - 0.706) / 0.001721
    return round(temperature, 1)
a="No Comment"
#Main Loop 
while True:
   
   #Setting Up Time
   time = utime.localtime()
    last_check=("{year:>04d}/{month:>02d}/{day:>02d} {HH:>02d}:{MM:>02d}".format(
            year=time[0], month=time[1], day=time[2],
            HH=time[3], MM=time[4], SS=time[5]))
    
    #Reading For the Sensors 
    Gas=gas.value()
    ir= IR.value()
    temp=ReadTemperature()

    #Fire Hazard
    if  ir==0 and Gas==0 and temp==50:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Fire at Level 1")
        lcd.move_to(0, 1)
        lcd.putstr("Last Check:{HH:>02d}:{MM:>02d}".format(HH=time[3], MM=time[4], SS=time[5]))
        print("Fire") #Testing without Display
        
    #Gas Leakage Condition 
    elif Gas==0:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Gas Detected")
        lcd.move_to(0, 1)
        lcd.putstr("LastCheck{HH:>02d}:{MM:>02d}".format(HH=time[3], MM=time[4], SS=time[5]))
        print("Gas") #Testing without Display
        
    #Normal Condition     
    else:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Status:Normal")
        lcd.move_to(0, 1)
        lcd.putstr("LastCheck:{HH:>02d}:{MM:>02d}".format(HH=time[3], MM=time[4], SS=time[5]))
        print("Status Normal") #Testing without Display
    
    #Setting Delays 
    print()
    utime.sleep(10)
#This Code was prepared by Raafiu Mahmood A.K.A EchoSniper. 
