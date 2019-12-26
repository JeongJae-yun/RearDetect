import RPi.GPIO as GPIO
import time
import threading
from tkinter import *

GPIO.setmode(GPIO.BCM) #BCM방식으로 핀 번호를 입력.

#motor module
#left wheel
pwm_pin=17
in1_pin=12
in2_pin=22

#right wheel
pwm_pin2=18
in1_pin2=25
in2_pin2=23

#ultrasonic module
TRIG_ARR =[13,16,4]  #트리거 핀 번호
ECHO_ARR =[19,20,21] #에코 핀 번호
result_arr = [500,500,500] #3개 초음파의 결과 저장 리스트.
FreqDegree=[200,75,10]  #부저의 빈도 횟수
SleepDegree=[0.3,0.2,0.1]   #부저의 간격 초수
CountDegree=[2,3,6] #부저의 빈도 수 

#buz 
BUZ=6 #부저 핀 번호
GPIO.setup(BUZ,GPIO.OUT) #부저 출력 설정
BUZ_PWM=GPIO.PWM(BUZ,900) 

 

#Motor GPIO setup
GPIO.setup(pwm_pin,GPIO.OUT) 
GPIO.setup(pwm_pin2,GPIO.OUT)
GPIO.setup(in1_pin,GPIO.OUT)
GPIO.setup(in1_pin2,GPIO.OUT)
GPIO.setup(in2_pin,GPIO.OUT)
GPIO.setup(in2_pin2,GPIO.OUT)
 

pwm_motor=GPIO.PWM(pwm_pin,5) #모터 시작 설정.
pwm_motor2=GPIO.PWM(pwm_pin2,5) 
pwm_motor.start(0) #모터 0에서 시작
pwm_motor2.start(0)
 
#초음파 센서 3개의 트리거, 에코를 입/출력 설정 
for i in range(0,3):
    GPIO.setup(TRIG_ARR[i],GPIO.OUT)
    GPIO.setup(ECHO_ARR[i],GPIO.IN)
    GPIO.output(TRIG_ARR[i],GPIO.LOW)

 

#부저 함수 
def buz(deg):

    BUZ_PWM.start(50)

    for i in range(0,CountDegree[deg]):
        BUZ_PWM.ChangeFrequency(FreqDegree[deg])
        time.sleep(SleepDegree[deg])
        
    BUZ_PWM.stop()

 
#거리 계산 함수 
def distance_check(index):

    GPIO.output(TRIG_ARR[index],GPIO.HIGH) #트리거 핀 off상태 
    time.sleep(0.00001)
    GPIO.output(TRIG_ARR[index],GPIO.LOW) 
    stop=0
    start=0

    while GPIO.input(ECHO_ARR[index])==GPIO.LOW: #에코 핀이 on이 되는 시점
        start=time.time()

    while GPIO.input(ECHO_ARR[index])==GPIO.HIGH: #에코핀이 다시 off가 되는 시점 반사판 수신 시간.
        stop=time.time()

    duration=stop-start
    distance=(duration*340*100)/2   #초음파는 반사판이기에 실제 이동거리 2배. 2로 나눈다. // 음속은 340m/s로 계산.
    
    return distance

 
#바퀴 모터 동작 함수
def control(gear):

    if gear == "stop":
        pwm_motor.ChangeDutyCycle(0)
        pwm_motor2.ChangeDutyCycle(0)
        GPIO.output(in1_pin2,False)
        GPIO.output(in2_pin2,False)
        

    elif gear =="go":
        pwm_motor.ChangeDutyCycle(50)
        pwm_motor2.ChangeDutyCycle(50)
        GPIO.output(in1_pin,True)
        GPIO.output(in1_pin2,True)
        GPIO.output(in2_pin,False)
        GPIO.output(in2_pin2,False)

    elif gear =="second":
        pwm_motor.ChangeDutyCycle(25)
        pwm_motor2.ChangeDutyCycle(25)
        GPIO.output(in1_pin,True)
        GPIO.output(in1_pin2,True)
        GPIO.output(in2_pin,False)
        GPIO.output(in2_pin2,False)

    elif gear=="leftSwing":
        pwm_motor2.ChangeDutyCycle(50)
        GPIO.output(in1_pin2,True)
        GPIO.output(in2_pin2,False)

    elif gear=="rightSwing":
        pwm_motor.ChangeDutyCycle(40)
        GPIO.output(in1_pin,True)
        GPIO.output(in2_pin,False)
        

    elif gear =="back":
        pwm_motor.ChangeDutyCycle(50)
        pwm_motor2.ChangeDutyCycle(50)
        GPIO.output(in1_pin,False)
        GPIO.output(in1_pin2,True)
        GPIO.output(in2_pin,True)
        GPIO.output(in2_pin2,True)


