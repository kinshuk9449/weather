from gpiozero import Button

rainsensor = Button(6)
Bucket_size = 0.2794
count = 0

def bucket_tipped():
    global count
    count = count+1
    print(count*Bucket_size)

def reset_rainfall():
    global count
    count = 0

rainsensor.when_pressed = bucket_tipped