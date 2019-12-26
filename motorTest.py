import RPi.GPIO as GPIO
#import warnings
#warnings.filterwarnings('ignore')
GPIO.setmode(GPIO.BCM)

#left 

pwm_pin=17
in1_pin=12
in2_pin=22


#right
pwm_pin2 =18
in1_pin2 =25
in2_pin2 =26

#GPIO setupt 
GPIO.setup(pwm_pin,GPIO.OUT)
GPIO.setup(pwm_pin2,GPIO.OUT)
GPIO.setup(in1_pin,GPIO.OUT)
GPIO.setup(in1_pin2,GPIO.OUT)
GPIO.setup(in2_pin,GPIO.OUT)
GPIO.setup(in2_pin2,GPIO.OUT)

#pwm_motor pin
pwm_motor=GPIO.PWM(pwm_pin,100)
pwm_motor2=GPIO.PWM(pwm_pin2,100)
pwm_motor.start(0)
pwm_motor2.start(0)

while True:
    gear =input("press w:go / s:stop / x:back  :")
    if gear =="s":
        pwm_motor.ChangeDutyCycle(0)
        pwm_motor2.ChangeDutyCycle(0)
    elif gear =="w":
        pwm_motor.ChangeDutyCycle(75)
        pwm_motor2.ChangeDutyCycle(75)
        GPIO.output(in1_pin,True)
        GPIO.output(in1_pin2,True)
        GPIO.output(in2_pin,False)
        GPIO.output(in2_pin2,False)
    elif gear =="ww":
        pwm_motor.ChangeDutyCycle(100)
        pwm_motor2.ChangeDutyCycle(100)
        GPIO.output(in1_pin,True)
        GPIO.output(in1_pin2,True)
        GPIO.output(in2_pin,False)
        GPIO.output(in2_pin2,False)
    elif gear =="x":
        pwm_motor.ChangeDutyCycle(20)
        pwm_motor2.ChangeDutyCycle(30)
        GPIO.output(in1_pin,True)
        GPIO.output(in1_pin2,False)
        GPIO.output(in2_pin,True)
        GPIO.output(in2_pin2,True)
    elif gear =="xx":
        pwm_motor.ChangeDutyCycle(100)
        pwm_motor2.ChangeDutyCycle(100)
        GPIO.output(in1_pin,False)
        GPIO.output(in1_pin2,False)
        GPIO.output(in2_pin,True)
        GPIO.output(in2_pin2,True)
    else:
        GPIO.cleanup()


