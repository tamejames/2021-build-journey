import time
import board
import adafruit_dht
from adafruit_circuitplayground.express import cpx

# Source: https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-neopixel
# Source: https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/neopixels

# Take humidity value (coming through pin A2)
dht = adafruit_dht.DHT11(board.A2)

# Initialise Circuit Playground onboard pixels
pixels = cpx.pixels

# Create array where each element is a pair of neopixels, to be used when creating symmetrical 'heartbeat pulse' pattern
heart_pattern_upbeat_array = [(0,9),(1,8),(2,7),(3,6),(4,5)] # Array for 'upbeat' of heartbeat
heart_pattern_downbeat_array = [(4,5),(3,6),(2,7),(1,8),(0,9)] # Array for 'downbeat' of heartbeat

# Create function for controlling neopixels in 'heartbeat pulse' pattern
def make_heartbeat(heartbeat_pattern_array, pixel_colour, pixel_brightness, heartbeat_pulse_time):

    # Lights moving down the heart (downbeat)
    for i in range(len(heartbeat_pattern_array)):
        pixels.brightness = pixel_brightness # Set brightness of neopixels
        pixels[heartbeat_pattern_array[i][0]] = pixel_colour # Set colour of first light in pair
        pixels[heartbeat_pattern_array[i][1]] = pixel_colour # Set colour of second light in pair
        time.sleep(heartbeat_pulse_time) # 
        pixels.show() # Set pixels to display specified colour and brightness
        pixels[heartbeat_pattern_array[i][0]] = (0,0,0) # Set colour of first light in pair to (0,0,0) (effectively 'off')
        pixels[heartbeat_pattern_array[i][1]] = (0,0,0) # Set colour of second light in pair to (0,0,0) (effectively 'off')
        pixels.show() # Set pixels to display specified colour and brightness


# Set up while loop with True condition to ensure it runs continuously
while True:
    # Measure current value of humidity
    humidity = dht.humidity

    # Light up LEDs in heartbeat upbeat pattern (set to green light, with brightness and pulse time related to humidity based on subjective judgement)
    make_heartbeat(heart_pattern_upbeat_array,(0,255,0),(humidity/1000)**1.2, (100-humidity)/400)

    # Measure current value of humidity
    humidity = dht.humidity

    # Light up LEDs in heartbeat upbeat pattern (set to green light, with brightness and pulse time related to humidity based on subjective judgement)
    make_heartbeat(heart_pattern_downbeat_array,(0,255,0),(humidity/1000)**1.2, (100-humidity)/400)

    # Define time between heartbeats, varying with humidity (higher humidity gives faster heartbeat). Noticed that with less than 1.5 seconds, it was possible for the heartbeat to look inconsistent - current hypothesis is that this is related to DHT11 having a sampling period of 1 second (https://www.mouser.com/datasheet/2/758/DHT11-Technical-Data-Sheet-Translated-Version-1143054.pdf)
    time.sleep(2.5-humidity/100) 