#주차 함수
def parking():

    root=Tk() #tkinter start
    control("go") #control car start
    canvas = Canvas(root,width=255,height=529) #캔버스의 크기 설정
    canvas.pack() 

    car=PhotoImage(file='parking.png') #캔버스 이미지 로드
    led_lst=((30,467,85,482,85,526,30,511),(95,486,150,486,150,529,95,529),(210,511,160,526,160,482,210,467)) # 불이 들어올 좌표 선정
    color=('green','orange','red')    
    
    while True: 
        degree=-1 
        deg_temp=-1

        for j in range(0,3):
            result_arr[j]=distance_check(j)  #0,1,2 번째의 초음파 센서를 하나씩 거리 체크해와서 결과 값에 하나씩 저장.
            print("===========================")

            if 0< result_arr[j]<5:  
                deg_temp=2 # 변화 표현
                print(j,"DISTANCE = %.2f cm"%(result_arr[j])) 
                canvas.create_polygon(led_lst[j],fill=color[2]) #가장 가까운 경우 빨간색 좌표 표

                control("stop")   #stop
                
                #gear = input("Press button 'Back' if you want to go forward")   # 사용자의 제어시 추가

                time.sleep(1.5)

                gear="back" #자동 제어시 추가.

                if gear =="back":
                    control(gear) # front control
                    time.sleep(0.3) # 0.5 second wait
                
                    gear="stop" # stop
                    control(gear) #stop control

                    time.sleep(1)
                    
                    if j==2:
                        control("leftSwing")  #왼쪽에서 물체감지 // 왼바퀴 앞으로 돌게 만든다.
                        time.sleep(1)
                        control("stop")

                    elif j==0:
                        control("rightSwing") #오른쪽에서 물체감지 // 오른바퀴 앞으로 돌게 만든다.
                        time.sleep(0.5)
                        control("stop")
                    break


                  
                

            elif 6< result_arr[j] <50:

                deg_temp=1
                print(j,"DISTANCE = %.2f cm"%(result_arr[j]))
                canvas.create_polygon(led_lst[j],fill=color[1])
                control("second")  # 속도 50에서 25로 줄이는 코드. 급정지를 막기위한 코

                

            elif 51< result_arr[j] < 80:

                deg_temp=0
                print(j,"DISTANCE = %.2f cm"%(result_arr[j]))
                canvas.create_polygon(led_lst[j],fill=color[0])
                time.sleep(0.5)

        

        if (deg_temp>degree):  #초음파 센서에 감지가 될 경우. 설정된 거리에 따라 deg_temp의 값이 달라지고 default인 -1보다 커진다.
            degree=deg_temp #거리에 따라 설정된 deg_temp값으로 degree값을 업데이트한다.

        if degree!=-1:   #감지가 되서 값이 바뀌었다면
            thread = threading.Thread(target=buz,args=(degree,))  #바뀌어진 degree값을 인수로 buz함수를 쓰레드 한다.
            thread.start() 
        
        canvas.create_image(0,0,image=car,anchor=NW) # 캔버스를 자동차 이미지로 업데이트
        canvas.update() 
        

try:

    while True:
        case = input("If you want to park, press P === If you don't want to park, press S : ") #첫 시작.

        if case =="p":   
            parking()  #parking함수 호출 
            
        elif case =="s": #후방 감지 종료
            print("End rear detect..") 
            break

 

except KeyboardInterrupt:
    print("cleanup")
    GPIO.cleanup()

 

finally:

    GPIO.cleanup()
