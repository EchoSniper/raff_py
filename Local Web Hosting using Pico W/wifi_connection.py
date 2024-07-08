#Import of Required Libraries
import network
from time import sleep


#Wi-Fi Details
print("Please Note 2.4 Ghz Wi-Fi Can Be Connected Only, Pico W cannot be connected to Wi-Fi 5 Ghz") 
ssid = input('Enter SSID of Your Wi-Fi: ')
password = input('Enter Password of the Wi-Fi: ')

#Connectivity Code
def ConnectWiFi(ssid,password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(10)
    print("Connected!") 
    print("WI-FI DETAILS:")
    print(wlan.ifconfig())

ConnectWiFi()