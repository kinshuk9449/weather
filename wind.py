from gpiozero import Button
import time
import math
import statistics

store_speeds = []

wind_count=0


radius_cm = 9.0
wind_interval = 5
ADJUSTMENT =1.18

def spin():
    global wind_count
    wind_count = wind_count+1
    
def calculate_speed(time_sec):
    global wind_count
    cicumference_cm = (2*math.pi)*radius_cm
    rotations = wind_count/2.0
    
    dist_km = (cicumference_cm * rotations)/100000
    
    km_per_sec = dist_km/ time_sec
    km_per_hour = km_per_sec *3600
    
    return km_per_hour * ADJUSTMENT

def reset_wind():
    global wind_count
    wind_count=0

wind_speed_sensor = Button(21)
wind_speed_sensor.when_pressed = spin

while True:
    start_time = time.time()
    while time.time() - start_time <= wind_interval:
        reset_wind()
        time.sleep(wind_interval)
        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)
        
    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds)
    print(wind_speed, wind_gust) 