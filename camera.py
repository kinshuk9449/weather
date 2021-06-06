from picamera import PiCamera
import time

camera = PiCamera()
camera.rotation = 180
camera.resolution = (320,240)
camera.framerate = 24
camera.start_preview(alpha=200)
time.sleep(1)
camera.capture('/home/pi/Desktop/pic/image_'+time.strftime("%Y-%m-%d_%H-%M-%S")+'.jpg')
camera.stop_preview()