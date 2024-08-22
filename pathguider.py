from machine import Pin, UART,PWM
import utime, time
import math


rcv = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
buff = bytearray(255)
TIMEOUT = False

motor1 = Pin(8, Pin.OUT)
motor2 = Pin(9, Pin.OUT)
motor3 = Pin(7, Pin.OUT)
motor4 = Pin(6, Pin.OUT)

motor5 = Pin(12, Pin.OUT)
motor6 = Pin(13, Pin.OUT)
buz = Pin(21, Pin.OUT)
motor5.value(0)
motor6.value(0)
trigger = Pin(2, Pin.OUT)
echo = Pin(3, Pin.IN)



rs = machine.Pin(10,machine.Pin.OUT)
e = machine.Pin(11,machine.Pin.OUT)
d4 = machine.Pin(12,machine.Pin.OUT)
d5 = machine.Pin(13,machine.Pin.OUT)
d6 = machine.Pin(14,machine.Pin.OUT)
d7 = machine.Pin(15,machine.Pin.OUT)
d7 = machine.Pin(15,machine.Pin.OUT)
buz = machine.Pin(28,machine.Pin.OUT)
b1=machine.Pin(26,machine.Pin.IN)
b2=machine.Pin(27,machine.Pin.IN)
def pulseE():
    e.value(1)
    utime.sleep_us(40)
    e.value(0)
    utime.sleep_us(40)
def send2LCD4(BinNum):
    d4.value((BinNum & 0b00000001) >>0)
    d5.value((BinNum & 0b00000010) >>1)
    d6.value((BinNum & 0b00000100) >>2)
    d7.value((BinNum & 0b00001000) >>3)
    pulseE()
def send2LCD8(BinNum):
    d4.value((BinNum & 0b00010000) >>4)
    d5.value((BinNum & 0b00100000) >>5)
    d6.value((BinNum & 0b01000000) >>6)
    d7.value((BinNum & 0b10000000) >>7)
    pulseE()
    d4.value((BinNum & 0b00000001) >>0)
    d5.value((BinNum & 0b00000010) >>1)
    d6.value((BinNum & 0b00000100) >>2)
    d7.value((BinNum & 0b00001000) >>3)
    pulseE()
def setUpLCD():
    rs.value(0)
    send2LCD4(0b0011)#8 bit
    send2LCD4(0b0011)#8 bit
    send2LCD4(0b0011)#8 bit
    send2LCD4(0b0010)#4 bit
    send2LCD8(0b00101000)#4 bit,2 lines?,5*8 bots
    send2LCD8(0b00001100)#lcd on, blink off, cursor off.
    send2LCD8(0b00000110)#increment cursor, no display shift
    send2LCD8(0b00000001)#clear screen
    utime.sleep_ms(2)#clear screen needs a long delay

buz.value(0)
setUpLCD()
rs.value(1)
for x in 'B1- A to B':
    send2LCD8(ord(x))
rs.value(0)
time.sleep(0.01)
send2LCD8(0b11000000)
time.sleep(0.01)
rs.value(1)
time.sleep(0.01)
for x in 'B2- A to C':
    send2LCD8(ord(x))




def ultra():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   return distance
lst=[]
md=0
tme=[]
st=0
tt=0

lst1=[]

tme1=[]
st1=0
tt1=0
rcv.write('1-for front')
rcv.write('2-for back')
rcv.write('3-for left')
rcv.write('4-for right')
rcv.write('5-for stop')

