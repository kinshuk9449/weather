from gpiozero import Button
import time
import requests
import serial
from picamera import PiCamera
import math
import wind_direction_byo
import ldr
import statistics
import serial
import http.client as httplib
import urllib

ser = serial.Serial('/dev/ttyACM0',9600)

store_speeds = []
store_directions = []
wind_count=0

key = "7LBLV1Z2X6A83YPM"

light_sent=0 
rain_sent =0

interval =  60
Bucket_size = 0.2794
radius_cm = 9.0
wind_interval = 5
ADJUSTMENT =1.18

rain_count = 0
pic_interval = 0

camera = PiCamera()
camera.rotation = 180
camera.resolution = (320,240)
camera.framerate = 24

def convert(lst):
        return ([i for item in lst for i in item.split()])
    
def bucket_tipped():
    global rain_count
    rain_count = rain_count+1
    print(rain_count*Bucket_size)

def reset_rainfall():
    global rain_count
    rain_count = 0

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
    
def read_temp():
    read_serial=ser.readline()
    temp = convert(str(read_serial))
    
    j=2
    k=0
    temp_hum = ['','','']
    while j < len(temp):
        if (temp[j] != ","):
            temp_hum[k] += temp[j]
            j +=1
        else:
            if k == 2:
                j=len(temp)
            else:
                k +=1
                j +=1
    return temp_hum

wind_speed_sensor = Button(21)
wind_speed_sensor.when_pressed = spin

rainsensor = Button(6)
rainsensor.when_pressed = bucket_tipped

while True:
    start_time = time.time()
    while time.time() - start_time <= interval:
        wind_start_time = time.time()
        reset_wind()
        
        #time.sleep(wind_interval)
        while time.time() - wind_start_time <= wind_interval:
            store_directions.append(wind_direction_byo.get_value())
        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)
    
    temp_hum = ['','','']
    temp_hum = read_temp() 
    print(temp_hum)
    wind_average = wind_direction_byo.get_average(store_directions)
    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds)
    light_density = ldr.getlight()
    if light_density > 0.6 and light_sent == 0:
        light_sent = 1
        r = requests.post('https://maker.ifttt.com/trigger/light_detected/with/key/q-QKxOXnErbECMlFLdb4z', params={"value1":temp_hum[0],"value2":temp_hum[1],"value3":wind_speed})
    else:
        light_sent = 0
    rainfall = rain_count * Bucket_size
    if rainfall > 0 and rain_sent == 0:
        rain_sent = 1
        r = requests.post('https://maker.ifttt.com/trigger/rain_detected/with/key/q-QKxOXnErbECMlFLdb4z', params={"value1":temp_hum[0],"value2":temp_hum[1],"value3":wind_speed})
    else:
        rain_sent = 0
        
    print(wind_speed, wind_gust,wind_average,light_density)
    reset_rainfall()
    
    params = urllib.parse.urlencode({'field1': temp_hum[0],'field2': temp_hum[1],'field3':rainfall ,'field4':wind_speed ,'field5':wind_gust ,'field6':wind_average,'field7':light_density , 'key':key }) 
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
    except:
            print ("connection failed")
    if pic_interval == 0:
        
        pic_interval+=1
        camera.start_preview(alpha=200)
        time.sleep(2)
        camera.capture('/home/pi/Desktop/pic/image_'+time.strftime("%Y-%m-%d_%H-%M-%S")+'.jpg')
        camera.stop_preview()
    else:
        pic_interval+=1
        if pic_interval == 10:
            pic_interval =0
    store_speeds = []
    store_directions = []