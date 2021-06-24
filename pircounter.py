import RPi.GPIO as GPIO #module pin IO Raspberry
import time
import paho.mqtt.client as paho #module mqtt

#deklarasi variabel global
n=0
nm=5
lamp="off"

#deklarasi pin I/O
PinLed_In = 4
PinLed_Out = 24
PinBuzzer = 22
PinPIR_In = 27
PinPIR_Out = 21
PinLamp = 25

#setting GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PinLed_In, GPIO.OUT)
GPIO.setup(PinLed_Out, GPIO.OUT)
GPIO.setup(PinBuzzer, GPIO.OUT)
GPIO.setup(PinLamp, GPIO.OUT)
GPIO.setup(PinPIR_In, GPIO.IN)
GPIO.setup(PinPIR_Out, GPIO.IN)

GPIO.output(PinLamp, True)

#function mqtt connect & read message
def on_connect(self, mosq, obj, rc):
        self.subscribe("$dataku/#")
        
def on_message(mosq, obj, msg):
    global nm
    global lamp
    print(msg.topic + " " + str(msg.payload))
    if msg.topic == "dataku/nmax":
        nmax_int=int(msg.payload)
        print(nmax_int)
        nm=nmax_int
        mqttc.publish("datamu",n)
    if msg.topic == "dataku/lampu":
        lamp = str(msg.payload)
        print(lamp)
        mqttc.publish("datamu",n)

#Function Lampu
def lampu():
    if "on" in lamp:
        GPIO.output(PinLamp,False)
    if "off" in lamp:
        GPIO.output(PinLamp, True)

#function alarm
def alarm():
    global n
    global nm
    if n == nm:
        print("alarm on")
        GPIO.output(PinBuzzer, True)
        mqttc.publish("datlarm","ON")
    elif n != nm:
        GPIO.output(PinBuzzer, False)
        print("alarm off")
        mqttc.publish("datlarm","OFF")

#function sensor masuk
def count_masuk():
    global n
    if GPIO.input(PinPIR_In):
        GPIO.output(PinLed_In, True)
        time.sleep(1)
        GPIO.output(PinLed_In, False)
        time.sleep(2) 
        n+=1
        print("Masuk")
        print("jumlah orang : ",n)
        mqttc.publish("datamu",n)
        alarm()

#function sensor keluar
def count_keluar():
    global n
    if n>0:
        if GPIO.input(PinPIR_Out):
            GPIO.output(PinLed_Out, True)
            time.sleep(1)
            GPIO.output(PinLed_Out, False)
            time.sleep(2) 
            n-=1
            print("Keluar")
            print("jumlah orang : ",n)
            mqttc.publish("datamu",n)
            alarm()

#setting mqtt
mqttc = paho.Client()
mqttc.connect("broker.hivemq.com", 1883)
mqttc.loop_start()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

#main program
while True:
    mqttc.publish("datamu",n)
    mqttc.subscribe("dataku/#")
    lampu()
    count_masuk()
    count_keluar()
    time.sleep(1)

