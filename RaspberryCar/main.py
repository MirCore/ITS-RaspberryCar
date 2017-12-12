import threading  # Modul threads
import time  # Modul time

from abstand import distanz  # Funktion für Wandabstand messen importieren
from aufraeumen import aufraeumen, losfahren  # Funktion für cleanup() importieren
from gpiosetup import *  # GPIO Setup importieren und ausführen
from linienfahren import linienfahren
from wandfahren import wandfahren

speed = 3  # 1 bis 4 (*25) (% Tastverhältnis)


def lenken(steer):
    speedHead = (100 - speed * 25) / 25
    if steer == 1:
        pr.ChangeDutyCycle(speed * 25)  #
        pl.ChangeDutyCycle(speed * 25)  #
    elif steer < 1:
        pr.ChangeDutyCycle(((1 - steer) * speedHead + speed) * 25)  #
        pl.ChangeDutyCycle(steer * speed * 25)  #
    elif steer > 1:
        steer = 2 - steer
        pr.ChangeDutyCycle(steer * speed * 25)  #
        pl.ChangeDutyCycle(((1 - steer) * speedHead + speed) * 25)  #
    return


def sensor(delay, run_event):
    steer = 1
    while run_event.is_set():
        last_steer = steer
        steer = linienfahren()
        if steer is None:
            test = distanz("L")
            if test < 60:
                steer = wandfahren()
            else:
                steer = last_steer
        lenken(steer)
        time.sleep(delay)


def main():
    # print ("Taster drücken")
    # while GPIO.input(GPIO_TASTER) == 1:
    #    time.sleep(.1)
    # print("Start in 1 Sekunde", end="\r")
    time.sleep(1)

    losfahren()
    pr.start(speed)  # Motor A, speed% Tastverhältnis
    pl.start(speed)  # Motor B, speed% Tastverhältnis

    run_event = threading.Event()
    run_event.set()

    th1_delay = .02  # sleep dauer der Funktion
    th2_delay = .02  # sleep dauer der Funktion
    th3_delay = .02  # sleep dauer der Funktion
    th1 = threading.Thread(target=sensor, args=(th1_delay, run_event))  # Funkton in einem neuen Thread zuordnen
    # th2 = threading.Thread(target = linienfahren, args = (th2_delay,run_event)) # Funkton in einem neuen Thread zuordnen
    # th3 = threading.Thread(target = sensor, args = (th3_delay,run_event)) # Funkton in einem neuen Thread zuordnen

    th1.start()  # Thread starten
    # th2.start() # Thread starten
    # th3.start() # Thread starten

    # Warten bis Srtg+C gedrückt wird:
    try:
        while 1:
            time.sleep(.01)

    except KeyboardInterrupt:
        print("attempting to close threads. Max wait =", max(th1_delay, 0))  #
        run_event.clear()
        th1.join()
        aufraeumen()
        print("threads successfully closed")


if __name__ == '__main__':
    main()
