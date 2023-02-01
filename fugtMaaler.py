import network
import socket
import time
import machine
from lib.neopixel import Neopixel

analog_value = machine.ADC(26)


numpix = 20
pixels = Neopixel(numpix, 0, 16, "GRB")
pixels.brightness(50)


ssid = 'newdahl'
password = '12345678'

def read_moisture():
    reading = analog_value.read_u16()
    # Calibrate the ADC value to a percentage
    # between 0 (dry) and 100 (wet)
    # print (reading)
    return str(100 * reading // 65535)

def alle():
    print ("Lys i alle planter")
    for i in range(0,5):
        pixels.set_pixel(i,(255,0,0))
    for i in range(5,10):
        pixels.set_pixel(i,(0,255,0))
    for i in range(10,15):
        pixels.set_pixel(i,(0,0,255))
    for i in range(15,20):
        pixels.set_pixel(i,(255,0,255))
    pixels.show()
    time.sleep(1)
    for i in range(numpix):
        pixels.set_pixel(i,(0,0,0))
    pixels.show()
    
def plante1():
    print ("Lys i plant 1")
    for i in range(0,5):
        pixels.set_pixel(i,(255,0,0))
    pixels.show()
    time.sleep(1)
    for i in range(numpix):
        pixels.set_pixel(i,(0,0,0))
    pixels.show()
    
def plante2():
    print ("Lys i plant 2")
    for i in range(5,10):
        pixels.set_pixel(i,(0,255,0))
    pixels.show()
    time.sleep(1)
    for i in range(numpix):
        pixels.set_pixel(i,(0,0,0))
    pixels.show()
    
def plante3():
    print ("Lys i plant 3")
    for i in range(10,15):
        pixels.set_pixel(i,(0,0,255))
    pixels.show()
    time.sleep(1)
    for i in range(numpix):
        pixels.set_pixel(i,(0,0,0))
    pixels.show()
    
def plante4():
    print ("Lys i plant 4")
    for i in range(15,20):
        pixels.set_pixel(i,(255,0,255))
    pixels.show()
    time.sleep(1)
    for i in range(numpix):
        pixels.set_pixel(i,(0,0,0))
    pixels.show()
    
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Venter på forbindelse...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Forbundet på {ip}')
    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage():
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Vandforhold i planter</title>
                <meta http-equiv="refresh" content="30">
            </head>
            <center><b>
                <form action="./alle">
                    <input type="submit" value="Lys i alle" style="height:120px; width:120px; color:black" />
                </form>
            <table><tr>      
                <td><form action="./plante1">
                    <input type="submit" value="Plante 1" style="height:40px; width:120px; color:red" />
                </form></td>
                <td><form action="./plante2">
                    <input type="submit" value="Plante 2" style="height:40px; width:120px; color:green" />
                </form></td>
                <td><form action="./plante3">
                    <input type="submit" value="Plante 3" style="height:40px; width:120px; color:blue" />
                </form></td>
                <td><form action="./plante4">
                    <input type="submit" value="Plante 4" style="height:40px; width:120px; color:fuchsia" />
                </form></td>
            </tr></table>
            
            <h1>Moisture Sensor</h1>
            <p>Percentage: """ + read_moisture() + """%</p>
            </body>
            </html>
            """#.format(read_moisture())
    return str(html)

def serve(connection):
    #Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/alle?':
            alle()
        elif request =='/plante1?':
            plante1()
        elif request =='/plante2?':
            plante2()
        elif request =='/plante3?':
            plante3()
        elif request =='/plante4?':
            plante4()
        html = webpage()
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