mab=0
mac=0
while True:
    time.sleep(0.3)
    dist=ultra()
    print(dist)
    
    
    if(dist<15):
        print('obs')
        motor1.value(0)
        motor2.value(0)
        motor3.value(0)
        motor4.value(0)
        buz.value(1)
        time.sleep(0.5)
        buz.value(0)
        
    if(st>0 and dist>14):
        tt=tt+1
    if(st1>0 and dist>14):
        tt1=tt1+1
        
    if(b1.value()==0):

            if(mab==1):
                tme.append(tt)
                print("Acting MODE")
                md=2
                print(lst)
                print(tme)
                setUpLCD()
                rs.value(1)
                for x in 'Trip A-B':
                    send2LCD8(ord(x))
                time.sleep(5)
            else:
                setUpLCD()
                rs.value(1)
                for x in 'No Map':
                    send2LCD8(ord(x))
                time.sleep(5)
                
                setUpLCD()
                rs.value(1)
                for x in 'B1- A to B':
                    send2LCD8(ord(x))
                rs.value(0)
                time.sleep(0.01)
                send2LCD8(0b11000000)
                time.sleep(0.01)
                rs.value(1)
                time.sleep(0.01)
                for x in 'B2- A to C':
                    send2LCD8(ord(x))

                
            
        
    if(b2.value()==0):
            if(mac==1):
                tme1.append(tt1)
                print("Acting MODE")
                md=4
                print(lst1)
                print(tme1)
                setUpLCD()
                rs.value(1)
                for x in 'Trip A-C':
                    send2LCD8(ord(x))
                time.sleep(5)
            else:
                setUpLCD()
                rs.value(1)
                for x in 'No Map':
                    send2LCD8(ord(x))
                time.sleep(5)
                
                setUpLCD()
                rs.value(1)
                for x in 'B1- A to B':
                    send2LCD8(ord(x))
                rs.value(0)
                time.sleep(0.01)
                send2LCD8(0b11000000)
                time.sleep(0.01)
                rs.value(1)
                time.sleep(0.01)
                for x in 'B2- A to C':
                    send2LCD8(ord(x))
    if(1):
        if(md==2):
            motor5.value(1)
            motor6.value(0)
            for i in range(0,len(lst)-1):
                if(lst[i]==1):
                    print('front')
                    motor1.value(1)
                    motor2.value(0)
                    motor3.value(1)
                    motor4.value(0)
                if(lst[i]==2):
                    print('back')
                    motor1.value(0)
                    motor2.value(1)
                    motor3.value(0)
                    motor4.value(1)
                if(lst[i]==3):
                    print('left')
                    motor1.value(1)
                    motor2.value(0)
                    motor3.value(0)
                    motor4.value(1)
                if(lst[i]==4):
                    print('right')
                    motor1.value(0)
                    motor2.value(1)
                    motor3.value(1)
                    motor4.value(0)
                if(lst[i]==5):
                    print('stop')
                    motor1.value(0)
                    motor2.value(0)
                    motor3.value(0)
                    motor4.value(0)
                    
                    
                time.sleep(tme[i]*0.3)

            motor1.value(0)
            motor2.value(0)
            motor3.value(0)
            motor4.value(0)
            print('Task Completed')
            md=0
    if(1):        
            
        if(md==4):
 
            for i in range(0,len(lst1)-1):
                if(lst1[i]==1):
                    print('front')
                    motor1.value(1)
                    motor2.value(0)
                    motor3.value(1)
                    motor4.value(0)
                if(lst1[i]==2):
                    print('back')
                    motor1.value(0)
                    motor2.value(1)
                    motor3.value(0)
                    motor4.value(1)
                if(lst1[i]==3):
                    print('left')
                    motor1.value(1)
                    motor2.value(0)
                    motor3.value(0)
                    motor4.value(1)
                if(lst1[i]==4):
                    print('right')
                    motor1.value(0)
                    motor2.value(1)
                    motor3.value(1)
                    motor4.value(0)
                if(lst1[i]==5):
                    print('stop')
                    motor1.value(0)
                    motor2.value(0)
                    motor3.value(0)
                    motor4.value(0)
                time.sleep(tme1[i]*0.3)
            motor1.value(0)
            motor2.value(0)
            motor3.value(0)
            motor4.value(0)            
            print('Task Completed')
            md=0
        
    x=rcv.read()
    if (x is not None):
        x=x.decode()
        print(x)
        time.sleep(1)
 
        if(x=='6'):
            mab=1
            lst=[]
            md=0
            tme=[]
            st=0
            tt=0            
            print("MAPPING MODE A-B")
            setUpLCD()
            rs.value(1)
            for x in 'Mapping':
                send2LCD8(ord(x))
            rs.value(0)
            time.sleep(0.01)
            send2LCD8(0b11000000)
            time.sleep(0.01)
            rs.value(1)
            time.sleep(0.01)
            for x in 'A to B':
                send2LCD8(ord(x))

            
            md=1
            
        if(x=='8'):
            mac=1
            lst1=[]
            md=0
            tme1=[]
            st1=0
            tt1=0            
            print("MAPPING MODE A-C")
            print("MAPPING MODE A-B")
            setUpLCD()
            rs.value(1)
            for x in 'Mapping':
                send2LCD8(ord(x))
            rs.value(0)
            time.sleep(0.01)
            send2LCD8(0b11000000)
            time.sleep(0.01)
            rs.value(1)
            time.sleep(0.01)
            for x in 'A to C':
                send2LCD8(ord(x))
            
            md=3
        if(x=='7'):
            tme.append(tt)
            print("Acting MODE")
            md=2
            print(lst)
            print(tme)
            setUpLCD()
            rs.value(1)
            for x in 'Trip':
                send2LCD8(ord(x))
            rs.value(0)
            time.sleep(0.01)
            send2LCD8(0b11000000)
            time.sleep(0.01)
            rs.value(1)
            time.sleep(0.01)
            for x in 'A to B':
                send2LCD8(ord(x))
            time.sleep(5)
            
        if(x=='9'):
            tme1.append(tt1)
            print("Acting MODE")
            md=4
            print(lst1)
            print(tme1)
            setUpLCD()
            rs.value(1)
            for x in 'Trip':
                send2LCD8(ord(x))
            rs.value(0)
            time.sleep(0.01)
            send2LCD8(0b11000000)
            time.sleep(0.01)
            rs.value(1)
            time.sleep(0.01)
            for x in 'A to C':
                send2LCD8(ord(x))
            time.sleep(5)
            
        if(md==1):
            time.sleep(0.3)


            if(x=='1'):
                st=st+1
                if(st>1):
                    tme.append(tt)
                    tt=0
                
                lst.append(1)
                print("VEHICLE ON")
                motor1.value(1)
                motor2.value(0)
                motor3.value(1)
                motor4.value(0)
            if(x=='2'):
                st=st+1
                if(st>1):
                    tme.append(tt)
                    tt=0                
                lst.append(2)
                motor1.value(0)
                motor2.value(1)
                motor3.value(0)
                motor4.value(1)
                
            if(x=='3'):
                st=st+1
                if(st>1):
                    tme.append(tt)
                    tt=0
                lst.append(3)
                print("VEHICLE ON")
                motor1.value(1)
                motor2.value(0)
                motor3.value(0)
                motor4.value(1)
            if(x=='4'):
                st=st+1
                if(st>1):
                    tme.append(tt)
                    tt=0
                lst.append(4)
                motor1.value(0)
                motor2.value(1)
                motor3.value(1)
                motor4.value(0)
                
            if(x=='5'):
                st=st+1
                if(st>1):
                    tme.append(tt)
                    tt=0
                lst.append(5)
                motor1.value(0)
                motor2.value(0)
                motor3.value(0)
                motor4.value(0)
                
                
        if(md==3):
            time.sleep(0.3)


            if(x=='1'):
                st1=st1+1
                if(st1>1):
                    tme1.append(tt1)
                    tt1=0
                
                lst1.append(1)
                print("VEHICLE ON")
                motor1.value(1)
                motor2.value(0)
                motor3.value(1)
                motor4.value(0)
            if(x=='2'):
                st1=st1+1
                if(st1>1):
                    tme1.append(tt1)
                    tt1=0                
                lst1.append(2)
                motor1.value(0)
                motor2.value(1)
                motor3.value(0)
                motor4.value(1)
                
            if(x=='3'):
                st1=st1+1
                if(st1>1):
                    tme1.append(tt1)
                    tt1=0
                lst.append(3)
                print("VEHICLE ON")
                motor1.value(1)
                motor2.value(0)
                motor3.value(0)
                motor4.value(1)
            if(x=='4'):
                st1=st1+1
                if(st1>1):
                    tme1.append(tt1)
                    tt1=0
                lst1.append(4)
                motor1.value(0)
                motor2.value(1)
                motor3.value(1)
                motor4.value(0)
                
            if(x=='5'):
                st1=st1+1
                if(st1>1):
                    tme1.append(tt1)
                    tt1=0
                lst1.append(5)
                motor1.value(0)
                motor2.value(0)
                motor3.value(0)
                motor4.value(0)
                
                
        if(md==2):
            motor5.value(1)
            motor6.value(0)
            for i in range(0,len(lst)):
                if(lst[i]==1):
                    print('front')
                    motor1.value(1)
                    motor2.value(0)
                    motor3.value(1)
                    motor4.value(0)
                if(lst[i]==2):
                    print('back')
                    motor1.value(0)
                    motor2.value(1)
                    motor3.value(0)
                    motor4.value(1)
                if(lst[i]==3):
                    print('left')
                    motor1.value(1)
                    motor2.value(0)
                    motor3.value(0)
                    motor4.value(1)
                if(lst[i]==4):
                    print('right')
                    motor1.value(0)
                    motor2.value(1)
                    motor3.value(1)
                    motor4.value(0)
                if(lst[i]==5):
                    print('stop')
                    motor1.value(0)
                    motor2.value(0)
                    motor3.value(0)
                    motor4.value(0)
                time.sleep(tme[i]*0.3)

            print('Task Completed')
            md=0
            
            
        if(md==4):
 
            for i in range(0,len(lst1)):
                if(lst1[i]==1):
                    print('front')
                    motor1.value(1)
                    motor2.value(0)
                    motor3.value(1)
                    motor4.value(0)
                if(lst1[i]==2):
                    print('back')
                    motor1.value(0)
                    motor2.value(1)
                    motor3.value(0)
                    motor4.value(1)
                if(lst1[i]==3):
                    print('left')
                    motor1.value(1)
                    motor2.value(0)
                    motor3.value(0)
                    motor4.value(1)
                if(lst1[i]==4):
                    print('right')
                    motor1.value(0)
                    motor2.value(1)
                    motor3.value(1)
                    motor4.value(0)
                if(lst1[i]==5):
                    print('stop')
                    motor1.value(0)
                    motor2.value(0)
                    motor3.value(0)
                    motor4.value(0)
                time.sleep(tme1[i]*0.3)
            
                print('Task Completed')
                md=0