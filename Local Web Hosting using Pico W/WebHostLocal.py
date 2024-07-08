#Code for Hosting Local Website  using Raspberry Pi Pico W or ESP32
import network
import socket
from time
import machine
import wifi_connectivity

# HTML to send to browsers
html = """<!DOCTYPE html>
<html>
<head>
    <title>Hello World</title>
</head>
<body>
    <h1>This is EchoSniper</h1>
    <p>This is an Example of Pico W/ESP32 based Local Host Website. </p>
</body>
</html>
"""

# Setup socket web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024)
    print(request)

    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(html)
    cl.close()
