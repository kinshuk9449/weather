import serial
ser = serial.Serial('/dev/ttyACM0',9600)
def convert(lst):
        return ([i for item in lst for i in item.split()])
while True:
    read_serial=ser.readline()
    temp = convert(str(read_serial))

    j=2
    k=0
    bc = ['','','']
    while j < len(temp):
        if (temp[j] != ","):
            bc[k] += temp[j]
            j +=1
        else:
            if k == 2:
                j=len(temp)
            else:
                k +=1
                j +=1  
    print(bc)