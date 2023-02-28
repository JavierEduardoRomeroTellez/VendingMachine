from flask import Flask, render_template, request, redirect
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

TRIG = 24
ECHO = 23

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/button', methods=['POST'])
def button():
    button_value = request.form['button']
    accionar_servo(button_value)
    return redirect('/')
    
def accionar_servo(button_value):
    pca = ServoKit(channels=16)
    
    print(button_value)
    
    print('Encendiendo servomotor:', button_value)
    pca.continuous_servo[int(button_value)].throttle = 1
    
    
    newDistance=0
    while True:
        i=0
        avgDistance=0
        for i in range(5):
            GPIO.output(TRIG, False)
            time.sleep(0.1)
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
            while GPIO.input(ECHO)==0:
                continue
            pulse_start = time.time()
            while GPIO.input(ECHO)==1:
                continue
            pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance,2)
            avgDistance = avgDistance + distance
        avgDistance = avgDistance/5
        avgDistance = round(avgDistance)
        if avgDistance < newDistance:
            break
        else:
            newDistance = avgDistance
    
    print('Apagando servomotor:', button_value)
    pca.continuous_servo[int(button_value)].throttle = 0

if __name__ == '__main__':
    app.run(debug=True)
		
