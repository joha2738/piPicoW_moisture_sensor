# piPicoW_moisture_sensor
Reading the moisture level in a plant and displaying it on a web page


Tilføj evt. nedenstående for at få LED lyset til at skifte farve alt efter fugtighed:


def update_leds():

    for i in range(20):
    
        moisture = read_moisture()
        
        if moisture < 700:
        
            color = (255, int(moisture / 10), 0)
            
        else:
        
            color = (int(255 - moisture / 10), 255, 0)
            
        np[i] = color
        
    np.show()
    
