#Library For The Code. 
from machine import Pin, I2C 
import network
import socket
import utime 
from utime import sleep
import machine
import wifi_connection

#Builtin Temperature Sensor and ADC Setup 

ADCPIN = 4 #For using the built in Pin
ADC_RESOLUTION = 65535 #can be refused for 2 other Temperature Sensor 
VOLTAGE_REFERENCE = 3.3 #voltage provided through the USB
sensor1 = machine.ADC(ADCPIN)

#Senor Pin Assigning

gas_pin=3 # Insert Gas Sensor Digital Input Pin  3 
ir_pin=4   #  Insert IR Sensor Digital Input Pin  4

#GIPO Pin Assigning

gas=Pin(gas_pin, Pin.IN)
IR=Pin(ir_pin, Pin.IN)
relay1=Pin(3, Pin.OUT)

#Setting Variables

fire_detected=0
gas_detected=0
floor=""
color="yellow"
last_check="Just Now"
condition="Normal"

#Temperature Sensor Function

def ReadTemperature():
    adc_value = sensor1.read_u16()
    volt = (VOLTAGE_REFERENCE / ADC_RESOLUTION) * adc_value
    temperature = 27 - (volt - 0.706) / 0.001721
    return round(temperature, 1)

#Code Prepared by Raafiu2010732 

# HTML Generation with multiple Variables

def generate_html(temp, gas_detected, fire_detected):
   
   #Setting the Background Color for the Required Warning Signs
    if fire_detected==1:
        color = "red"
    elif gas_detected==1:
        color = "yellow"
    else:
        color = "green"
#HTML File Input For the Local Host Website
    html = f"""
<!DOCTYPE html>

<html>

    <head>

        <meta charset="UFT-8">
        <meta name="description" content="Fire Alarm the ability to detect the floor at which the fire is taking place">
        <meta name="keywords" content="Awanress, Hazards, Safety">
        <meta name="Name" content="Raafiu Mahmood">'
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="120"> 

    </head>
    
<body style="background-color:{color};text-align: center;"> 
    
    <title style="color: rgb(4, 0, 255); margin-top: 0%; text-align: center; "> The Fire Alarm with Location</title>
    <h1 style="color: rgb(0, 4, 255); margin-top: 0%; text-align: center; "> The Fire Alarm with Location</h2>
    <h2 style="color: rgb(0, 4, 255); margin-top: 0%; text-align: center; "> Project by Raafiu, Taremun and Anika</h2>
    <h1 style="color: rgb(0, 4, 255); margin-top: 0%; text-align: center; "> Last Check: {last_check}</h1>
    <h1 style="color: rgb(0, 4, 255); margin-top: 0%; text-align: center; "> Status: </h1>
    <h1 style="color: rgb(0, 4, 255); margin-top: 0%; text-align: center; "> {condition}</h1>
    <h1 style="color: rgb(0, 4, 255); margin-top: 0%; text-align: center; "> {floor}</h1>
    <h1 style="color: rgb(0, 4, 255); margin-top: 0%; text-align: center; "> Location: Plot 16 Aftab Uddin Ahmed Rd, Dhaka 1229 </h1>
    <!-- HTML Prepared by Raafiu2010732 -->
</body>

</html>
    """
    return html


# Setup socket web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)

while True:
    #Setting Up Time or Last Check Time
    
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
        print("Last Check:{HH:>02d}:{MM:>02d}".format(HH=time[3], MM=time[4], SS=time[5]))
        print("Fire") #Testing without Display
        color="red"
        condition="Fire Hazard"
        floor="Floor 1"
        fire_detected=1
        relay1.on()
        
#Gas Leakage Condition
        
    elif Gas==1:
        #print("Gas Detected")
        #print("LastCheck{HH:>02d}:{MM:>02d}".format(HH=time[3], MM=time[4], SS=time[5]))
        print("yellow")
        condition="Gas Leakage"
        floor="Floor 1"
        gas_detected=1
        relay1.off()
        
#Normal Condition
        
    else:
        print("All Good and Clear") 
        print("LastCheck:{HH:>02d}:{MM:>02d}".format(HH=time[3], MM=time[4], SS=time[5]))
        print("green")
        floor="All Floor Status Normal"
        condition="Normal"
        relay1.off()
        
# Accept incoming connection
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024)
    print(request)
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(generate_html(temp, gas_detected, fire_detected))
    cl.close()
