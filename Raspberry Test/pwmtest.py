import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

def pwm():
    freq=0
    tast=0
    
    freq = input("Freq eingeben ")
    if freq!="":
        freq = int(freq)
    else:
        pwm()
        return()
        
    tast = input("Tast eingeben ")  
    if tast!="":
        tast = int(tast)
    else:
        pwm()
        return()
        
    p = GPIO.PWM(18, freq) #Kanal 18, 0.5Hz
    p.start(tast)           #Tastverhältnis 70%
    end = input('Enter y to restart (else stop): ')
    
    if end=="y":
        pwm()
    else:
        p.stop()
        GPIO.cleanup()
    
    
pwm()